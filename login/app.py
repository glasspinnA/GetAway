from flask import Flask, render_template, redirect, url_for, request, g, session
from flask.ext.mysqldb import MySQL 
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'sql7.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql7112481'
app.config['MYSQL_PASSWORD'] = 'sf9MHtn6p5'
app.config['MYSQL_DB'] = 'sql7112481'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	#Skapar en anslutning till servern
	cur = mysql.connection.cursor()
	error = None
	if request.method == 'POST':
		session.pop('user',None)

		usernameInput = request.form['username']
		passwordInput = request.form['password']
		cur.execute('SELECT username FROM adminDB WHERE username =%s', [usernameInput])
		usernameFromDB = cur.fetchone()[0]
		cur.execute('SELECT password FROM adminDB WHERE username =%s', [usernameInput])
		passwordFromDB = cur.fetchone()[0]

		if usernameInput == usernameFromDB and passwordInput == passwordFromDB:
			session['user'] = usernameInput
			return redirect(url_for('welcome'))	
		else:
			error = "Wrong password"

	return render_template('login.html', error=error)

@app.route('/welcome')
def welcome():
	if g.user:
		return render_template('welcome.html')

	return redirect(url_for('index'))

@app.before_request
def before_request():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(seconds=20)
	g.user = None
	if 'user' in session:
		g.user = session['user']


if __name__ == '__main__':
    app.run(debug=True)