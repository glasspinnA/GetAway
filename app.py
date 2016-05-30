#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, json, request,redirect,session,jsonify, url_for,g, flash
import pymysql.cursors
import random
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.wsgi import LimitedStream
from datetime import timedelta
import uuid
import os

app = Flask(__name__)

# DATABAS: Uppgifter för anslutning.
app.secret_key = os.urandom(24)

loginDatbaseInfo = open("loginDatbaseInfo.txt").read()
loginDatbaseInfo = loginDatbaseInfo.split()
host = loginDatbaseInfo[0]
user = loginDatbaseInfo[1]
password = loginDatbaseInfo[2]
db = loginDatbaseInfo[3]
charset = 'utf8mb4'

mysql = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)

# Fix för Connection Reset på POST
# Mer info om denna klass:
# http://flask.pocoo.org/snippets/47/
class StreamConsumingMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        stream = LimitedStream(environ['wsgi.input'],
                               int(environ['CONTENT_LENGTH'] or 0))
        environ['wsgi.input'] = stream
        app_iter = self.app(environ, start_response)
        try:
            stream.exhaust()
            for event in app_iter:
                yield event
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()

app.config['UPLOAD_FOLDER'] = 'static/Uploads'
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)

# SIDA: Start.

@app.route('/')
def main():
    return render_template('index.html')

# FUNKTION: Ladda upp fil.

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if session.get('user'):
        if request.method == 'POST':
            file = request.files['file']
            extension = os.path.splitext(file.filename)[1]
            f_name = str(uuid.uuid4()) + extension
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
            return json.dumps({'filename':f_name})
    else:
        return ('Unauthorized Access')

# SIDA: Lägg till.
    
@app.route('/add')
def showAdd():
    if session.get('user'):
        return render_template('add.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')

# FUNKTION: Uppdatera inlägg.
    
