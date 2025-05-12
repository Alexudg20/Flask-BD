import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
pymysql.install_as_MySQLdb()

app = Flask (__name__)

app.config['SECRET_KEY'] = os.urandom(24)

app.config['MYSQL_HOST'] = os.environ.get('DB_HOST')
app.config['MYSQL_USER'] = os.environ.get('DB_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('DB_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('DB_NAME')
app.config['MYSQL_PORT'] = int (os.environ.get('DB_PORT', 3306))

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        port=app.config['MYSQL_PORT']
)

@app.route('/login', methods =['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT username, password from users where username = '{username}'")
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and pwd == user[1]:
            session['username'] = user [0]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Usuario o password incorrectos')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
    
        cursor.execute(f"INSERT INTO users (username, password) VALUES (%s, %s)", (username, pwd))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/Index')
def Index():
    limit = 10
    page_clientes = max(request.args.get('clientes_page', 1, type = int), 1)
    page_pedidos = max(request.args.get('pedidos_page', 1, type = int), 1)
    page_productos = max(request.args.get('productos_page', 1, type = int), 1)
    page_categorias = max(request.args.get('categorias_page', 1, type = int), 1)
    page_almacenes = max(request.args.get('almacenes_page', 1, type = int), 1)

    conn = get_db_connection()
    cur = conn.cursor()

    #1
    offset_clientes = (page_clientes - 1) * limit
    cur.execute('SELECT COUNT(*) FROM CLIENTES')
    total_clientes = cur.fetchone()[0]
    total_clientes_pages = (total_clientes +  limit -1) // limit
    cur.execute('SELECT * FROM CLIENTES LIMIT %s OFFSET %s', (limit, offset_clientes))
    datac = cur.fetchall()

    #2
    offset_pedidos = (page_pedidos - 1) * limit
    cur.execute('SELECT COUNT(*) FROM PEDIDOS')
    total_pedidos = cur.fetchone()[0]
    total_pedidos_pages = (total_pedidos +  limit -1) // limit
    cur.execute('SELECT * FROM PEDIDOS LIMIT %s OFFSET %s', (limit, offset_pedidos))
    datape = cur.fetchall()

    #3
    offset_productos = (page_productos - 1) * limit
    cur.execute('SELECT COUNT(*) FROM PRODUCTOS')
    total_productos = cur.fetchone()[0]
    total_productos_pages = (total_productos +  limit -1) // limit
    cur.execute('SELECT * FROM PRODUCTOS LIMIT %s OFFSET %s', (limit, offset_productos))
    datapro = cur.fetchall()

    #4
    offset_categorias = (page_categorias - 1) * limit
    cur.execute('SELECT COUNT(*) FROM CATEGORIAS')
    total_categorias = cur.fetchone()[0]
    total_categorias_pages = (total_categorias +  limit -1) // limit
    cur.execute('SELECT * FROM CATEGORIAS LIMIT %s OFFSET %s', (limit, offset_categorias))
    datacat = cur.fetchall()

    #5
    offset_almacenes = (page_almacenes - 1) * limit
    cur.execute('SELECT COUNT(*) FROM ALMACENES')
    total_almacenes = cur.fetchone()[0]
    total_almacenes_pages = (total_almacenes +  limit -1) // limit
    cur.execute('SELECT * FROM ALMACENES LIMIT %s OFFSET %s', (limit, offset_almacenes))
    datalm = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('index.html', 
    CLIENTES = datac, PEDIDOS = datape, PRODUCTOS = datapro, CATEGORIAS = datacat, ALMACENES = datalm,
    page_clientes=page_clientes, total_clientes_pages=total_clientes_pages, 
    page_pedidos=page_pedidos, total_pedidos_pages= total_pedidos_pages,
    page_productos=page_productos, total_productos_pages=total_productos_pages,
    page_categorias=page_categorias, total_categorias_pages=total_categorias_pages,
    page_almacenes=page_almacenes, total_almacenes_pages=total_almacenes_pages
)


###CLIENTE

##ADD

@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        ID_CLIENTE = request.form['ID_CLIENTE']
        NOMBRE = request.form['NOMBRE']
        CONTACTO = request.form['CONTACTO']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO CLIENTES (ID_CLIENTE, NOMBRE, CONTACTO) VALUES (%s, %s, %s)',
        (ID_CLIENTE, NOMBRE, CONTACTO))

        connection.commit()
        cursor.close()
        connection.close()
        flash('Alta exitosa')

        return redirect(url_for('Index'))

##UPDATE

@app.route('/edit/<id_cliente>', methods=['GET'])
def edit_cliente(id_cliente):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM CLIENTES WHERE ID_CLIENTE = %s", (id_cliente))
        cliente = cursor.fetchone()
    return render_template ('edit-cliente.html', Cliente = cliente)

@app.route('/update_CLIENTE/<string:ID_CLIENTE>', methods= ['POST'])
def update_client(ID_CLIENTE):
    if request.method == 'POST':
        NOMBRE = request.form['NOMBRE']
        CONTACTO = request.form['CONTACTO']
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("""
            UPDATE CLIENTES
            SET NOMBRE = %s,
                CONTACTO = %s
            WHERE ID_CLIENTE = %s           
        """, (NOMBRE, CONTACTO, ID_CLIENTE))
        connection.commit()
        cur.close()
        connection.close()
        flash('Cliente actualizado')
        return redirect(url_for('Index'))

##DELETE

@app.route('/delete_cliente/<string:ID_CLIENTE>')
def delete_client(ID_CLIENTE):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("DELETE FROM CLIENTES WHERE ID_CLIENTE = %s", (ID_CLIENTE,))
    connection.commit()
    cur.close()
    connection.close()
    flash('Cliente eliminado')
    return redirect(url_for('Index'))

###PEDIDOS

##ADD

@app.route('/add_pedido', methods=['POST'])
def add_pedido():
    if request.method == 'POST':
        ID_PEDIDO = request.form['ID_PEDIDO']
        CLIENTE = request.form['CLIENTE']
        CONTACTO = request.form['FECHAP']
        IDP = request.form['IDP']
        CANTIDAD = request.form['CANTIDAD']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO PEDIDOS (ID_PEDIDO, CLIENTE, FECHAP, IDP, CANTIDAD) VALUES (%s, %s, %s, %s, %s)',
        (ID_CLIENTE, NOMBRE, CONTACTO))

        connection.commit()
        cursor.close()
        connection.close()
        flash('Alta exitosa')

        return redirect(url_for('Index'))

