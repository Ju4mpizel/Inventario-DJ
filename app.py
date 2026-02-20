from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# --- PASO 1: LA CONEXIÓN ---
# Esta función es como "marcar el número" de la base de datos.
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345", 
        database="inventario_dj"
    )

# --- PASO 2: LA RUTA PRINCIPAL ---
@app.route('/')
def index():
    # Abrimos la conexión
    mi_conexion = conectar()
    # El cursor es como un "carrito" que va a la base de datos y trae datos
    cursor = mi_conexion.cursor(dictionary=True)
    
    # Leemos qué botón de talla presionó el usuario (si es que presionó alguno)
    talla_que_llega = request.args.get('talla')
    
    # Esta es la orden que le daremos a la base de datos (SQL)
    # Usamos JOIN para traer el nombre de la marca desde la otra tabla
    orden_sql = "SELECT p.id_polera, p.descripcion, p.talla, p.precio, p.stock, m.nombre_marca FROM poleras p JOIN marcas m ON p.id_marca = m.id_marca"

    # --- PASO 3: LA LÓGICA DEL FILTRO (S-M-L) ---
    # Si el usuario mandó una talla, cambiamos la orden de "traer todo" a "filtrar"
    if talla_que_llega == 'S':
        orden_sql = orden_sql + " WHERE p.talla = 'S'"
    elif talla_que_llega == 'M':
        orden_sql = orden_sql + " WHERE p.talla = 'M'"
    elif talla_que_llega == 'L':
        orden_sql = orden_sql + " WHERE p.talla = 'L'"
    
    # Ejecutamos la orden en MySQL
    cursor.execute(orden_sql)
    
    # Guardamos los resultados en una lista llamada 'lista_de_poleras'
    lista_de_poleras = cursor.fetchall()
    
    # Cerramos el carrito y la conexión (siempre hay que cerrar)
    cursor.close()
    mi_conexion.close()
    
    # --- PASO 4: MANDAR TODO AL HTML ---
    # Le pasamos la lista y también la talla que estaba activa para que el HTML sepa qué hacer
    return render_template('index.html', poleras=lista_de_poleras, talla_activa=talla_que_llega)

if __name__ == '__main__':
    app.run(debug=True)