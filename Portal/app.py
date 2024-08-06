import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_ENDPOINT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please fill in all fields')
            return redirect(url_for('login'))

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM students WHERE email = %s AND password = %s", (email, password))
                student = cursor.fetchone()
        finally:
            conn.close()

        if student:
            session['student_id'] = student[0]
            return redirect(url_for('student_profile'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            flash('Please fill in all fields')
            return redirect(url_for('register'))

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO students (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
                conn.commit()
        finally:
            conn.close()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

from datetime import datetime

@app.route('/profile')
def student_profile():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    student_id = session['student_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    # Format date if necessary
    if student and student[3]:
        try:
            dob = datetime.strptime(student[3], '%Y-%m-%d').strftime('%d-%m-%Y')
        except ValueError:
            dob = student[3]  # Use the original value if formatting fails
    else:
        dob = 'N/A'

    return render_template('profile.html', student=(student[0], student[1], student[2], dob))


@app.route('/logout')
def logout():
    session.pop('student_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
