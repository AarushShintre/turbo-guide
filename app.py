from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'account'
app.config['FLASK_APP'] = "main.py"

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))
# http://localhost:5000/login - the following will be our login page, which will use both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "name" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        # Create variables for easy access
        name = request.form['name']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE name = %s AND password = %s', (name, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in user table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['name'] = account['name']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or name/password incorrect
            msg = 'Incorrect name/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('name', None)
   # Redirect to login page
   return redirect(url_for('login'))


# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "name", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE name = %s', (name,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'name must contain only characters and numbers!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into user table
            cursor.execute('INSERT INTO user VALUES (%s, %s, %s)', (name,email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', name=session['name'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
