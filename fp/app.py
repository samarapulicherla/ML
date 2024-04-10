from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
import pickle
import numpy as np
import os

app = Flask(__name__)
secret_key = os.urandom(24)
app.secret_key = secret_key  
m = pickle.load(open('xgboost.pkl', 'rb'))

def create_table():
    conn = sqlite3.connect('signup.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            mobile TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('index1'))
    else:
        return render_template('login.html')

@app.route('/registerform', methods=["GET",'POST'])
def registerform():
    if request.method=='POST':
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']

        conn = sqlite3.connect('signup.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (fullname, username, email, mobile, password)
                VALUES (?, ?, ?, ?, ?)
            ''', (fullname, username, email, mobile, password))
            conn.commit()
            conn.close()
            return render_template('login.html')
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register_form.html', error="Username or email already exists")
    else:
        return render_template('register_form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('signup.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM users WHERE email = ? AND password = ?
        ''', (email, password))
        data = cursor.fetchone()
        conn.close()

        if data is None:
            return render_template("register_form.html", error="Invalid email or password")    

        email == str(data[0]) and password == str(data[1])
        return redirect(url_for('index1'))
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/make_prediction', methods=['POST'])
def make_prediction():
    
    int_features = [int(float(x)) for x in request.form.values()]
    pre_final_features = [np.array(int_features)]
    prediction = m.predict(pre_final_features)
    
    if prediction[0] == 1:
        output = "Demented"
    elif prediction[0] == 2:
        output = "NonDemented"
    else:
        output = "Converted"

    return render_template('predict.html', prediction_text='The person is affected by {}'.format(output))

    if 'user_id' not in session:
        return redirect(url_for('login'))


@app.route('/about_dementia')
def about_dementia():
    return render_template('about_dementia.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/index1')
def index1():
    return render_template('index1.html')

@app.route('/precautions')
def precautions():
    return render_template('precautions.html')

@app.route('/precautions1')
def precautions1():
    return render_template('precautions1.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')


if __name__ == "__main__":
    app.run(debug=True)
