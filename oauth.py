import webbrowser
import scapi

API_HOST = "api.sandbox-soundcloud.com"

CONSUMER = "7677c24753cabb115546da3c30a63c94"
CONSUMER_SECRET = "caeb1283c7f456eb4a6a347a8bcc7a59"

# first, we create an OAuthAuthenticator that only knows about consumer
# credentials. This is done so that we can get an request-token as
# first step.
oauth_authenticator = scapi.authentication.OAuthAuthenticator(CONSUMER, 
                                                              CONSUMER_SECRET,
                                                              None, 
                                                              None)

# The connector works with the authenticator to create and sign the requests. It
# has some helper-methods that allow us to do the OAuth-dance.
connector = scapi.ApiConnector(host=API_HOST, authenticator=oauth_authenticator)

# First step is to get a request-token, and to let the user authorize that
# via the browser.
token, secret = connector.fetch_request_token()
authorization_url = connector.get_request_token_authorization_url(token)
webbrowser.open(authorization_url)
oauth_verifier = raw_input("please enter verifier code as seen in the browser:")

# Now we create a new authenticator with the temporary token & secret we got from
# the request-token. This will give us the access-token
oauth_authenticator = scapi.authentication.OAuthAuthenticator(CONSUMER, 
                                                              CONSUMER_SECRET,
                                                              token, 
                                                              secret)

# we need a new connector with the new authenticator!
connector = scapi.ApiConnector(API_HOST, authenticator=oauth_authenticator)
token, secret = connector.fetch_access_token(oauth_verifier)


# now we are finally ready to go - with all four parameters OAuth requires,
# we can setup an authenticator that allows for actual API-calls.
oauth_authenticator = scapi.authentication.OAuthAuthenticator(CONSUMER, 
                                                              CONSUMER_SECRET,
                                                              token, 
                                                              secret)

# we pass the connector to a Scope - a Scope is essentially a path in the REST-url-space.
# Without any path-component, it's the root from which we can then query into the
# resources.
root = scapi.Scope(scapi.ApiConnector(host=API_HOST, authenticator=oauth_authenticator))

# Hey, nice meeting you!  Connected to SoundCloud using OAuth will allow you to access protected resources, like the current user's name.  
print "Hello, %s" % root.me().username
