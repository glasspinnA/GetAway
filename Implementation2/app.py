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

loginDatbaseInfo = open("/Users/Oliver/Desktop/Implementation2/loginDatbaseInfo.txt").read()
loginDatbaseInfo = loginDatbaseInfo.split()
host = loginDatbaseInfo[0]
user = loginDatbaseInfo[1]
password = loginDatbaseInfo[2]
db = loginDatbaseInfo[3]

mysql = pymysql.connect(host=host, user=user, password=password, db=db)

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

app.config['UPLOAD_FOLDER'] = '/Users/Oliver/Desktop/Implementation2/static/Uploads'
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)

# SIDA: Start.

@app.route('/')
def main():
    return render_template('index.html')

# FUNKTION: Ladda upp fil.

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':f_name})

# SIDA: Lägg till.
    
@app.route('/add')
def showAddWish():
    #if session.get('user'):
        return render_template('addWish.html')
    #else:
    #    return render_template('error.html', error = 'Unauthorized Access')

# FUNKTION: Uppdatera inlägg.
    
@app.route('/updateWish', methods=['POST'])
def updateWish():
    try:
        with mysql.cursor() as cursor:
            #if session.get('user'):
                _title = request.form['title']
                _country = request.form['country']
                _description = request.form['description']
                _wish_id = request.form['id']
                _filePath = request.form['filePath']
                _tag = request.form['tag']
  
                cursor.callproc('sp_updateWish',(_title,_country,_description,_wish_id.split(),_filePath,_tag))
                data = cursor.fetchall()

                if len(data) is 0:
                    mysql.commit()
                    return json.dumps({'status':'OK'})
                else:
                    return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})
    finally:
        cursor.close()
    
# FUNKTION: Hämta alla inlägg (från databasen).
    
@app.route('/getAllWishes')
def getAllWishes():
    try:
        with mysql.cursor() as cursor:
            cursor.callproc('sp_GetAllWishes',())
            result = cursor.fetchall()
                         
            wishes_dict = []
            for wish in result:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
						'Country': wish[2],
                        'Description': wish[3],
                        'FilePath': wish[4],
                        'Tag': wish[5]} 
                wishes_dict.append(wish_dict)
                
            return json.dumps(wishes_dict)
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
                
# SIDA: Visa alla inlägg.
        
@app.route('/dashboard')
def showDashboard():
        return render_template('dashboard.html')

# FUNKTION: Ta bort inlägg.

@app.route('/deleteWish',methods=['POST'])
def deleteWish():
    try:
        with mysql.cursor() as cursor:
        
            #if session.get('user'):
                _id = request.form['id']

                cursor.callproc('sp_deleteWish',(_id.split()))
                result = cursor.fetchall()

                if len(result) is 0:
                    mysql.commit()
                    return json.dumps({'status':'OK'})
                else:
                    return json.dumps({'status':'An Error occured'})
            #else:
            #    return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        
# FUNKTION: Hämta ett inläggs id (används för redigering).
    
@app.route('/getWishById',methods=['POST'])
def getWishById():
    try:
        with mysql.cursor() as cursor:
            #if session.get('user'):
            
                _id = request.form['id']
    
                cursor.callproc('sp_GetWishById',(_id.split()))
                result = cursor.fetchall()

                wish = []
                wish.append({'Id':result[0][0],'Title':result[0][1],'Country': result[0][2],'Description':result[0][3],'FilePath':result[0][4],'Tag':result[0][5]})

                return json.dumps(wish)
            #else:
            #    return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    
# FUNKTION: Lägg till.   
        
@app.route('/addWish',methods=['POST'])
def addWish():    
    try:
        with mysql.cursor() as cursor:
            #if session.get('user'):
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
            #else:
            #    return render_template('error.html', error = 'Unauthorized Access')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()

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
                    flash("Fel användarnamn eller lösenord")
            return render_template('login.html')
    except Exception as e:
        flash("Fel användarnamn eller lösenord")
        return render_template('login.html')
    finally:
        cursor.close()
             
#Metod som renderar admin sidan
@app.route('/admin')
def welcome():
    if g.user:
        return render_template('welcome.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')
    return redirect(url_for('login'))

#Metod som droppar ens session när man loggar ut från admin sidan
@app.route('/admin', methods=["POST","GET"])
def logout():
    session.pop('user', None)
    flash("Du är utloggad")
    return redirect(url_for('login'))

#Metod som ändrar lösenordet till admin kontont.
#Skickar det nya lösenordet till DB och ersätter det gamla lösenordet
@app.route("/changeContactInfo", methods=["POST","GET"])
def changePassword():
    if g.user:
        try:
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
                        flash("Det gamla lösenordet är felaktigt eller så stämmer det nya lösenordet inte överrens")
        except Exception as e:
            return render_template('error.html',error = str(e)) 
        finally:
            cursor.close() 
        return render_template('changeContactInfo.html')
    return redirect(url_for('login'))

# SIDA: Hämta alla tags.
        
@app.route('/data_post', methods=['POST'])
def data_post():
    
    checkboxArray = request.form['data'];
    
    print(checkboxArray)
   
    return checkboxArray
if __name__ == "__main__":
    app.run(debug=True, port=5002)