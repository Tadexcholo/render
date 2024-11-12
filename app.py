from flask import Flask, render_template, request, jsonify, make_response
import pusher
import mysql.connector
import datetime
import pytz

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    "host": "185.232.14.52",
    "database": "u760464709_tst_sep",
    "user": "u760464709_tst_sep_usr",
    "password": "dJ0CIAFF="
}

# Ruta de inicio
@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Código para notificar actualizaciones
def notificarActualizacionTemperaturaHumedad():
    pusher_client = pusher.Pusher(
        app_id='1869080',
        key='cdcefdd16aec9a6423e7',
        secret='5d8e0749eed8b7b71f31',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger("canalRegistrosTemperaturaHumedad", "registroTemperaturaHumedad", {})

@app.route("/buscar")
def buscar():
    try:
        con = mysql.connector.connect(**db_config)
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT Id_Curso_Pago, Telefono, Archivo 
            FROM tst0_cursos_pagos
            ORDER BY Id_Curso_Pago DESC
            LIMIT 10 OFFSET 0
        """)
        registros = cursor.fetchall()
        return make_response(jsonify(registros))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return make_response(jsonify({"error": str(err)}), 500)
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

@app.route("/guardar", methods=["POST"])
def guardar():
    try:
        con = mysql.connector.connect(**db_config)
        cursor = con.cursor()
        id = request.form.get("id")
        telefono = request.form.get("telefono")
        archivo = request.form.get("archivo")
        
        if id:
            sql = """
            UPDATE tst0_cursos_pagos SET
            Telefono = %s,
            Archivo = %s
            WHERE Id_Curso_Pago = %s
            """
            val = (telefono, archivo, id)
        else:
            sql = """
            INSERT INTO tst0_cursos_pagos (Telefono, Archivo)
            VALUES (%s, %s)
            """
            val = (telefono, archivo)

        cursor.execute(sql, val)
        con.commit()
        notificarActualizacionTemperaturaHumedad()
        return make_response(jsonify({"success": True}), 200)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        con.rollback()
        return make_response(jsonify({"error": str(err)}), 500)
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

@app.route("/editar", methods=["GET"])
def editar():
    try:
        con = mysql.connector.connect(**db_config)
        cursor = con.cursor(dictionary=True)
        id = request.args.get("id")
        sql = """
        SELECT Id_Curso_Pago, Telefono, Archivo FROM tst0_cursos_pagos
        WHERE Id_Curso_Pago = %s
        """
        val = (id,)
        cursor.execute(sql, val)
        registros = cursor.fetchall()
        return make_response(jsonify(registros))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return make_response(jsonify({"error": str(err)}), 500)
    finally:
        if con.is_connected():
            cursor.close()
            con.close()

@app.route("/eliminar", methods=["POST"])
def eliminar():
    try:
        con = mysql.connector.connect(**db_config)
        cursor = con.cursor()
        id = request.form["id"]
        sql = """
        DELETE FROM tst0_cursos_pagos
        WHERE Id_Curso_Pago = %s
        """
        val = (id,)
        cursor.execute(sql, val)
        con.commit()
        notificarActualizacionTemperaturaHumedad()
        return make_response(jsonify({"success": True}), 200)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        con.rollback()
        return make_response(jsonify({"error": str(err)}), 500)
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
