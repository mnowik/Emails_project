from flask import Flask,render_template,request,json
app = Flask(__name__)

#---------------contextio loader------------------
import contextio as c

CONSUMER_KEY = 'key'
CONSUMER_SECRET = 'pass'
ID = 'id' 


context_io = c.ContextIO(
	consumer_key=CONSUMER_KEY,
	consumer_secret=CONSUMER_SECRET
	)

#---------------template in html---------------
@app.route('/messages')
def messages(name=None):
    return render_template('slides.html', emails=messages())


@app.route('/login')
def login(name=None):
    return render_template('login.html')


@app.route('/login1', methods=['GET', 'POST'])
def login1():
    return 'bonjour'




@app.route('/login2', methods=["GET", "POST"])
def login2():
    if request.method == "POST":
    	accounts = context_io.post_accounts()
	# since we return a list, let's be sure we have a result
	if accounts:
	    account = accounts[0]

	params = {
	   'email': request.data
	}
	account = c.Account(context_io, params)
	account.POST()

        return account



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
    app.run(debug=True)
