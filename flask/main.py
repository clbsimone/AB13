import socket as sck
import AlphaBot
import time
import sqlite3
from flask import Flask, render_template, redirect, url_for, make_response, request

app = Flask(__name__, static_url_path='/static')

SEPARATOR = ';'
SEPARATOR_DB = '-'

r = AlphaBot.AlphaBot()

def playMov(command, duration):
    if command.lower() == 'b':
        r.backward()
        time.sleep(duration)
        r.stop()
    elif command.lower() == 'f':
        r.forward()
        time.sleep(duration)
        r.stop()
    elif command.lower() == 'r':
        r.right()
        time.sleep(duration)
        r.stop()
    elif command.lower() == 'l':
        r.left()
        time.sleep(duration)
        r.stop()
    else:
        cDb(command)

def check_password(hashed_password, user_password):
    return hashed_password == user_password

def validate(username, password):
    completion = False
    with sqlite3.connect('./db.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[0]
            dbPass = row[1]
            if dbUser == username:
                completion = check_password(dbPass, password)

    return completion

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            if username== "simone":
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('username', 'simone')
                return resp
            elif username == "zorro":
                resp = make_response(redirect(url_for('zorro')))
                resp.set_cookie('username', 'zorro')
                return resp
            else:
                #settare il cookie
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('username', 'utentegenerico')
                return resp
    return render_template('login.html', error=error)

def commandHistory(user, command):
    with sqlite3.connect('./db.db') as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO COMMAND_HISTORY(user, command, date, time) VALUES ('{user}', '{command}', CURRENT_DATE, CURRENT_TIME)")

@app.route('/index', methods=['GET', 'POST'])  
def index():
    user = request.cookies.get('username');
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'f':
            playMov('f',1)
            commandHistory(user, 'f;1')
        elif action == 'b':
            playMov('b', 1)
            commandHistory(user, 'b;1')
        elif action == 'r':
            playMov('r',1)
            commandHistory(user, 'r;1')
        elif action == 'l':
            playMov('l',1)
            commandHistory(user, 'l;1')
        else:
            print("Unknown command")

    return make_response(render_template("index.html"))

@app.route('/zorro', methods=['GET', 'POST'])  
def zorro():
    return make_response(render_template("zorro.html"))


def cDb(command):
    q = f"SELECT MovSequence FROM TABLE_MOVEMENTS WHERE Shortcut = '{command.lower()}'"

    movSeq = curDb.execute(q)

    ms = movSeq.fetchall()

    if(len(ms) == 0):
        playMov('f', 0)
    else:
        cList = str(ms[0][0]).split(SEPARATOR_DB)
        
        for mov in cList:
            playMov(mov.split(SEPARATOR)[0], float(mov.split(SEPARATOR)[1]))

def main():
    app.run(debug=True, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
