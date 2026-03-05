from flask import Flask, render_template, request, redirect
import mysql.connector
from db import conectar
app = Flask(__name__)
#READ

@app.route('/')
def index():
    #Se realiza la conexion a la base de datos
    mi_conexion = conectar()
    cursor = mi_conexion.cursor(dictionary=True)
    
    # Capturamos los filtros de la URL si la URL es por ejemplo ?=talla o ?=marca
    talla_f = request.args.get('talla')
    marca_f = request.args.get('marca')
    
    #Consulta base con el JOIN para ver el nombre de la marca
    orden_sql = "SELECT p.*, m.nombre_marca FROM poleras p JOIN marcas m ON p.id_marca = m.id_marca"

    #Filtros simples (Si llega talla, filtra por talla. Si llega marca, filtra por marca)
    if talla_f:
        orden_sql += f" WHERE p.talla = '{talla_f}'"
    elif marca_f:
        orden_sql += f" WHERE p.id_marca = {marca_f}"
    #Ejecutamos la consulta SQL y actualizamos todos los datos
    cursor.execute(orden_sql)
    lista_de_poleras = cursor.fetchall()
    
    #Ejecutamos la consulta SQL y actualizamos todos los datos
    cursor.execute("SELECT * FROM marcas")
    lista_marcas = cursor.fetchall()
    #Cerramos conexion
    cursor.close()
    mi_conexion.close()
    #Renderizamos en el html
    return render_template('index.html', 
                           poleras=lista_de_poleras, 
                           marcas=lista_marcas, 
                           talla_activa=talla_f, 
                           marca_activa=marca_f)

    
#CREATE

@app.route('/agregar')
def vista_agregar():
    #Se realiza la conexion a base de datos
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    
    #Ejecutamos la consulta SQL y agarramos todas las marcas para que el cliente seleccione en el formulario de agregado
    cursor.execute("SELECT * FROM marcas")
    lista_marcas = cursor.fetchall()
    #Cerramos conexion
    cursor.close()
    conexion.close()
    #Renderizamos en el html
    return render_template('create.html', marcas=lista_marcas)

#Agregar con boton a la base de datos
@app.route('/guardar_polera', methods=['POST'])
def guardar():
    #Se toma del create.html y guardamos en variables
    desc = request.form['txtDescripcion']
    talla = request.form['txtTalla']
    precio = request.form['txtPrecio']
    stock = request.form['txtStock']
    marca = request.form['txtMarca']
    
    #Realizamos la conexion a base de datos
    conexion = conectar()
    cursor = conexion.cursor()
    #Insertamos en la base de datos con una cadena de orden sql y con los datos que guardamos en variables
    orden_sql = "INSERT INTO poleras (descripcion, talla, precio, stock, id_marca) VALUES (%s, %s, %s, %s, %s)"
    datos = (desc, talla, precio, stock, marca)
    #Ejecutamos la consulta SQL e insertamos en la base de datos
    cursor.execute(orden_sql, datos)
    conexion.commit()
    #Cerramos conexion
    cursor.close()
    conexion.close()
    
    #Volvemos a la pestaña principal
    return redirect('/')


#DELETE

#Saca el id desde la URL y lo uso como parametro de mi funcion
@app.route('/confirmar_eliminar/<int:id>')
def vista_eliminar(id):
    #Se realiza la conexion a base de datos
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    
    #Se hace un SELECT para mostrar la info antes de borrar
    consulta = """
        SELECT p.id_polera, p.descripcion, p.talla, p.precio, m.nombre_marca 
        FROM poleras p 
        JOIN marcas m ON p.id_marca = m.id_marca 
        WHERE p.id_polera = %s
    """
    #Ejecutamos la consulta SQL y seleccionamos los datos a mostrar para confirmar la eliminacion, solo mostramos ese unico
    cursor.execute(consulta, (id,))
    polera_datos = cursor.fetchone()
    #Cerramos conexion
    cursor.close()
    conexion.close()
    #Renderizamos en el html
    return render_template('delete.html', p=polera_datos)
#Borrar con boton de la base de datos
@app.route('/ejecutar_eliminar', methods=['POST'])
def eliminar():
    #Saca el ID de el delete tomando el id del delete.html
    id_a_borrar = request.form['txtID']
    #Se realiza la conexion a base de datos
    conexion = conectar()
    cursor = conexion.cursor()
    
    #Ejecutamos la consulta SQL y eliminamos el dato que seleccionamos
    cursor.execute("DELETE FROM poleras WHERE id_polera = %s", (id_a_borrar,))
    #Cerramos conexion
    conexion.commit()
    conexion.close()
    #Volvemos a la pagina principal
    return redirect('/')


#UPDATE


#Volvemos a sacar el id de la URL
@app.route('/editar/<int:id>')
def vista_editar(id):
    #Se realiza la conexion a base de datos
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    
    #Ejecutamos la consulta SQL y mostramos todos los datos de la polera a actualizar
    cursor.execute("SELECT * FROM poleras WHERE id_polera = %s", (id,))
    polera_actual = cursor.fetchone()
    
    #Leemos las marcas para que solo pueda seleccionar las existentes en el formulario
    cursor.execute("SELECT * FROM marcas")
    lista_marcas = cursor.fetchall()
    #Cerramos conexion
    cursor.close()
    conexion.close()
    
    #Renderizamos en el html
    return render_template('update.html', p=polera_actual, marcas=lista_marcas)

@app.route('/ejecutar_actualizar', methods=['POST'])
def actualizar():
    # Recibimos los datos desde update.html
    id_p = request.form['txtID']
    desc = request.form['txtDescripcion']
    talla = request.form['txtTalla']
    precio = request.form['txtPrecio']
    stock = request.form['txtStock']
    marca = request.form['txtMarca']
    #Se realiza la conexion a base de datos
    conexion = conectar()
    cursor = conexion.cursor()
    
    #La consulta SQL para actualizar las lista
    orden_sql = """
        UPDATE poleras 
        SET descripcion=%s, talla=%s, precio=%s, stock=%s, id_marca=%s 
        WHERE id_polera=%s
    """
    datos = (desc, talla, precio, stock, marca, id_p)
    #Ejecutamos la consulta SQL y se actualiza el producto
    cursor.execute(orden_sql, datos)
    conexion.commit()
    #Cerramos conexion
    cursor.close()
    conexion.close()
    #Volvemos a la pagina principal
    return redirect('/')

#Comando para correr el codigo
if __name__ == '__main__':
    app.run(debug=True)
