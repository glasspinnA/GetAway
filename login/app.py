from flask import Flask, render_template, redirect, url_for, request
from flask.ext.mysqldb import MySQL 


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql7.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql7111382'
app.config['MYSQL_PASSWORD'] = 'VkMW5xVfX2'
app.config['MYSQL_DB'] = 'sql7111382'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
	#Skapar en anslutning till servern
	cur = mysql.connection.cursor()
	
	error = None
	if request.method == 'POST':
		usernameInput = request.form['username']
		passwordInput = request.form['password']
		cur.execute('SELECT username FROM admin WHERE username =%s', [usernameInput])
		usernameFromDB = cur.fetchone()[0]
		cur.execute('SELECT password FROM admin WHERE username =%s', [usernameInput])
		passwordFromDB = cur.fetchone()[0]
		if usernameInput != usernameFromDB or passwordInput != passwordFromDB:
			error = "Wrong password"	
		else:
			error = "KOM IN"
	return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)