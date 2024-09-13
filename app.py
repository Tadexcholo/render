from flask import Flask

from flask import render_template
from flask import request
import pusher
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"];
    nombreapellido = request.form["txtNombreApellidoFA"];
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"
@app.route("/evento")
def evento():
    pusher_client = pusher.Pusher(
        app_id='1767944',
        key='93408f3e56875b1bb947',
        secret='fd213855fc0b2521c437',
        cluster='us2',
        ssl=True
    )

pusher_client.trigger('conexion', 'evento', {'message': 'hello world'})