@app.route('/update', methods=['POST'])
def update():
    try:
        mysql.connect()
        with mysql.cursor() as cursor:
            if session.get('user'):
                _title = request.form['title']
                _country = request.form['country']
                _description = request.form['description']
                _destination_id = request.form['id']
                _filePath = request.form['filePath']
                _tag = request.form['tag']
  
                cursor.callproc('sp_updateWish',(_title,_country,_description,_destination_id.split(),_filePath,_tag))
                data = cursor.fetchall()

                if len(data) is 0:
                    mysql.commit()
                    return json.dumps({'status':'OK'})
                else:
                    return json.dumps({'status':'ERROR'})
            else:
                return ('Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})
    finally:
        cursor.close()
        mysql.close()
    
# FUNKTION: Hämta alla inlägg (från databasen).
    
@app.route('/getAll')
def getAll():
    try:
        mysql.connect()
        with mysql.cursor() as cursor:
                cursor.callproc('sp_GetAllWishes',())
                destinations = cursor.fetchall()
                         
                destinations_dict = []
                for destination in destinations:
                    destination_dict = {
                            'Id': destination[0],
                            'Title': destination[1],
						  'Country': destination[2],
                            'Description': destination[3],
                            'FilePath': destination[4],
                            'Tag': destination[5]} 
                    destinations_dict.append(destination_dict)
                
                return json.dumps(destinations_dict)
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        mysql.close()
                
# SIDA: Visa alla inlägg.
        
@app.route('/dashboard')
def showDashboard():
    if g.user:
        return render_template('dashboard.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')
    
# FUNKTION: Ta bort inlägg.

@app.route('/delete',methods=['POST'])
def delete():
    try:
        mysql.connect()
        with mysql.cursor() as cursor:
            if session.get('user'):
                _id = request.form['id']

                cursor.callproc('sp_deleteWish',(_id.split()))
                result = cursor.fetchall()

                if len(result) is 0:
                    mysql.commit()
                    return json.dumps({'status':'OK'})
                else:
                    return json.dumps({'status':'An Error occured'})
            else:
                return ('Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        mysql.close()
        
# FUNKTION: Hämta ett inläggs id (används för redigering).
    
@app.route('/getById',methods=['POST'])
def getById():
    try:
        mysql.connect()
        with mysql.cursor() as cursor:
            if session.get('user'):
            
                _id = request.form['id']
    
                cursor.callproc('sp_GetWishById',(_id.split()))
                result = cursor.fetchall()

                destination = []
                destination.append({'Id':result[0][0],'Title':result[0][1],'Country': result[0][2],'Description':result[0][3],'FilePath':result[0][4],'Tag':result[0][5]})

                return json.dumps(destination)
            else:
                return ('Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        mysql.close()
    
# FUNKTION: Lägg till.   
        
@app.route('/addDestination',methods=['POST'])
def addDestination():    
    try:
        mysql.connect()
        with mysql.cursor() as cursor:
            if session.get('user'):
                _title = request.form['inputTitle']
                _country = request.form['inputCountry']
                _description = request.form['inputDescription']
                
                if request.form.get('filePath') is None:
                    _filePath = ''
                else:
                    _filePath = request.form.get('filePath')

                _tag = " "
                storeTags = ""
                checkboxArray = []
                checkboxArray = request.form.getlist("inputTag")
                for i in checkboxArray:
                    storeTags += i + ", "               
                _tag = storeTags   

                cursor.callproc('sp_addWish',(_title,_country,_description,_filePath,_tag))
                data = cursor.fetchall()

                if len(data) is 0:
                    mysql.commit()
                    return redirect('/dashboard')
                else:
                    return render_template('error.html',error = 'An error occurred!')
            else:
                return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        mysql.close()

#Metod som kontrollerar om det finns någon aktiv session eller inte
#Metoden droppar också session om den har varit inaktiv i 20 sekunder
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20) #Om inget händer på 20 sek så droppas sessionen
    g.user = None
    if 'user' in session:
        g.user = session['user']

#Metod som kontrollerar om username och password
#stämmer överrens med det username och password som finns i DB
@app.route('/login',methods=['POST','GET'])
def login():
    global passwordFromDB
    try:
        mysql.connect()
        with mysql.cursor() as cursor:
            if request.method == 'POST':
                usernameInput = request.form['username']
                passwordInput = request.form['password']
                cursor.execute('SELECT username FROM tbl_login WHERE username =%s', [usernameInput])
                usernameFromDB = cursor.fetchone()[0]
                cursor.execute('SELECT password FROM tbl_login WHERE username =%s', [usernameInput])
                passwordFromDB = cursor.fetchone()[0]
                if usernameInput == usernameFromDB and check_password_hash(passwordFromDB, passwordInput):
                    session['user'] = usernameInput
                    return redirect(url_for('welcome'))
                else:
                    flash("Wrong username or password")
            return render_template('login.html')
    except Exception as e:
        flash("Wrong username or password")
        return render_template('login.html')
    finally:
        cursor.close()
        mysql.close()
             
#Metod som renderar admin sidan
@app.route('/admin')
def welcome():
    if g.user:
        return render_template('admin.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')
    return redirect(url_for('login'))

#Metod som droppar ens session när man loggar ut från admin sidan
@app.route('/admin', methods=["POST","GET"])
def logout():
    session.pop('user', None)
    flash("You are signed out")
    return redirect(url_for('login'))

@app.route('/error', methods=["POST","GET"])
def error():
	if request.method == "POST":
		return redirect(url_for("login"))
	return render_template('error.html')


#Metod som ändrar lösenordet till admin kontont.
#Skickar det nya lösenordet till DB och ersätter det gamla lösenordet
@app.route("/changePassword", methods=["POST","GET"])
def changePassword():
    if g.user:
        try:
            mysql.connect()
            with mysql.cursor() as cursor:
                if request.method == "POST":
                    oldPasswordInput = request.form['oldPassword']
                    newPasswordInput = request.form['newPassword']
                    newPasswordCheckInput = request.form['newPasswordChecker']
                    if check_password_hash(passwordFromDB, oldPasswordInput) and newPasswordInput == newPasswordCheckInput:
                        newPassword = generate_password_hash(newPasswordInput)
                        cursor.execute('UPDATE tbl_login SET password=%s WHERE password=%s', (newPassword,passwordFromDB))
                        flash("Lösenordet är nu ändrat")
                        mysql.commit()
                    else:
                        flash("The old password is incorrect or the new password does not match.")
        except Exception as e:
            return render_template('error.html',error = str(e)) 
        else:
            return ('Unauthorized Access')
        finally:
            cursor.close()
            mysql.close()
            return render_template('changePassword.html')
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=5002)