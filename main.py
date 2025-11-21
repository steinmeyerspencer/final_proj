import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'

seating_chart = [
    ['O', 'X', 'X', 'O'],
    ['X', 'O', 'O', 'O'],
    ['O', 'O', 'X', 'O'],
    ['X', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'X'],
    ['O', 'X', 'O', 'O'],
    ['O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O'],
    ['O', 'O', 'X', 'O'],
    ['O', 'O', 'O', 'X'],
    ['X', 'O', 'O', 'O'],
    ['X', 'O', 'O', 'O']
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ('POST',))
def index_post():
    page = request.form.get('pageOption')
    
    if page == 'adminLogin':
        return render_template('admin.html')
    elif page == 'reserveSeat':
        return render_template('reservations.html', seats = seating_chart)
    
    
    return render_template('index.html')



@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/reservations')
def reservations():
    
    
    return render_template('reservations.html', seats=seating_chart)



app.run(port=5004)