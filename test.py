from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
pymysql.install_as_MySQLdb()

app = Flask (__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Lor0-420'
app.config['MYSQL_DB'] = 'flask'

def get_db_connection():
    return pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

@app.route('/')
def Index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM CLIENTES')
    datac = cur.fetchall()
    return render_template('index.html', CLIENTES = datac)

if __name__ == '__main__':
    app.run(port = 3000, debug = True)