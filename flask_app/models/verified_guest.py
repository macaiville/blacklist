from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from datetime import date




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

    @classmethod
    def search_vguest(cls, data):
        data = {
            'phone_number': data
        }
        query = " SELECT * FROM verified_guest WHERE phone_number = %(phone_number)s"
        results = connectToMySQL('blacklist').query_db(query, data)
        print(results)
        if not results or len(results) < 1:
            return False
        return results[0]
    
    @classmethod
    def search_blocked(cls, data):
        data = {
            'phone_number': data
        }
        query = " SELECT * FROM blocked WHERE phone_number = %(phone_number)s"
        results = connectToMySQL('blacklist').query_db(query, data)
        print(results)
        if not results or len(results) < 1:
            return False
        return results[0]
    
    @classmethod
    def get_all_blocked(cls):
        new_list = []
        query = "SELECT * FROM blocked"
        results = connectToMySQL('blacklist').query_db(query)
        for r in results:
            new_list.append(r['phone_number'])

        if not results or len(results) < 1:
            return False
        return new_list
    
    @staticmethod
    def verified_guest_validations(guest):
        blocked = Vguest.get_all_blocked()
        valid = True
        if len(guest['first_name']) < 2:
            flash("First name needs to be at least 2 characters long")
            valid = False
        if len(guest['last_name']) < 2:
            flash("Last name needs to be at least 2 characters long")
            valid = False
        if len(guest['phone_number']) < 1:
            flash("Please enter a Phone Number.")
            valid = False
        if not phone.match(guest['phone_number']):
            flash("Phone number must be 10 Digits long")
            valid = False
        if not guest['date']:
            flash("Please enter a date")
            valid = False
        if guest['phone_number'] in blocked:
            flash("THIS NUMBER AND GUEST IS BLOCKED! PLEASE SEARCH FOR GUEST IN 'SEARCH BLOCKED GUEST' BY PHONE NUMBER TO SEE WHY!")
            valid = False
        return valid
    
    @classmethod
    def search_vguest_by_date(cls, data):
        data = {
            'date': data
        }
        query = " SELECT * FROM verified_guest WHERE date = %(date)s"
        results = connectToMySQL('blacklist').query_db(query, data)
        print(results)
        if not results or len(results) < 1:
            return None
        return results