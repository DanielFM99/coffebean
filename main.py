from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

# Database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'coffebean'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/coffebean/ - Login page
@app.route('/coffebean/', methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        password = request.form['password']
        email    = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesn't exist or username/password are incorrect
            msg = 'Incorrect email/password!'
    return render_template('index.html', msg=msg)

# http://localhost:5000/coffebean/logout - Logout page
@app.route('/coffebean/logout')
def logout():
    # Remove session data
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/coffebean/register - Registration page
@app.route('/coffebean/register', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exists
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        usernameLen = len(username)
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists, show error and validation checks
        if account:
            msg = 'Account already exists!'
        # RegEx for email, back-end validation
        elif not re.match(r"(^[-\w\D][^@]{0,64}@([\w-]+\.)+[\w-]+$)", email):
            msg = 'Invalid email address!'
        elif not (usernameLen >= 5 and usernameLen <= 128):
            msg = 'Invalid username!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        # RegEx for password, back-end validation
        elif not re.match(r"^(?=(?:.*[a-z]))(?=(?:.*[A-Z]){2})(?=(?:.*\d){2})(?=(?:.*[-@!$%^#&*()_+|~={}\[\]:\";`'<>?,.\/\\]){2}).{10,128}$", password):
            msg = 'Invalid password!'
        else:
            # Account doesn't exists and the form is valid
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty
        msg = 'Please fill out the form!'
    # Show registration form with message
    return render_template('register.html', msg=msg)

# http://localhost:5000/coffebean/home - Home page
@app.route('/coffebean/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'], email=session['email'],)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/coffebean/profile - Profile page
@app.route('/coffebean/profile')
def profile():
    if 'loggedin' in session:
        # Get session data
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))