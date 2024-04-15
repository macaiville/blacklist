from flask_app.models.users import User
from flask_app.models.verified_guest import Vguest
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template("login_page.html")

@app.route('/home')
def home():
    if len(session) < 1:
        return redirect('/')
    data = Vguest.get_all_guest(session['user_id'])
    return render_template("home.html", data = data)

@app.route('/create_user')
def new_user():
    return render_template('register.html')

@app.route('/new/user', methods=['POST'])
def create():
    if not User.new_user_validation(request.form):
        return redirect('/create_user')
    
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pw)

    new_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw
    }
    print(new_data)
    User.add_new_user(new_data)

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    email_data = {"email": request.form['email']}
    print(email_data)
    user = User.get_by_email(email_data)
    print(user)
    if not user:
        flash('Invalid Email or password')
        return redirect('/')

    check_pw = bcrypt.check_password_hash(user['password'], request.form['password'])
    if not check_pw:
        flash('Invalid Email or password')
        return redirect('/')
    
    session['user_id'] = user['id']
    session['first_name'] = user['first_name']
    session['last_name'] = user['last_name']

    return redirect('/home')

