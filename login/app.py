#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, g, session
from flask.ext.mysqldb import MySQL 
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'sql7.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql7112481'
app.config['MYSQL_PASSWORD'] = 'sf9MHtn6p5'
app.config['MYSQL_DB'] = 'sql7112481'
mysql = MySQL(app)

#Metod som kontrollerar om det inmatade username och password stämmer 
#med det username och password som finns lagrade i databasen
@app.route('/', methods=['GET', 'POST'])
def index():
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
			error = "Fel password"

	return render_template('login.html', error=error)

#Metod som anropas före index metoden. Metoden kontrollerar
#om det finns en user i session 
@app.before_request
def before_request():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(seconds=20) #Om inget händer på 20 sek så droppas sessionen
	g.user = None
	if 'user' in session:
		g.user = session['user']

#Metod som visar admin sidan som man kommer till när man har loggat in
@app.route('/welcome')
def welcome():
	if g.user:
		return render_template('welcome.html')

	if request.method == 'POST':
		return render_template('index.html')

	return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)