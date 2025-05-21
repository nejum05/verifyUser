from flask import Flask, render_template, request, redirect, session
import mysql.connector
from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production!

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def home():
    return 'Welcome to the User Auth App!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['username'] = username
            return f'Welcome, {username}!'
        else:
            return 'Login failed. Try again.'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