##UPDATE

@app.route('/edit_pedido/<id_pedido>', methods=['GET'])
def edit_pedido(id_pedido):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PEDIDOS WHERE ID_PEDIDO = %s", (id_pedido))
        pedido = cursor.fetchone()
    return render_template ('edit-pedido.html', PEDIDO = pedido)

@app.route('/update_PEDIDO/<string:ID_PEDIDO>', methods= ['POST'])
def update_pedido(ID_CLIENTE):
    if request.method == 'POST':
        CLIENTE = request.form['CLIENTE']
        FECHAP = request.form['FECHAP']
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("""
            UPDATE PEDIDOS
            SET CLIENTE = %s,
                FECHAP = %s
            WHERE ID_PEDIDO = %s           
        """, (CLIENTE, FECHAP, CANTIDAD))
        connection.commit()
        cur.close()
        connection.close()
        flash('Pedido actualizado')
        return redirect(url_for('Index'))

##DELETE

@app.route('/delete_pedido/<string:ID_PEDIDO>')
def delete_pedido(ID_PEDIDO):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("DELETE FROM PEDIDOS WHERE ID_PEDIDO = %s", (ID_PEDIDO,))
    connection.commit()
    cur.close()
    connection.close()
    flash('Pedido eliminado')
    return redirect(url_for('Index'))


###PRODUCTOS

##ADD

@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        ID_PRODUCTO = request.form['ID_PRODUCTO']
        DESCRIPCION = request.form['DESCRIPCION']
        PRECIO = request.form['PRECIO']
        IDCAT = request.form['IDCAT']
        CANTIDAD = request.form['CANTIDAD']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO PRODUCTO (ID_PRODUCTO, DESCRIPCION, PRECIO, IDCAT, CANTIDAD) VALUES (%s, %s, %s, %s, %s)',
        (ID_PRODUCTO, DESCRIPCION, PRECIO, IDCAT, CANTIDAD))

        connection.commit()
        cursor.close()
        connection.close()
        flash('Alta exitosa')

        return redirect(url_for('Index'))

##UPDATE

@app.route('/edit_producto/<id_productos>', methods=['GET'])
def edit_producto(id_producto):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PRODUCTOS WHERE ID_PRODUCTO = %s", (id_producto))
        pedido = cursor.fetchone()
    return render_template ('edit-pedido.html', PRODUCTO = producto)

@app.route('/update_PRODUCTO/<string:ID_PRODUCTO>', methods= ['POST'])
def update_producto(ID_PRODUCTO):
    if request.method == 'POST':
        PRODUCTO = request.form['PRODUCTO']
        ID_PRODUCTO = request.form['ID_PRODUCTO']
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("""
            UPDATE PRODUCTOS
            SET PRODUCTO = %s,
                ID_PRODUCTO = %s
            WHERE ID_PRODUCTOS = %s           
        """, (ID_PRODUCTO, DESCRIPCION, PRECIO, IDCAT, CANTIDAD))
        connection.commit()
        cur.close()
        connection.close()
        flash('Producto actualizado')
        return redirect(url_for('Index'))

