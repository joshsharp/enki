# Taken almost verbatim from Henrik Lied's django-twitter-oauth app
# http://github.com/henriklied/django-twitter-oauth

import json
from oauth import oauth
import httplib
from conf import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_SECRET, ACCESS_KEY

signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

def consumer():
	try: return consumer._consumer
	except AttributeError:
		consumer._consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
		return consumer._consumer

def connection():
	#use a new connection every time to prevent breakage
	#connection._connection = httplib.HTTPConnection('twitter.com')
	return httplib.HTTPConnection('twitter.com')

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
	con.request(req.http_method, req.to_url())
	return con.getresponse().read()

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
    )))


def is_authorized(token):
	return api('http://twitter.com/account/verify_credentials.json',
		token)

def tweet(token,message):
    result = api('http://api.twitter.com/1/statuses/update.json',token,{"status":message},http_method="POST")
    return result