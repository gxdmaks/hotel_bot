import sqlite3
from datetime import datetime

connection = sqlite3.connect('hotel.db')
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users(tg_id INTEGER, name TEXT, phone_number TEXT,reg_date DATETIME);')
sql.execute('CREATE TABLE IF NOT EXISTS room(room_id INTEGER PRIMARY KEY AUTOINCREMENT , room_name INTEGER, room_price REAL, room_quantity INTEGER, room_des DATETIME, room_photo TEXT, room_reg_date DATETIME);')
sql.execute('CREATE TABLE IF NOT EXISTS busy_room(tg_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, user_room TEXT, quantity INTEGER, total_for_room REAL);')

def register_user(tg_id, name, phone_number):
    connection = sqlite3.connect('hotel.db')
    sql = connection.cursor()
    sql.execute('INSERT INTO users '
                '(tg_id, name, phone_number, reg_date) VALUES'
                '(?, ?, ?, ?);', (tg_id, name, phone_number, datetime.now()))

    connection.commit()

def check_user(user_id):
    connection = sqlite3.connect('hotel.db')
    sql = connection.cursor()
    checker = sql.execute('SELECT tg_id FROM users WHERE tg_id=?;', (user_id, ))
    if checker.fetchone():
        return True

    else:
        return False

def dob_user(room_name, room_price, room_quantity, room_des, room_photo):
    connection = sqlite3.connect('hotel.db')
    sql = connection.cursor()
    sql.execute('INSERT INTO room '
                '(room_name, room_price, room_quantity, room_des, room_photo) VALUES'
                '(?, ?, ?, ?, ?);', (room_name, room_price, room_quantity, room_des, room_photo))
    connection.commit()

def delete_exact_user_from_room(room_id, user_id):
    connection = sqlite3.connect('hotel.db')
    sql = connection.cursor()
    sql.execute('DELETE FROM busy_room WHERE user_id=? AND room_id=?;',(user_id,room_id ))
    connection.commit()

def delete_users_from_all_room(user_id):
    connection = sqlite3.connect('hotel.db')
    sql = connection.cursor()
    sql.execute('DELETE FROM busy_room WHERE user_id=?;', (user_id, ))
    connection.commit()

def get_room_name_id():
    connection = sqlite3.connect('hotel.db')
    sql=connection.cursor()
    room = sql.execute('SELECT room_name, room_id, room_quantity FROM room').fetchall()
    sorted_room = [i for i in room if i[2] > 0]
    return sorted_room

def get_exact_room(room_name):
    connection = sqlite3.connect('hotel.db')
    sql=connection.cursor()
    exact_room = sql.execute('SELECT room_photo, room_des, room_price FROM room WHERE room_name=?;', (room_name, )).fetchone()

    return exact_room
def add_room(user_id, user_room, quantity):
    connection = sqlite3.connect('hotel.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO busy_room (user_id, user_room, quantity)'
                'VALUES (?, ?, ?);', (user_id, user_room, quantity))

def get_user_number_name(user_id):
    connection = sqlite3.connect('hotel.db')
    sql = connection.cursor()
    exect_user = sql.execute('SELECT name, phone_number FROM users WHERE tg_id=?;', (user_id,))
    return exect_user.fetchone()

connection.commit()