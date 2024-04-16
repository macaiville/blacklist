from flask_app.models.blocked import Blocked
from flask_app import app
from flask import flash, session, redirect, request, render_template, flash



@app.route('/blocked')
def blocked_page():
    return render_template('blacklist.html')

@app.route('/blocked_for_life', methods=['POST'])
def not_coming_back():
    if not session or len(session) < 1:
        return redirect("/")
    
    if not Blocked.validate_blocked(request.form):
        return redirect('/blocked')
    
    Blocked.your_blocked(request.form)

    return redirect('/home')