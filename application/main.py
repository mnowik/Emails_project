from flask import Flask, redirect, url_for, session, request
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_oauthlib.client import OAuth


SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = 'id'
FACEBOOK_APP_SECRET = 'secret'


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

@facebook.tokengetter
def get_facebook_oauth_token():
    if session.has_key('facebook_oauth_tokens'):
        del session['facebook_oauth_tokens']
    return session.get('oauth_token')

@app.before_request
def before_request():
    g.user = None
    if 'facebook_oauth_tokens' in session:
        g.user = session['facebook_oauth_tokens']

@app.route('/')
def index():
    posts = []
    if g.user:
        posts='oui'

    return render_template('index.html', posts=posts)
'''
@app.route('/')
def index():
    return redirect(url_for('login'))
'''

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))




@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return render_template('index.html', posts=me)




if __name__ == '__main__':
    app.run()