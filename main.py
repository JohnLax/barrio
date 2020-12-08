from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, logging
from flask_login import logout_user
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os

NKeys = [
    "Db0nOi6ocaoKwOhFDQAL",
    "OBlYJ7Y7DYyY1k8ObM03",
    "N6scrg5heJndhtmcoJCb",
    "OCOTUQ9pbgD5yUs1dXVJ",
    "FL9S8ZMSXA5BZjELYXKH",
    "VtQ8PaXBuvcOJxO4YBSK",
    "LEBPYXpH6Nm35V0hasuj",
    "YfgLH77WiVeFKXF9wfo5",
    "M12PO2x1ple0r3AkHsGq",
    "2GlVcd3PNef53i858oga",
    "6Hv4ItsARTao288jMtAK",
    "000RpqgbvvurAFAdSgCU",
    "TZH0u7vYaYVZ152tI9Jr",
    "ZRKiaBae9r9t0S4TgpWp",
    "D6aOSttelgAX2pwY00HX",
    "SuZgUE5c2j6aVJaYpNfj",
    "MPsosICrLok3fJTR6i56",
    "OHIPlr7nd4SDkedlraef",
    "XMkRivt3XhEaiAXnlOhA",
    "YSQtQTTTL1fR5MjchGCK",
    "PbuTCchOZhOPjskbLLnI",
    "UqidBaZ07PMs9iUdKo6t",
    "M1sgJvhU1WQ05WQWoMTP",
    "Fa2IG4Uk83HhtCS6L4ya",
    "ZboF2HeJ6HVhRMEJoIi7",
    "Q8TawRLVjV1pwsWB3AMG",
    "JFcMMTqqA6BHCaxmPdWQ",
    "7YxHseZb0M9LW2kybAjp",
    "YlXC7KJSNXli9oeAG1la",
    "AkhbnfXF8U1LfYZoQjSW",
    "PyMcRfNbmZoxkZM0lSti",
    "5XwjFiPYNTotdSxYFktQ",
    "H48sYNLkDRYtcwdtc3EN",
    "FhJ4kWWGxLg2OKx9fH5y",
    "WshiJuBLSKH82n0MWksW",
    "EGF7kNrOXpm68g1Q0LD7",
    "W294kR3HUobVedhe0D0S",
    "PIllcoE2NyaXdeyLeusr",
    "0sOWelfWeo0xZtfag1lp",
    "MwjKkID8PdcgXI4vRuYy",
    "YK132ZjkxtU9Yq0lcEv8",
    "DotvZTcwvi2DvIUD5dbH",
    "CfVc6Twar0RjwVwbfFi4",
    "TqtrtqbfM9hpKy9PXiHp",
    "25gpviUCnxpOcG8TXBKn",
    "26CNeOa4WnDe8cqbrf10",
    "Nu9Lb3VSZQ8x7GPoyba8",
    "75GDCtBYOGIoYCQ5isVG",
    "YxfKYiVIEXF79DxN6MQ4",
    "YtRFU0pJPGT51ueSIp2N",
    "UA4BOA35cI3PDNUpQVGy",
    "Bc32DHys5pVleFE4kqYJ",
    "Ro2ZWT2aen50ngpasVbG",
    "0skInZx278gOCPmWUu8C",
    "8GvANtUJc4QEi4w8viJN",
    "5oxDrLGlB2wylmvyNB50",
    "8DwdFZcncLOi6UnGAOJ8",
    "8aXfkIQHoqypmMlFleCt",
    "64kIxalMfnmMfmaklBVQ",
    "BKjc0yJjIG2a4o37e2S4",
]


app = Flask(__name__)
picFolder = os.path.join('static', 'pics')
print(picFolder)
app.config['UPLOAD_FOLDER'] = picFolder
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'SolaresAdminMySql'
app.config['MYSQL_PASSWORD'] = 'vJ50V1C6ypFkVNmD'
app.config['MYSQL_DB'] = 'barrio'

# Intialize MySQL
mysql = MySQL(app)
@app.route('/')
def index():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'pic1.png')
    return render_template("index.html", user_image=pic1)   
# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        if username == 'Administracion':
            if password == '1234':
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('admin'))
            else:
                msg = 'El usuario o la contraseña es incorrecta!'
        if username == 'Seguridad':
            if password == '1234':
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('control'))
            else:
                msg = 'El usuario o la contraseña es incorrecta!'
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'El usuario o la contraseña es incorrecta!'
    return render_template('index.html', msg=msg)


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        key = request.form['clavekey']
        cargo = '2'
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', [username])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if key in NKeys:
            if account:
                msg = 'La cuenta ya existe!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'El email no es valido!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'El usuario que contenga numero y caracteres!'
            elif not username or not password or not email:
                msg = 'Por favor rellene el formulario!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cursor.execute('INSERT INTO accounts (username, password, email, clavekey, id_cargo) VALUES (%s, %s, %s, %s, %s)', (username, password, email, key, cargo))
                mysql.connection.commit()
                msg = 'Se ah registrado correctamente!'
        else:
            msg = 'La clave no es valida!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Por favor rellene el formulario!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  

@app.route('/controlsystem/')
def control():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('control.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  

@app.route('/adminsystem/')
def admin():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('admin.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login')) 


if __name__ == '__main__':
    app.run(port=3000, debug=True)