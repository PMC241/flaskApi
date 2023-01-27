from flask import Flask, current_app, render_template, request, redirect, url_for, session, jsonify
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__) 
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'holakeHace'

app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

# Intialize MySQL
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'usuario' in request.form and 'password' in request.form:
        # Create variables for easy access
        usuario = request.form['usuario']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s AND password = %s', (usuario, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            app.logger.info('%s Ha ingresado el usuario: ', usuario)
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['usuario'] = account['usuario']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Contraseña o Usuario incorrecto!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out                                       
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('usuario', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'usuario' in request.form and 'password' in request.form and 'correo' in request.form:
        # Create variables for easy access
        usuario = request.form['usuario']
        password = request.form['password']
        correo = request.form['correo']

    # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s', (usuario,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Este usuario ya se encuentra registrado!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
            msg = 'Direccion de correo invalida!'
        elif not re.match(r'[A-Za-z0-9]+', usuario):
            msg = 'El usuario solo puede tener letras y numeros!'
        elif not usuario or not password or not correo:
            msg = 'Porfavor Ingresa datos en el formulario!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO cuentas VALUES (NULL, %s, %s, %s)', (usuario, password, correo,))
            mysql.connection.commit()
            msg = 'Te has registrado con exito!'


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Porfavor Ingresa datos en el formulario!'
    # Show registration form with message (if any)
    return render_template('registro.html', msg=msg)

@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', usuario=session['usuario'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/perfil')
def perfil():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuentas WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('perfil.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

health_status = True

@app.route('/toggle')
def toggle():
    global health_status
    health_status = not health_status
    return jsonify(health_value=health_status)


@app.route('/healthcheck')
def health():
    if health_status:
        resp = jsonify(health="vivo")
        resp.status_code = 200
    else:
        resp = jsonify(health="muerto")
        resp.status_code = 500

    return resp

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"),host='0.0.0.0', port=os.getenv("PORT", default=5000))