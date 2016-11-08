from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongologinexample'

mongo = PyMongo(app)
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('admin'))

    return render_template('index.html')

@app.route('/admin')
def admin():
    users = mongo.db.users
    userlist = users.find({})
    userSession = users.find_one({'username': session['username']})
    return render_template('admin.html', userlist=userlist, userSession=userSession)

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
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_username = users.find_one({'username': request.form['username']})

        if existing_username is None:
            existing_email = users.find_one({'email': request.form['email']})
            
            if existing_email is None:
                users.insert({'fullname': request.form['fullname'], 'email': request.form['email'], 'username': request.form['username'], 'password': request.form['pass'] })
                return redirect(url_for('index'))
            return 'Email Already exists'
        return 'That username already exists'

def create_app():
    return app
