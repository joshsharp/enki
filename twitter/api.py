# Taken almost verbatim from Henrik Lied's django-twitter-oauth app
# http://github.com/henriklied/django-twitter-oauth

import json
from oauth import oauth
import httplib
from conf import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_SECRET, ACCESS_KEY
import requests

signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

def consumer():
	try: return consumer._consumer
	except AttributeError:
		consumer._consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
		return consumer._consumer

def connection():
	#use a new connection every time to prevent breakage
	#connection._connection = httplib.HTTPConnection('twitter.com')
	return httplib.HTTPSConnection('twitter.com')

def oauth_request(
	url,
	token,
	parameters=None,
	signature_method=signature_method,
	http_method='GET'):
	
	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), token=token, http_url=url,
		parameters=parameters, http_method=http_method
	)
	req.sign_request(signature_method, consumer(), token)
	return req

def oauth_response(req):
	con = connection()
	print req.to_url()
	if req.http_method == 'GET':
		resp = requests.get(req.to_url())
	else:
		resp = requests.post(req.to_url())
	return resp.content

def get_unauthorized_token(signature_method=signature_method):
	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), http_url='http://twitter.com/oauth/request_token'
	)
	req.sign_request(signature_method, consumer(), None)
	try:
		return oauth.OAuthToken.from_string(oauth_response(req))
	except:
		return None

def get_authorization_url(token, signature_method=signature_method):
	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), token=token,
		http_url='http://twitter.com/oauth/authenticate' #authorize
	)
	req.sign_request(signature_method, consumer(), token)
	return req.to_url()

def get_authorized_token(token, signature_method=signature_method):
	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), token=token,
		http_url='http://twitter.com/oauth/access_token'
	)
	req.sign_request(signature_method, consumer(), token)
	return oauth.OAuthToken.from_string(oauth_response(req))

def api(url, token, params = None, http_method='GET'):

    return json.loads(oauth_response(oauth_request(
        url, token, http_method=http_method, parameters=params
    )),encoding='utf-8')


def is_authorized(token):
	return api('https://twitter.com/account/verify_credentials.json',
		token)

def tweet(token,message):
    result = api('https://api.twitter.com/1.1/statuses/update.json',token,{"status":message},http_method="POST")
    return result