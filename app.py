from flask import Flask, request, render_template, redirect, url_for
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)

# External PostgreSQL connection URL
DB_URL = "postgresql://mydatabase_8cun_user:xUw8BZ8swteQRj6HK1XycFfEhqZFbUw5@dpg-cq578p5ds78s73ct5dk0-a.oregon-postgres.render.com/mydatabase_8cun"

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            age INTEGER
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('form'))

@app.route('/users')
def users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT name, email, age FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('user.html', users=users)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
