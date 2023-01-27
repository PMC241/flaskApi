from flask import Flask, jsonify
import os

app = Flask(__name__)

data = {
    "Comidas": [
        {
            "nombre": "Cazuela", 
            "descripcion": "Deliciosa cazuela preparada con cariño"
        },
        {
            "nombre": "Limon", 
            "descripcion": "Delicioso limon para el rico pescado que vendemos"
        },
        {
            "nombre": "Pescado", 
            "descripcion": "Exquisito corte de pescado marinado en aceite de roble viejo de 40 años"
        }
    ]
} 

@app.route('/test')
def get_drinks():
    return data

@app.route('/')
def index():
    return jsonify({"Choo Chooo": "Bienvenido a la locomotora de python 🚅"})

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"),host='0.0.0.0', port=os.getenv("PORT", default=5000))