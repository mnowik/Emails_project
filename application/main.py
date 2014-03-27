from flask import Flask, redirect, url_for, session, request
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_oauthlib.client import OAuth
import facebook


SECRET_KEY = 'development key'
DEBUG = True


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

 #---------------- oauth part ----------------
facebook_o = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'read_stream'}
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
    session['username']=facebook_o.get('/me').data['name']
    return redirect(url_for('index'))


#------------------- real apps ------------------
@app.route('/profile')
def profile():
    graph = facebook.GraphAPI(session['oauth_token']['access_token'])
    profile = graph.get_object("me",fields="feed")
    #ami=graph.get_object("522000987",fields="bio")
    #amis=graph.get_objects({"1142987430","522000987"})
    #friends = graph.get_connections("me", "friends")
    #newsfeed = graph.get_connections("me", "home")
    #feed = graph.get_connections("me", "permissions")
    return render_template('facebook.html',profile=profile)
if __name__ == '__main__':
    app.run()