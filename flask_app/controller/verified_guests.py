from flask_app.models.verified_guest import Vguest
from flask_app import app
from flask import request, redirect, session, render_template, flash
from datetime import date


@app.route('/add_guest' , methods=["POST"])
def today_guest():
    c_date = date.today()
    if len(session) < 1:
        return redirect('/')
    if not Vguest.verified_guest_validations(request.form):
        return redirect('/home')
    
    if not request.form['date'] == c_date:
        flash("Date Needs to be Today's date!")
        return redirect('/home')
    
    Vguest.add_guest(request.form)
    
    return redirect('/home')

@app.route('/delete/<int:id>')
def delete_guest(id):
    if len(session) < 1:
        return redirect('/')
    
    Vguest.delete_guest(id)

    return redirect('/home')

@app.route('/search/verified_guest')
def search_verified():
    return render_template('search.html')

@app.route('/search_vguest', methods=['POST'])
def search_vguest():
    if len(session) < 1:
        return redirect('/')

    phone_number = request.form.get('phone_number') 
    data = Vguest.search_vguest(phone_number)
    return render_template('search.html', data = data)

@app.route('/search/blocked')
def search_blocked():
    return render_template('blocked.html')

@app.route('/search_blocked', methods=['POST'])
def search_no_entry():
    if len(session) < 1:
        return redirect('/')

    phone_number = request.form.get('phone_number') 
    data = Vguest.search_blocked(phone_number)
    return render_template('blocked.html', data = data)

@app.route('/search_vguest_date', methods=['POST'])
def search_vguest_date():
    if len(session) < 1:
        return redirect('/')

    date = request.form.get('date') 
    all = Vguest.search_vguest_by_date(date)
    return render_template('search.html', all = all)
