from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

phone = re.compile(r"^[0-9]{10}")

class Vguest:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone_number = data['phone_number']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    
    @staticmethod
    def verified_guest_validations(Vguest):
        valid = True
        if len(Vguest['first_name']) < 2:
            flash("First name needs to be at least 2 characters long")
            valid = False
        if len(Vguest['last_name']) < 2:
            flash("Last name needs to be at least 2 characters long")
            valid = False
        if len(Vguest['phone_number']) < 1:
            flash("Please enter a Phone Number.")
            valid = False
        if not phone.match(Vguest['phone_number']):
            flash("Phone number must be 10 Digits long")
            valid = False
        if not Vguest['date']:
            flash("Please enter a date")
            valid = False
        return valid
    
    @classmethod
    def add_guest(cls, data):
        query = "INSERT INTO verified_guest(first_name, last_name, phone_number, date, user_id) VALUES(%(first_name)s, %(last_name)s, %(phone_number)s, %(date)s, %(user_id)s)"
        results = connectToMySQL('blacklist').query_db(query, data)
        return results
    
    @classmethod
    def get_all_guest(cls, data):
        data = {
            "users_id": session['user_id']
        }
        query = "SELECT * FROM verified_guest LEFT JOIN users ON user_id = %(users_id)s"
        results = connectToMySQL('blacklist').query_db(query, data)
        from_the_bottom = []
        for dictionary in reversed(results):
            from_the_bottom.append(dictionary)
        if not results or len(results) < 1:
            return False
        return from_the_bottom
    
    @classmethod
    def delete_guest(cls, data):
        data = {
            'id': data
        }
        query = "DELETE FROM verified_guest WHERE id = %(id)s"
        results = connectToMySQL('blacklist').query_db(query, data)
        return results