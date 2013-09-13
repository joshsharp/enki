#!/usr/bin/env python
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

from twitter import conf, api, utils

class Connector(QObject):
    
    sendJS = Signal(str)
    
    def __init__(self,window):
        self.token = utils.Token(conf.ACCESS_KEY,conf.ACCESS_SECRET)
        self.window = window
        super(Connector,self).__init__()
        
    
    @Slot(str)
    @Slot(str,int)
    def tweet(self,tweet,id=None):
        params = {"status":tweet}
        
        if len(tweet) > 140:
            return False        
        if id:
            params['in_reply_to_status_id'] = id
        
        try:
            result = api.api('http://api.twitter.com/1/statuses/update.json',self.token,
                         params,http_method='POST')
        except e:
            print e
        else:
            self.sendJS.emit("onTweetSuccess();")
        print "Connector tweet:", tweet, id, result

    @Slot(str,str)
    def dm(self,screen_name,text):
        result = api.api('http://api.twitter.com/1/direct_messages/new.json', self.token,
                         {"text":text,"screen_name":screen_name},http_method='POST')
        print "Connector DM:", screen_name, text, result
    
    @Slot(int)
    def fave(self,id):
        result = api.api('http://api.twitter.com/1/favorites/create/%s.json' % id, self.token,
                         http_method='POST')
        print "Connector fave:", id, result
    
    @Slot(int)
    def unfave(self,id):
        result = api.api('http://api.twitter.com/1/favorites/destroy/%s.json' % id, self.token,
                         http_method='POST')
        print "Connector unfave:", id, result
        
    @Slot(str)
    def follow(self,screen_name):
        result = api.api('http://api.twitter.com/1/friendships/create.json', self.token,
                         {"screen_name":screen_name}, http_method='POST')
        print "Connector follow:", screen_name, result
    
    @Slot(str)
    def unfollow(self,screen_name):
        result = api.api('http://api.twitter.com/1/friendships/destroy.json', self.token,
                         {"screen_name":screen_name}, http_method='POST')
        print "Connector unfollow:", screen_name, result
        
    @Slot(str)
    def block(self,screen_name):
        result = api.api('http://api.twitter.com/1/blocks/create.json', self.token,
                         {"screen_name":screen_name}, http_method='POST')
        print "Connector block:", screen_name, result
    
    @Slot(str)
    def spam(self,screen_name):
        result = api.api('http://api.twitter.com/1/report_spam.json', self.token,
                         {"screen_name":screen_name}, http_method='POST')
        print "Connector spam:", screen_name, result
        
    @Slot(int)
    def delete_tweet(self,id):
        result = api.api('http://api.twitter.com/1/statuses/destroy/%s.json' % id, self.token,
                         http_method='POST')
        print "Connector delete tweet:", id, result
    
    @Slot(int)
    def delete_dm(self,id):
        result = api.api('http://api.twitter.com/1/direct_messages/destroy/%s.json' % id, self.token,
                         http_method='POST')
        print "Connector delete dm:", id, result
        

    @Slot(str)
    def preview_url(self,url):
        self.window.show_preview(url)
        
    @Slot(int,int)
    def show_sys_menu(self,x,y):
        self.window.show_sys_menu(x,y)