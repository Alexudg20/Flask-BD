from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
pymysql.install_as_MySQLdb()

app = Flask (__name__)

# MYSQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'ItemPlus'

# settings
app.secret_key = 'myllave'

if __name__ == '__main__':
    app.run(port = 3000, debug = True)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM CLIENTES')
    datac = cur.fetchall()
    cur.execute('SELECT * FROM PEDIDOS')
    datape = cur.fetchall()
    cur.execute('SELECT * FROM PRODUCTOS')
    datapro = cur.fetchall()
    cur.execute('SELECT * FROM CATEGORIAS')
    datacat = cur.fetchall()
    cur.execute('SELECT * FROM ALMACENES')
    datalm = cur.fetchall()
    cur.execute('SELECT * FROM PROVEEDOR')
    datapr = cur.fetchall()
    cur.execute('SELECT * FROM TRANSACCIONES')
    datatr = cur.fetchall()
    return render_template('index.html', CLIENTES = datac, PEDIDOS = datape, PRODUCTOS = datapro, CATEGORIAS = datacat, ALMACENES = datalm, PROVEEDOR = datapr, TRANSACCIONES = datatr)

@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        ID_CLIENTE = request.form['ID_CLIENTE']
        NOMBRE = request.form['NOMBRE']
        CONTACTO = request.form['CONTACTO']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO CLIENTES (ID_CLIENTE, NOMBRE, CONTACTO) VALUES (%s, %s, %s)',
        (ID_CLIENTE, NOMBRE, CONTACTO))
        mysql.connection.commit()
        flash('Alta exitosa')

        return redirect(url_for('Index'))
    
@app.route('/add_pedido', methods=['POST'])
def add_pedido():
    if request.method == 'POST':
        ID_PEDIDO = request.form['ID_PEDIDO']
        CLIENTE = request.form['CLIENTE']
        FECHAP = request.form['FECHAP']
        IDP = request.form['IDP']
        CANTIDAD = request.form['CANTIDAD']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO PEDIDOS (ID_PEDIDO, CLIENTE, FECHAP, IDP,  CANTIDAD) VALUES (%s, %s, %s, %s, %s)',
        (ID_PEDIDO, CLIENTE, FECHAP, IDP, CANTIDAD))
        mysql.connection.commit()
        flash('Alta exitosa')

        return redirect(url_for('Index'))
    
@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        ID_PRODUCTO = request.form['ID_PRODUCTO']
        DESCRIPCION = request.form['DESCRIPCION']
        PRECIO = request.form['PRECIO']
        IDCAT = request.form['IDCAT']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO PRODUCTOS (ID_PRODUCTO, DESCRIPCION, PRECIO, IDCAT) VALUES (%s, %s, %s, %s)',
        (ID_PRODUCTO, DESCRIPCION, PRECIO, IDCAT))
        mysql.connection.commit()
        flash('Alta exitosa')

        return redirect(url_for('Index'))

@app.route('/edit/<string:ID_CLIENTE>')
def get_client(ID_CLIENTE):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM CLIENTES WHERE ID_CLIENTE = {0}'.format (ID_CLIENTE))
    data = cur.fetchall()
    return render_template('edit-cliente.html', Cliente = data[0])

@app.route('/update/<string:ID_CLIENTE>', methods= ['POST'])
def update_client(ID_CLIENTE):
    if request.method == 'POST':
        NOMBRE = request.form['NOMBRE']
        CONTACTO = request.form['CONTACTO']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE CLIENTES
            SET NOMBRE = %s,
                CONTACTO = %s
            WHERE ID_CLIENTE = %s           
        """, (NOMBRE, CONTACTO, ID_CLIENTE))
        mysql.connection.commit()
        flash('Cliente actualizado')
        return redirect(url_for('Index'))

@app.route('/delete/<string:ID_CLIENTE>')
def delete_client(ID_CLIENTE):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM CLIENTES WHERE ID_CLIENTE = {0}'.format(ID_CLIENTE))
    mysql.connection.commit()
    flash('Cliente eliminado')
    return redirect(url_for('Index'))

