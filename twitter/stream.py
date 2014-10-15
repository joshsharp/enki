#!/usr/bin/env python

import json, time
from oauth.oauth import OAuthRequest, OAuthSignatureMethod_HMAC_SHA1
from datetime import datetime
import random, math, re, urllib, urllib2
from conf import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_SECRET, ACCESS_KEY
from utils import Token
import endpoints

STREAM_URL = "https://userstream.twitter.com/2/user.json"


def connect(signal):    
    
    consumer = Token(CONSUMER_KEY,CONSUMER_SECRET)
    token = Token(ACCESS_KEY,ACCESS_SECRET)
        
    parameters = {
        'oauth_consumer_key': CONSUMER_KEY,
        'oauth_token': token.key,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_nonce': token._generate_nonce(),
        'oauth_version': '1.0',
    }
    
    access_token = token
    
    oauth_request = OAuthRequest.from_token_and_callback(access_token,
                    http_url=STREAM_URL, 
                    parameters=parameters)
    signature_method = OAuthSignatureMethod_HMAC_SHA1()
    signature = signature_method.build_signature(oauth_request, consumer, access_token)
    
    parameters['oauth_signature'] = signature
    
    data = urllib.urlencode(parameters)
    
    print "%s?%s" % (STREAM_URL,data)


    req = urllib2.urlopen("%s?%s" % (STREAM_URL,data))
    buffer = ''
    while True:
        
        chunk = req.read(1)
        if not chunk:
            print buffer
            break
        
        chunk = unicode(chunk)
        buffer += chunk
        
        tweets = buffer.split("\r\n",1)
        if len(tweets) > 1:
            #print tweets[0]
            signal.emit(tweets[0])
            buffer = tweets[1]
    

def home_timeline(signal):
    statuses = endpoints.home_timeline()
    
    statuses = reversed(statuses)
    
    for status in statuses:
        
        signal.emit(status)
    