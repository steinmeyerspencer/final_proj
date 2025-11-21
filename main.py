import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from datetime import datetime

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

# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('reservations.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

def create_eticket_num(first_name):
    infotc_string = 'INFOTC4320'
    
    # find the length of the shorter word
    min_length = min(len(first_name), len(infotc_string))
    
    eticket_num = ''
    
    # loop as far as the shorter allows to avoid adding nulls
    for i in range(min_length):
        eticket_num += first_name[i]
        eticket_num += infotc_string[i]
        
    # append whatever is leftover from the longer string
    eticket_num += first_name[min_length:]
    eticket_num += infotc_string[min_length:]
    
    return eticket_num
    

# route to display index page
@app.route('/')
def index():
    return render_template('index.html')

# route to handle logic from when the page is selected
@app.route('/', methods = ('POST',))
def index_post():
    page = request.form.get('pageOption')
    
    if page == 'adminLogin':
        return render_template('admin.html')
    elif page == 'reserveSeat':
        return render_template('reservations.html', seats = seating_chart)
    
    
    return render_template('index.html')


# route to display admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

# route to handle admin page logic
@app.route('/admin', methods = ('POST',))
def admin_post():
    return render_template('admin.html')

# route to display reservations page
@app.route('/reservations')
def reservations():
    
    return render_template('reservations.html', seats=seating_chart)

# route to handle seat reservation request
@app.route('/reservations', methods = ("POST", ))
def reservations_post():
    # get information from reservations page and create variables to send to function
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    row = request.form.get('row')
    seat = request.form.get('seat')
    eticket_num = create_eticket_num(first_name)
    created = datetime.now()
    
    # set the text to display
    text_to_display = []
    text_to_display.append(f"Congralutions {first_name}! Row {row}, seat {seat} is now reserved for you. Enjoy your trip!")
    text_to_display.append(f"\nYour eticket number is: {eticket_num}")
    text_to_display.append(f"\ndb: {first_name} {last_name} {row} {seat} {eticket_num} {created}")
    
    # to do: set the seating chart to the actual stuff from the database.
        # update seating chart after reservation goes through
            # should be handled by sending to database
        # send reservation to database
        # update css for text input boxes
        
    
    return render_template('reservations.html', seats=seating_chart, text_to_display = text_to_display)

app.run(port=5004)