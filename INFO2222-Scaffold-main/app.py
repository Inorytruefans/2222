'''
app.py contains all of the server application
this is where you'll find all of the get/post request handlers
the socket event handlers are inside of socket_routes.py
'''

import sqlite3
import hashlib
from flask import Flask, render_template, request, abort, url_for, make_response
from flask_socketio import SocketIO
import db
import secrets

# import logging

# this turns off Flask Logging, uncomment this to turn off Logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)

# secret key used to sign the session cookie
app.config['SECRET_KEY'] = secrets.token_hex()
socketio = SocketIO(app)

# don't remove this!!
import socket_routes




# index page
@app.route("/")
def index():
    return render_template("index.jinja")

# login page
@app.route("/login")
def login():    
    return render_template("login.jinja")

# handles a post request when the user clicks the log in button
@app.route("/login/user", methods=["POST"])
def login_user():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    user =  db.get_user(username)
    if user is None:
        return "Error: User does not exist!"
    
    if user and db.verify_password(password, user.password, user.salt):
        #use cookie to store user info
        response = make_response(url_for('home', username=request.json.get("username")))
        response.set_cookie('username', username)
        return response
    
        #display the friend list
    


    else:
        return "Error: Password does not match!"

# handles a get request to the signup page
@app.route("/signup")
def signup():
    return render_template("signup.jinja")

# handles a post request when the user clicks the signup button
@app.route("/signup/user", methods=["POST"])
def signup_user():
    if not request.is_json:
        abort(404)
    username = request.json.get("username")
    password = request.json.get("password")
    
    if db.get_user(username) is None:
        db.insert_user(username, password)
        return url_for('home', username=username)

    if db.get_user(username):    
        return "Error: User already exists!"
    
    
# show the friend list page
def friends():
    username = request.cookies.get('username')
    friend_list = db.get_friends(username)
    return render_template('friends.jinja', friend_list=friend_list)

# !remember make a html for friend list - done
# !and for friend username - done
# no logout feature to clean the cookies - dono if need to do

# add friend page
def add_friend():
    username = request.cookies.get('username')
    friend_username = request.json.get["friend_username"]
    friend = db.get_user(friend_username)
    if friend:
        send_friend_request(username, friend_username)
        return "Request sent"
    else:
        return "User does not exist"
    
    

# handler when a "404" error happens
@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.jinja'), 404

# home page, where the messaging app is
@app.route("/home")
def home():
    if request.args.get("username") is None:
        abort(404)
    return render_template("home.jinja", username=request.args.get("username"))



if __name__ == '__main__':
    socketio.run(app)
