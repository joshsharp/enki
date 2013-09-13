#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from oauth.oauth import OAuthRequest, OAuthSignatureMethod_HMAC_SHA1
from datetime import datetime
from hashlib import md5
import urllib, urllib2, json
import sys, os
import time
import random, math, re
import threading
from twitter import stream, conf
from twitter.utils import relativetime
from connector import Connector
from qt.preview import PreviewDialog

class MainWindow(QMainWindow):
    
    refreshReady = Signal(list)
    tweets = {}
    dms = {}
    
    username = 'joshsharp'
    
    
    DM_TEMPLATE = """
    <div class="dm" id="t%s"><img class="avatar" src="%s"/>
        <div class="inner"><span class="user">%s</span> %s
            <div class="meta"><span class="time">%s</span></div>
        </div>
    </div>
    """
    
    DM_FROM_TEMPLATE = """
    <div class="dm" id="t%s"><img class="avatar" src="%s"/>
        <div class="inner"><span class="user dm-to">%s</span> %s
            <div class="meta"><span class="time">%s</span></div>
        </div>
    </div>
    """
    
    TWEET_TEMPLATE = """
    <div class="tweet %s" id="t%s">
        <img class="avatar" src="%s"/>
        <div class="inner"><span class="user">%s</span> %s
            <div class="meta"><span class="time">%s</span> from <span class="source">%s</span></div>
        </div>
    </div>
    """
    
    RETWEET_TEMPLATE = """
    <div class="tweet" id="t%s">
        <img class="avatar" src="%s"/>
            <div class="inner rt">RT by <span class="user">%s</span></div>            
            <div class="inner"><span class="user">%s</span> %s
            <div class="meta"><span class="time">%s</span> from <span class="source">%s</span></div>
        </div>
    </div>
    """
    
    def create_menus(self):

        #fileMenu = self.menuBar().addMenu("&File")
        self.toolbars["main"] = self.addToolBar("File")
        self.toolbars["main"].setObjectName("File")
        self.toolbars["main"].setFloatable(False)
        self.toolbars["main"].setMovable(False)
        
        #profileIcon = QIcon("user.png")
        self.toolbars["main"].addAction(QIcon("comment.png"),"New Post")
        self.toolbars["main"].addSeparator()
        self.toolbars["main"].hide()
        #self.toolbars["main"].addAction(QIcon("refresh.png"),"Refresh",self.refresh)
        #self.toolbars["main"].setIconSize(QSize(32,32))
        
        #self.toolbars["status"] = QStatusBar()
        #self.setStatusBar(self.toolbars["status"])
        #self.toolbars["status"].showMessage("Ready")

    def setup_layout(self):
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.widgets["central"] = QWidget()
        self.setCentralWidget(self.widgets["central"])
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.layouts["central"] = layout
        self.widgets["central"].setLayout(layout)
        
        top = QWidget()
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(5,5,5,5)
        top.setLayout(top_layout)
        top.setMaximumHeight(64)
        top.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed))
        
        self.widgets['top'] = top
        self.layouts['top'] = top_layout
        
        status = QTextEdit()
        #status.setSizeHint(0,QSize(0,22))
        top_layout.addWidget(status)        
        layout.addWidget(top)
        top.hide()
        
        web = QWebView(self.widgets["central"])
        self.widgets['web'] = web
        layout.addWidget(web)
        
        #splitter.addWidget(web)
        #layout.addWidget(splitter)
        
        path = os.getcwd()
        
        web.load(QUrl.fromLocalFile(path + '/base/base.html'))
        self.web = web
        self.web_frame = web.page().mainFrame()
        web.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        web.page().linkClicked.connect(self.launch_link)
        #self.web_frame.setScrollBarPolicy(Qt.Vertical,Qt.ScrollBarAlwaysOff)
        self.connector = Connector(self)
        self.connector.sendJS.connect(self.web_frame.evaluateJavaScript)
        self.web_frame.addToJavaScriptWindowObject("connector", self.connector)
        
        menu = QMenu()
        menu.addAction("Profile")
        menu.addAction("Accounts")
        menu.addAction("Settings")
        self.sys_menu = menu
    
    def __init__(self):
        QMainWindow.__init__(self,None)
        self.setWindowTitle("Enki - joshsharp")
        self.widgets = {}
        self.layouts = {}
        self.menus = {}
        self._data = None
        self._event = None
        self.toolbars = {}

        #file = QFile("main.ui")
        #file.open(QFile.ReadOnly)
        #self.window = loader.load(file, self)
        #file.close()
        self.setWindowIcon(QIcon("icon.png"))
        settings = QSettings("Recursive", "Musca")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))

        #layout = QVBoxLayout()
        #layout.addWidget()
        #self.setLayout(self.window.findChild(QLayout,"verticalLayout_4"))
        
        self.create_menus()
        self.setup_layout()
        self.refreshReady.connect(self.refreshed)
        
        
        self.refresh()
        
        #return HttpResponse(response.read(),content_type='application/json')
        
        #self.friends_list = self.widgets["friends_list"]
        #self.add_items(items)
        #self.model = SimpleListModel([i["text"] for i in items])
        #self.friends_list.setModel(self.model)
        
        #self.timer = QTimer(self)
        #self.connect(self.timer,SIGNAL("timeout()"),self.refresh)
        #self.timer.start(120000)
    
    def show_sys_menu(self,x,y):
        self.sys_menu.popup(self.web.mapToGlobal(QPoint(x,y)))
    
    def show_preview(self,url):
        d = PreviewDialog(self)
        d.show()
        d.activateWindow()
    
    def launch_link(self,url):
        QDesktopServices.openUrl(url)
       
    def refresh(self):
                
        self.streamtask = threading.Thread(target=stream.connect,args=[self.refreshReady])        
        self.streamtask.start()
        
        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self.update_times)
        timer.start(20000)
    
    def update_times(self):
        print "updating times"
        tweets = self.web_frame.findAllElements("div.tweet")
        for tweet in tweets:
            t = self.tweets[long(tweet.attribute('id')[1:])]
            meta = tweet.findFirst('.time')
            meta.setInnerXml(relativetime(t['created_at']))
            
        tweets = self.web_frame.findAllElements("div.dm")
        for tweet in tweets:
            t = self.dms[long(tweet.attribute('id')[1:])]
            meta = tweet.findFirst('.time')
            #print 'dm %s' % t['direct_message']['id']
            #print meta
            #print relativetime(t['direct_message']['created_at'])
            meta.setInnerXml(relativetime(t['direct_message']['created_at']))
    
    
    def parse_text(self,text,entities):
        
        for url in entities.get('urls',[]):
            
            text = text.replace(url['url'],'<a class="link" href="%s" target="_blank">%s</a>' % (url['expanded_url'],url['display_url']))
        
        
        for url in entities.get('media',[]):
            
            text = text.replace(url['url'],'<a class="media" href="%s">%s</a>' % (url['expanded_url'],url['display_url']))
        
        for user in entities.get('user_mentions',[]):
            text = text.replace("@%s" % user['screen_name'],'@<a class="username" href="javascript:;" target="_blank">%s</a>' % user['screen_name'],1)
            text = text.replace("@%s" % user['screen_name'].lower(),'@<a class="username" href="javascript:;" target="_blank">%s</a>' % user['screen_name'],1)
            
        for hash in entities.get('hashtags',[]):
            text = text.replace('#%s' % hash['text'],'<a class="link hash" href="javascript:;" target="_blank">#%s</a>' % hash['text'])
        
        text = text.replace("\n","<br/>")
        
        return text
    
    def parse_regex(self,text):
        
        return text
    
    def display_dm(self,tweet):
        self.dms[tweet['direct_message']['id']] =tweet
        print self.dms[tweet['direct_message']['id']]
        #print "%s: %s" % (tweet['direct_message']['sender']['screen_name'], tweet['direct_message']['text'])
        
        if tweet['direct_message'].get('entities'):
            text = self.parse_text(tweet['direct_message']['text'],tweet['direct_message'].get('entities'))
        else:
            text = self.parse_regex(tweet['direct_message']['text'])
        
        body = self.web_frame.findFirstElement("#timeline-dms")
        
        if tweet['direct_message']['sender']['screen_name'] == self.username:
            body.prependInside(self.DM_FROM_TEMPLATE % (tweet['direct_message']['id'],
                                               tweet['direct_message']['sender']['profile_image_url'],
                                               tweet['direct_message']['recipient']['screen_name'],
                                               text,
                                               relativetime(tweet['direct_message']['created_at'])))
        else:
        
            body.prependInside(self.DM_TEMPLATE % (tweet['direct_message']['id'],
                                               tweet['direct_message']['sender']['profile_image_url'],
                                               tweet['direct_message']['sender']['screen_name'],
                                               text,
                                               relativetime(tweet['direct_message']['created_at'])))
        QSound.play("dm2.wav")
    
    def display_tweet(self,tweet):
        self.tweets[tweet['id']] = tweet
        #print tweet['id']
        print self.tweets[tweet['id']]
        #print "%s: %s" % (tweet['user']['screen_name'], tweet['text'])
        
        text = self.parse_text(tweet['text'],tweet['entities'])
        mention = False
        t_class = ''
        
        for user in tweet['entities'].get('user_mentions',[]):
            if user['screen_name'] == conf.USERNAME:
                mention = True
                body = self.web_frame.findFirstElement("#timeline-mentions")
                body.prependInside(self.TWEET_TEMPLATE % ('',tweet['id'],
                                                  tweet['user']['profile_image_url'],
                                                  tweet['user']['screen_name'],
                                                  text,
                                                  relativetime(tweet['created_at']),
                                                  tweet['source']))
                break
            
        
        if mention:
            t_class = 'mention'
        
        body = self.web_frame.findFirstElement("#timeline-home")
        body.prependInside(self.TWEET_TEMPLATE % (t_class, tweet['id'],
                                                  tweet['user']['profile_image_url'],
                                                  tweet['user']['screen_name'],
                                                  text,
                                                  relativetime(tweet['created_at']),
                                                  tweet['source']))
        
        
        
                
        
            
    
    def display_retweet(self,tweet):
        self.tweets[tweet['id']] = tweet
        #print tweet['id']
        print self.tweets[tweet['id']]
        #print "%s: %s" % (tweet['user']['screen_name'], tweet['text'])
        
        text = self.parse_text(tweet['retweeted_status']['text'],tweet['retweeted_status']['entities'])
        
        body = self.web_frame.findFirstElement("#timeline-home")
        body.prependInside(self.RETWEET_TEMPLATE % (tweet['id'],
                                                  tweet['retweeted_status']['user']['profile_image_url'],
                                                  tweet['user']['screen_name'],
                                                  tweet['retweeted_status']['user']['screen_name'],
                                                  text,
                                                  relativetime(tweet['created_at']),
                                                  tweet['retweeted_status']['source'])) 
        
        
    def refreshed(self, data):
        try:
            tweet = json.loads(data)
        except:
            print "couldn't parse"
        else:
            
            if tweet.get('direct_message'):
                
                self.display_dm(tweet)
            
            elif tweet.get('retweeted_status'):
                
                self.display_retweet(tweet)
            
            elif tweet.get('text'):
                
                self.display_tweet(tweet)
                
            else:
                print "event: ", data
        
    def closeEvent(self,e):
        print 'closing'
        settings = QSettings("Recursive", "Musca")
        
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState()) 
        #self.streamtask = None
        print self.tweets.keys()
        

