from flask import Flask, redirect, url_for, session, request
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_oauthlib.client import OAuth
import facebook


SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '690228564355373'
FACEBOOK_APP_SECRET = '123a723b5e269c5d2b7274377317d965'


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook_o = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

@facebook_o.tokengetter
def get_facebook_oauth_token():
    if session.has_key('oauth_tokens'):
        del session['oauth_tokens']
    return session.get('oauth_token')

@app.before_request
def before_request():
    g.user = None
    if 'oauth_token' in session:
        g.user = session['oauth_token']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return facebook_o.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/logout')
def logout():
    session.pop('oauth_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
@facebook_o.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = resp
    me = facebook_o.get('/me')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    token=get_facebook_oauth_token()
    graph = facebook.GraphAPI(token['access_token'])
    profile = graph.get_object("me")
    me = facebook_o.get('/me/friends')
    return render_template('facebook.html', voici=profile)

if __name__ == '__main__':
    app.run()