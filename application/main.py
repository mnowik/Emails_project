from flask import Flask,render_template
app = Flask(__name__)

#---------------contextio loader------------------
import contextio as c

'''CONSUMER_KEY = 'key'
CONSUMER_SECRET = 'pass'
ID = 'id' '''


context_io = c.ContextIO(
	consumer_key=CONSUMER_KEY, 
	consumer_secret=CONSUMER_SECRET
	)

#---------------template in html---------------
@app.route('/')
def hello(name=None):
    return render_template('simple.html', emails=messages())



#----------------- functions------------------
'''def connection():

	accounts = context_io.get_accounts()
	# since we return a list, let's be sure we have a result
	if accounts:
	    account = accounts[0]

	params = {
	   'id': ID
	}
	account = c.Account(context_io, params)
	account.get()
	return account.username'''

def messages():
	accounts = context_io.get_accounts()
	# since we return a list, let's be sure we have a result
	if accounts:
	    account = accounts[0]
	params = {
	   'id': ID
	}
	emails=c.Account(context_io,params).get_messages()
	return emails


if __name__ == '__main__':
    app.run()
