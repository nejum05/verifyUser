from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Your db4free MySQL config
db_config = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12780373',
    'password': 'plR7hiKCmt',
    'database': 'sql12780373',
    'port': 3306
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            message = "Registration successful! Please login."
            return redirect('/login')
        except mysql.connector.errors.IntegrityError:
            message = "Username already exists."
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['username'] = username
            return redirect('/')
        else:
            message = "Invalid username or password."

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
