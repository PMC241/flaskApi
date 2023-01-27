from flask import Blueprint, request, jsonify, session
from flask_mysqldb import MySQL


api = Blueprint('api', __name__)

@api.route('/api/login', methods=['POST'])
def apiLogin():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.is_json:
    # Get data from json
        data = request.get_json()
        usuario = data.get('usuario')
        password = data.get('password')
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s AND password = %s', (usuario, password,))
        
        cuenta = cursor.fetchone()
    # If account exists in accounts table in out database
    if cuenta:
        api.logger.info('%s Ha ingresado el usuario: ', usuario)
        # Create session data, we can access this data in other routes
        session['loggedin'] = True
        session['id'] = cuenta['id']
        session['usuario'] = cuenta['usuario']
        # Return success message
        return jsonify(success=True, mensaje='Inicio de sesión exitoso', usuario=cuenta)
    else:
        # Account doesnt exist or username/password incorrect
        return jsonify(success=False, mensaje='Usuario o contraseña incorrecta')