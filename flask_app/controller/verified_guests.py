from flask_app.models.verified_guest import Vguest
from flask_app import app
from flask import request, redirect, session



@app.route('/add_guest' , methods=["POST"])
def today_guest():
    if len(session) < 1:
        return redirect('/')
    if not Vguest.verified_guest_validations(request.form):
        return redirect('/home')

    Vguest.add_guest(request.form)

    return redirect('/home')

