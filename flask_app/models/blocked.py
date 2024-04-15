from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

phone = re.compile(r"^[0-9]{10}")

class Blocked:
    def __init__(self,data):
        self.phone_number = data['phone_number']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @staticmethod
    def validate_blocked(user):
        valid = True
        if len(user['phone_number']) < 1:
            flash('Phone number can not be blank')
            valid = False
        if not phone.match(user['phone_number']):
            flash("Phone Number needs to be 10 digits long")
            valid = False
        if len(user['comment']) < 1:
            flash("Comment can not be blank.")
            valid = False
        return valid


        

    @classmethod
    def your_blocked(cls, data):
        query = "INSERT INTO blocked(phone_number, comment, user_id) VALUES(%(phone_number)s, %(comment)s, %(user_id)s)"
        results = connectToMySQL('blacklist').query_db(query, data)
        return results