from flask_app.models.verified_guest import Vguest
from flask_app import app
from flask import request, redirect, session, render_template



@app.route('/add_guest' , methods=["POST"])
def today_guest():
    if len(session) < 1:
        return redirect('/')
    if not Vguest.verified_guest_validations(request.form):
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

    phone = request.form.get('phone_number') 
    data = Vguest.search_vguest(phone)
    return redirect('/search/verified_guest')
