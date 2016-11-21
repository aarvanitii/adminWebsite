from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
import time

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongologinexample'

mongo = PyMongo(app)
@app.route('/')
def index():

    return render_template('index.html')

#Admin routes

@app.route('/admin')
def admin():
    if 'username' in session:
        users = mongo.db.users
        userSession = users.find_one({'username': session['username']})        
        return render_template('admin.html', userSession=userSession)
    
    return redirect(url_for('login_form'))

@app.route('/admin/<username>', methods=['POST'])
def show_user_profile(username):
    users = mongo.db.users
    userSession = users.find_one({'username': session['username']})
    return render_template('profile.html', userSession=userSession)

#Users routes

@app.route('/admin/users')
def users():
    users = mongo.db.users
    userlist = users.find({})
    userSession = users.find_one({'username': session['username']})
    print(userSession['username'])
    return render_template('users.html', userlist=userlist, userSession=userSession)

@app.route('/delete-user/<username>', methods=['POST'])
def delete_user(username):
    if request.method == 'POST':
        users = mongo.db.users    
        users.remove({'username': username})
        return redirect(url_for('users'))       

@app.route('/change-psw', methods=['GET','POST'])
def change_psw():
    if request.method == 'POST':
        users = mongo.db.users
        userSession = users.find_one({'username': session['username']})
        if request.form['password1'] == userSession['password']:
            if request.form['password2'] == request.form['password3']:
                userSession.update_one('username' == userSession['username'],'password' == request.form['password3'])
                return 'password changed successfuly'
            return 'New password wrong '
        return 'Old password wrong'

#Post/Upload routes

@app.route('/admin/post')
def post():
    posts = mongo.db.posts
    postslist = posts.find({'author': session['username']})    
    return render_template('post.html', postslist=postslist)

@app.route('/upload-post', methods=['POST'])
def upload_post():
    date = time.strftime('%X %x')
    if request.method == 'POST':
        posts = mongo.db.posts
        posts.insert({'title': request.form['title'], 'text': request.form['text'], 'author': session['username'],'date': date})
        return redirect(url_for('post'))
    return render_template('post.html')

@app.route('/delete-post/<title>', methods=['POST'])
def delete_post(title):
    if request.method == 'POST':
        posts = mongo.db.posts    
        posts.remove({'title': title})
        return redirect(url_for('post'))    

@app.route('/posts')
def posts():
    posts = mongo.db.posts
    postslist = posts.find({})    
    return render_template('posts.html', postslist=postslist) 

#Login/Logout routes

@app.route('/login-form')
def login_form():
    if 'username' in session:
        return redirect(url_for('admin'))

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username': request.form['username']})

    if login_user:
        if request.form['pass'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('admin'))

    return 'Invalid Username/Password'

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login_form'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_username = users.find_one({'username': request.form['username']})

        if existing_username is None:
            existing_email = users.find_one({'email': request.form['email']})
            
            if existing_email is None:
                users.insert({'fullname': request.form['fullname'], 'email': request.form['email'], 'username': request.form['username'], 'password': request.form['pass'] })
                return redirect(url_for('users'))
            return 'Email Already exists'
        return 'That username already exists'    

def create_app():
    return app