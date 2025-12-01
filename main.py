import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from datetime import datetime

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'

# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('reservations.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

def get_seating_chart():
    seating_chart = [['O'] * 4 for _ in range(12)]
    
    db = get_db_connection()
    
    seats = db.execute('SELECT seatRow, seatColumn FROM reservations').fetchall()
    
    for seat in seats:
        row = seat[0]
        col = seat[1]
        
        seating_chart[row - 1][col - 1] = 'X'
        
    db.close()
        
    return seating_chart
    

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
        seating_chart = get_seating_chart()
        return render_template('reservations.html', seats = seating_chart)
    
    
    return render_template('index.html')


# route to display admin page
@app.route('/admin')
def admin():
    chart = get_seating_chart()
    return render_template('admin.html', chart_to_display = chart)

# route to handle admin page logic
@app.route('/admin', methods = ('POST',))
def admin_post():
    return render_template('admin.html')

# route to display reservations page
@app.route('/reservations')
def reservations():
    seating_chart = get_seating_chart()
    return render_template('reservations.html', seats=seating_chart)

# route to handle seat reservation request
@app.route('/reservations', methods = ("POST", ))
def reservations_post():
    # get information from reservations page and create variables to send to function
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    row = int(request.form.get('row'))
    seat = int(request.form.get('seat'))
    eticket_num = create_eticket_num(first_name)
    created = datetime.now()
    
    text_to_display = []
    
    current_chart = get_seating_chart()
    if current_chart[row - 1][seat - 1] == 'X':
        text_to_display.append(f"Row {row}, seat {seat} is already taken. Please select another seat.")
        return render_template('reservations.html', seats=current_chart, text_to_display = text_to_display)
    
    
    # insert into database
    try:
        conn = get_db_connection()
        sql_query = """
            INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber, created) 
            VALUES (?, ?, ?, ?, ?);
            """
        conn.execute(sql_query, (first_name, row, seat, eticket_num, created))
        conn.commit()
        
    except sqlite3.Error as e:
        flash(f"A database error occurred: {e}", "error")
        return redirect(url_for('reservations'))
    
    finally:
        if conn:
            conn.close()
    
    # set the text to display
    text_to_display.append(f"Congralutions {first_name}! Row {row}, seat {seat} is now reserved for you. Enjoy your trip!")
    text_to_display.append(f"Your eticket number is: {eticket_num}")
    
    
    # get new chart and display it
    seating_chart = get_seating_chart()
    
    return render_template('reservations.html', seats=seating_chart, text_to_display = text_to_display)

app.run(port=5004)