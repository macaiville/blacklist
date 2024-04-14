from flask_app.models.users import User
from flask_app import app
from flask import render_template, redirect

@app.route('/')
def login_page():
    return render_template("login_page.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/create_user')
def new_user():
    return render_template('register.html')