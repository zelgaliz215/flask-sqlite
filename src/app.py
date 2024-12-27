from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "claversupersecreta"


@app.route('/')
@app.route('/inicio')
def home():
    return render_template('index.html')

# Crear bd sqlite si no existe
def initDb():
    # conexion a una bd en el disco
    con = sqlite3.connect("src/db/tutorial.db")
    # cursor para ejecutar sentencias sql
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefono TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
    con.commit()
    con.close()


# Funcion para ver susuarios
@app.route('/usuarios')
def usuarios():
    con = sqlite3.connect("src/db/tutorial.db")
    con.row_factory = sqlite3.Row 
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    # print(users)
    con.close()
    return render_template('usuarios.html', users=users)

# Añadir usuario
@app.route('/create_usuario', methods=['GET','POST'])
def create_user():
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        con = sqlite3.connect("src/db/tutorial.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, telefono) VALUES (?,?,?)",(nombre, email, telefono))
        con.commit()
        con.close()
        # Redirigir a la lista de usuarios después de insertar
        return redirect(url_for('usuarios'))
    return render_template('crear-usuario.html')


# Eliminar usuario
@app.route('/delete_usuario/<int:id>', methods=['GET'])
def delete_user(id):
    con = sqlite3.connect("src/db/tutorial.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect(url_for('usuarios'))

# EDitar usuario
@app.route('/edit_usuario/<int:id>', methods=['GET','POST'])
def edit_user(id):
    con = sqlite3.connect("src/db/tutorial.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    # Recibe el formulario diligenciado a travez de un POST
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        cursor.execute("UPDATE usuarios SET nombre=?, email=?, telefono=? WHERE id=?", (nombre, email, telefono, id))
        con.commit()
        con.close()
        return redirect(url_for('usuarios'))
    
    # Obtener los datos del usuario para mostrarlos en el formulario de edicion
    cursor.execute("SELECT * FROM usuarios WHERE id=?", (id,))
    user = cursor.fetchone()
    con.close()
    return render_template('editar_usuario.html', user=user)

if __name__ == '__main__':
    initDb()  # Crear bd si no existe antes de iniciar la app
    app.run(debug=True, host="0.0.0.0", port=5000)
