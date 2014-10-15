from . import api, conf
from conf import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_SECRET, ACCESS_KEY
from utils import Token

def home_timeline():
    consumer = Token(CONSUMER_KEY,CONSUMER_SECRET)
    token = Token(ACCESS_KEY,ACCESS_SECRET)
        
    return api.api('https://api.twitter.com/1.1/statuses/home_timeline.json',
            token, {'count':100})