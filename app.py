from flask import Flask, render_template, request, redirect
import mysql.connector
from db import conectar
app = Flask(__name__)
#READ
@app.route('/')
def index():
    mi_conexion = conectar()
    cursor = mi_conexion.cursor(dictionary=True)
    
    # Capturamos los filtros de la URL
    talla_f = request.args.get('talla')
    marca_f = request.args.get('marca')
    
    # Consulta base con el JOIN para ver el nombre de la marca
    orden_sql = "SELECT p.*, m.nombre_marca FROM poleras p JOIN marcas m ON p.id_marca = m.id_marca"

    # Filtros simples (Si llega talla, filtra por talla. Si llega marca, filtra por marca)
    if talla_f:
        orden_sql += f" WHERE p.talla = '{talla_f}'"
    elif marca_f:
        orden_sql += f" WHERE p.id_marca = {marca_f}"
    
    cursor.execute(orden_sql)
    lista_de_poleras = cursor.fetchall()
    
    # Necesitamos las marcas para dibujar los botones
    cursor.execute("SELECT * FROM marcas")
    lista_marcas = cursor.fetchall()
    
    cursor.close()
    mi_conexion.close()
    
    return render_template('index.html', 
                           poleras=lista_de_poleras, 
                           marcas=lista_marcas, 
                           talla_activa=talla_f, 
                           marca_activa=marca_f)

    
#CREATE
# RUTA PARA MOSTRAR EL FORMULARIO DE AGREGAR
@app.route('/agregar')
def vista_agregar():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    
    # Necesitamos traer las marcas de la base de datos para que el usuario elija una
    cursor.execute("SELECT * FROM marcas")
    lista_marcas = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    return render_template('create.html', marcas=lista_marcas)

# RUTA PARA GUARDAR LA POLERA (Esta no se ve, solo procesa)
@app.route('/guardar_polera', methods=['POST'])
def guardar():
    # 1. Recogemos los datos que vienen del formulario
    desc = request.form['txtDescripcion']
    talla = request.form['txtTalla']
    precio = request.form['txtPrecio']
    stock = request.form['txtStock']
    marca = request.form['txtMarca']
    
    # 2. Conectamos y guardamos
    conexion = conectar()
    cursor = conexion.cursor()
    
    orden_sql = "INSERT INTO poleras (descripcion, talla, precio, stock, id_marca) VALUES (%s, %s, %s, %s, %s)"
    datos = (desc, talla, precio, stock, marca)
    
    cursor.execute(orden_sql, datos)
    conexion.commit() # Guarda los cambios
    
    cursor.close()
    conexion.close()
    
    # 3. Volvemos al inicio para ver la polera nueva en la lista
    return redirect('/')

# RUTA 1: Para ver la ventana de confirmación (GET)
@app.route('/confirmar_eliminar/<int:id>')
def vista_eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    
    # Buscamos la polera con un JOIN para mostrar la marca también
    consulta = """
        SELECT p.id_polera, p.descripcion, p.talla, p.precio, m.nombre_marca 
        FROM poleras p 
        JOIN marcas m ON p.id_marca = m.id_marca 
        WHERE p.id_polera = %s
    """
    cursor.execute(consulta, (id,))
    polera_datos = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    return render_template('delete.html', p=polera_datos)

# RUTA 2: Para borrar físicamente de la base de datos (POST)
@app.route('/ejecutar_eliminar', methods=['POST'])
def eliminar():
    id_a_borrar = request.form['txtID']
    
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Orden SQL para borrar el registro
    cursor.execute("DELETE FROM poleras WHERE id_polera = %s", (id_a_borrar,))
    
    conexion.commit() # ¡Obligatorio para que MySQL guarde el cambio!
    conexion.close()
    
    return redirect('/')


# 1. RUTA PARA MOSTRAR EL FORMULARIO CON DATOS CARGADOS
@app.route('/editar/<int:id>')
def vista_editar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    
    # Buscamos la polera específica por su ID
    cursor.execute("SELECT * FROM poleras WHERE id_polera = %s", (id,))
    polera_actual = cursor.fetchone()
    
    # Traemos las marcas para que el usuario pueda cambiarla si quiere
    cursor.execute("SELECT * FROM marcas")
    lista_marcas = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    # Mandamos los datos a la página update.html
    return render_template('update.html', p=polera_actual, marcas=lista_marcas)

# 2. RUTA PARA PROCESAR EL CAMBIO (UPDATE)
@app.route('/ejecutar_actualizar', methods=['POST'])
def actualizar():
    # Recibimos el ID oculto y los nuevos datos
    id_p = request.form['txtID']
    desc = request.form['txtDescripcion']
    talla = request.form['txtTalla']
    precio = request.form['txtPrecio']
    stock = request.form['txtStock']
    marca = request.form['txtMarca']
    
    conexion = conectar()
    cursor = conexion.cursor()
    
    # La orden de SQL para actualizar
    orden_sql = """
        UPDATE poleras 
        SET descripcion=%s, talla=%s, precio=%s, stock=%s, id_marca=%s 
        WHERE id_polera=%s
    """
    datos = (desc, talla, precio, stock, marca, id_p)
    
    cursor.execute(orden_sql, datos)
    conexion.commit() # ¡Importante!
    
    cursor.close()
    conexion.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

#DELETE