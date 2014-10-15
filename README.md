# Enki

A Python+Qt Twitter desktop client using the streaming twitter endpoints.

Requirements:

* oauth
* pyside
* requests

You will need to specify your own twitter client details in `twitter/conf.py`. The constants are provided for you in `conf_example.py`.

There is no login implemented, just hard-code your own access token like a real developer. The easiest way to do this is to [create a new app](https://apps.twitter.com/) and use Twitter's tools to generate yourself a token.

### Still to do

Basically everything. It's good for watching your timeline go by, and not much else.

* Favourites
* Quoted RTs
* Preload mention and DM timelines with REST API (home timeline is implemented)
* Loading images, profiles, conversation views within the app
* Search and user lookup
* Handling streaming events like follow and delete
* Notifications
* Unread badges
