#!/usr/bin/env python

import random, time
import math
from datetime import datetime
from hashlib import md5

class Token(object):
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret
        self.callback = None

    def _generate_nonce(self):
        random_number = ''.join(str(random.randint(0, 9)) for i in range(40))
        m = md5(str(time.time()) + str(random_number))
        return m.hexdigest()
        
    def set_callback(self,func):
        self.callback = func
        


def relativetime(value, accuracy = 1):
    now = datetime.now().utcnow()
    
    time_format = "%a %b %d %H:%M:%S +0000 %Y" #"%Y-%m-%d %H:%M:%S"
    then = datetime.fromtimestamp(time.mktime(time.strptime(value, time_format)))
    #now = now.utcnow()
    
    #print now
    
    #then = value
    diff = now - then
    
    values = []
    i = 0    
    
    days = diff.days
    seconds = diff.seconds
    
    years = int(math.floor(days / 365))
    days -= years * 365
    weeks = int(math.ceil(days / 7))
    days -= weeks * 7
    hours = int(math.ceil(seconds / 3600))
    seconds -= hours * 3600
    minutes = int(math.ceil(seconds / 60))
    seconds -= minutes * 60
    
    if diff.days < 0:
        return "Just now"
    
    if years > 0:
        values.append("%d year%s" % (years, 's' if years != 1 else ''))
        i += 1
    
    if weeks > 0:
        values.append("%d week%s" % (weeks, 's' if weeks != 1 else ''))
        i += 1
    
    if days > 0 and i < accuracy:
        values.append("%d day%s" % (days, 's' if days != 1 else ''))
        i += 1
    
    if hours > 0 and i < accuracy:
        values.append("%d hour%s" % (hours, 's' if hours != 1 else ''))
        i += 1
    
    if minutes > 0 and i < accuracy:
        values.append("%d min%s" % (minutes, 's' if minutes != 1 else ''))
        i += 1
    
    if seconds > 0 and i < accuracy:
        values.append("%d second%s" % (seconds, 's' if seconds != 1 else ''))
        
    
    if len(values) == 0:
        return "Just now"
    
    return ", ".join(values) + ' ago'