##DELETE

@app.route('/delete_producto/<string:ID_PRODUCTO>')
def delete_producto(ID_PRODUCTO):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("DELETE FROM PRODUCTOS WHERE ID_PRODUCTO = %s", (ID_PRODUCTO,))
    connection.commit()
    cur.close()
    connection.close()
    flash('PRODUCTO eliminado')
    return redirect(url_for('Index'))


###CATEGORIAS

##ADD

@app.route('/add_categoria', methods=['POST'])
def add_categoria():
    if request.method == 'POST':
        ID_CATEGORIA = request.form['ID_CATEGORIA']
        DESCRIPCION = request.form['NOMBRECAT']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO CATEGORIAS (ID_CATEGORIA, NOMBRECAT) VALUES (%s, %s)',s
        (ID_CATEGORIA, NOMBRECAT))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Alta exitosa')

        return redirect(url_for('Index'))

##UPDATE

@app.route('/edit/<id_categoria>', methods=['GET'])
def edit_categoria(id_categoria):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM CATEGORIAS WHERE ID_PRODUCTO = %s", (id_categoria))
        pedido = cursor.fetchone()
    return render_template ('edit-pedido.html', CATEGORIA = categoria)

@app.route('/update_categoria/<string:ID_CATEGORIA>', methods= ['POST'])
def update_categoria(ID_CATEGORIA):
    if request.method == 'POST':
        ID_CATEGORIA = request.form['ID_CATEGORIA']
        NOMBRECAT = request.form['NOMBRECAT']
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("""
            UPDATE CATEGORIAS
            SET CATEGORIA = %s,
                ID_CATEGORIA = %s
            WHERE ID_CATEGORIA = %s           
        """, (ID_CATEGORIA, NOMBRECAT))
        connection.commit()
        cur.close()
        connection.close()
        flash('Categoria actualizada')
        return redirect(url_for('Index'))

##DELETE

@app.route('/delete_categoria/<string:ID_CATEGORIA>')
def delete_categoria(ID_CATEGORIA):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("DELETE FROM CATEGORIAS WHERE ID_CATEGORIA = %s", (ID_CATEGORIA,))
    connection.commit()
    cur.close()
    connection.close()
    flash('Categoria eliminada')
    return redirect(url_for('Index'))


###ALMACEN

##ADD

@app.route('/add_almacen', methods=['POST'])
def add_almacen():
    if request.method == 'POST':
        ID_ALMACEN = request.form['ID_ALMACEN']
        UBICACION = request.form['UBICACION']
        CAPACIDAD = request.form['CAPACIDAD']
        ID_PRODUCTO = request.form['ID_PRODUCTO']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO ALMACENES (ID_ALMACEN, UBICACION, CAPACIDAD , ID_PRODUCTO) VALUES (%s, %s, %s, %s)',
        (ID_ALMACEN, UBICACION, CAPACIDAD , ID_PRODUCTO))

        connection.commit()
        cursor.close()
        connection.close()
        flash('Alta exitosa')

        return redirect(url_for('Index'))

##UPDATE

@app.route('/edit/<id_almacen>', methods=['GET'])
def edit_almacen(id_producto):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM ALMACENES WHERE ID_ALMACEN = %s", (id_almacen))
        pedido = cursor.fetchone()
    return render_template ('edit-almacen.html', ALMACEN = almacen)

@app.route('/update_ALMACEN/<string:ID_PRODUCTO>', methods= ['POST'])
def update_almacen(ID_ALMACEN):
    if request.method == 'POST':
        ALMACEN = request.form['ALMACEN']
        ID_ALMACEN = request.form['ID_ALMACEN']
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("""
            UPDATE ALMACENES
            SET ALMACEN = %s,
                ID_ALMACEN = %s
            WHERE ALMACENES = %s           
        """, (ID_ALMACEN, UBICACION, CAPACIDAD , ID_PRODUCTO))
        connection.commit()
        cur.close()
        connection.close()
        flash('Almacen actualizado')
        return redirect(url_for('Index'))

##DELETE

@app.route('/delete/<string:ID_ALMACEN>')
def delete_almacen(ID_ALMACEN):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("DELETE FROM ALMACENES WHERE ID_ALMACEN = %s", (ID_ALMACEN,))
    connection.commit()
    cur.close()
    connection.close()
    flash('Almacen eliminado')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3306)# debug = True)