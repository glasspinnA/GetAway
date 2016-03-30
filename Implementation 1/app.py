#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, json, request,redirect,session,jsonify, url_for
import pymysql.cursors
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.wsgi import LimitedStream
import uuid
import os

app = Flask(__name__)

mysql = pymysql.connect(host='sql7.freemysqlhosting.net',
                             user='sql7111162',
                             password='j37hIiC1L1',
                             db='sql7111162')

# Default setting
pageLimit = 5

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


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':f_name})


@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')




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
                        'Description': wish[2],
                        'FilePath': wish[3],}
                wishes_dict.append(wish_dict)
                
            return json.dumps(wishes_dict)
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()

@app.route('/showDashboard')
def showDashboard():
    return render_template('dashboard.html')
    
# Not being used but prepared
@app.route('/deleteWish',methods=['POST'])
def deleteWish():
    try:
        with mysql.cursor() as cursor:
        
            if session.get('user'):
                _id = request.form['id']    
                _user = session.get('user')

                conn = mysql.connect()
                cursor.callproc('sp_deleteWish',(_id,_user))
                result = cursor.fetchall()

                if len(result) is 0:
                    conn.commit()
                    return json.dumps({'status':'OK'})
                else:
                    return json.dumps({'status':'An Error occured'})
            else:
                return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()

# Not being used but prepared
@app.route('/getWishById',methods=['POST'])
def getWishById():
    try:
        with mysql.cursor() as cursor:
            if session.get('user'):
            
                _id = request.form['id']
                _user = session.get('user')
    
                conn = mysql.connect()
                cursor.callproc('sp_GetWishById',(_id,_user))
                result = cursor.fetchall()

                wish = []
                wish.append({'Id':result[0][0],'Title':result[0][1],'Description':result[0][2],'FilePath':result[0][3],'Private':result[0][4],'Done':result[0][5]})

                return json.dumps(wish)
            else:
                return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

# Not being used but prepared
@app.route('/getWish',methods=['POST'])
def getWish():
    try:
        with mysql.cursor() as cursor:
            if session.get('user'):
                _user = session.get('user')
                _limit = pageLimit
                _offset = request.form['offset']
                _total_records = 0

                conn = mysql.connect()
                cursor.callproc('sp_GetWishByUser',(_user,_limit,_offset,_total_records))
            
                wishes = cursor.fetchall()
                cursor.close()

                cursor.execute('SELECT @_sp_GetWishByUser_3');

                outParam = cursor.fetchall()

            

                response = []
                wishes_dict = []
                for wish in wishes:
                    wish_dict = {
                            'Id': wish[0],
                            'Title': wish[1],
                            'Description': wish[2],
                            'Date': wish[4]}
                    wishes_dict.append(wish_dict)
                response.append(wishes_dict)
                response.append({'total':outParam[0][0]}) 
                




                return json.dumps(response)
            else:
                return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/addWish',methods=['POST'])
def addWish():    
    try:
        with mysql.cursor() as cursor:
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            if request.form.get('filePath') is None:
                _filePath = ''
            else:
                _filePath = request.form.get('filePath')

            cursor.callproc('sp_addWish',(_title,_description,_filePath))
            data = cursor.fetchall()

            if len(data) is 0:
                mysql.commit()
                return redirect('/showDashboard')
            else:
                return render_template('error.html',error = 'An error occurred!')

            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()

# Not being used but prepared
@app.route('/updateWish', methods=['POST'])
def updateWish():
    try:
        with mysql.cursor() as cursor:
            if session.get('user'):
                _user = session.get('user')
                _title = request.form['title']
                _description = request.form['description']
                _wish_id = request.form['id']
                _filePath = request.form['filePath']
                _isPrivate = request.form['isPrivate']
                _isDone = request.form['isDone']


                conn = mysql.connect()
                cursor.callproc('sp_updateWish',(_title,_description,_wish_id,_user,_filePath,_isPrivate,_isDone))
                data = cursor.fetchall()

                if len(data) is 0:
                    conn.commit()
                    return json.dumps({'status':'OK'})
                else:
                    return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})
    finally:
        cursor.close()
        conn.close()

@app.route('/login',methods=['POST','GET'])
def validateLogin():
    if request.method == 'POST':
        usernameInput = request.form['username']
        passwordInput = request.form['password']

        if usernameInput == 'admin' and passwordInput == 'qaz123':
            return redirect(url_for('welcome'))  

    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


if __name__ == "__main__":
    app.run(debug=True, port=5002)
