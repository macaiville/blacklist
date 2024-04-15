import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

email_regex = re.compile(r"^[a-zA-Z0-9\.\-_]+@{1}[a-zA-Z0-9]+\.{1}[a-zA-Z]{2,5}$")
password_re = re.compile(r"^[a-zA-Z0-9]+[^a-zA-Z0-9]{1}")

class User:
    def __init__(self,data) -> None:
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def new_user_validation(User):
        valid = True
        if len(User['first_name']) < 2:
            flash("First name needs to be at least 2 characters long")
            valid = False
        if len(User['last_name']) < 2:
            flash("Last name needs to be at least 2 characters long")
            valid = False
        if not email_regex.match(User['email']):
            flash('Invalid Email Address')
            valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s"
            email_in_use = connectToMySQL("blacklist").query_db(query, User)
            if email_in_use:
                flash("Email Already in use.")
                valid = False
        if len(User['email']) < 1:
            flash("Email can't be blank")
        if not password_re.match(User['password']):
            flash('Password need to be 8 characters long and have a special character.')
            valid = False
        if len(User['password']) < 8:
            flash('Password need to be 8 characters')
            valid = False
        if not User['password'] == User['confirm_password']:
            flash("Your Passwords Don't Match")
            valid = False
        return valid
        
    @classmethod
    def add_new_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        results = connectToMySQL("blacklist").query_db(query, data)
        return results
    
    @classmethod
    def get_by_email(cls ,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL("blacklist").query_db(query, data)
        if not results or len(results) < 1:
            return False
        return results[0]