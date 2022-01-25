import smtplib
import string
import random  # define the random module
# from app.models_package.models import User
# from app.utils.form_validation import password_validator
# from app import app
# from flask import jsonify
import re


def password_validator(password):
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$', password):
        if 8 <= len(password) <= 16:
            return True
    else:
        return False


def generate_temp_password_and_check():
    S = 8  # number of characters in the string.
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    password = str(''.join(random.choices(alphabet, k=S)))
    if not password_validator(password):
        # print("Generated Password is not satisfying")
        print(password)
        return generate_temp_password_and_check()
    print(password)
    # print("Generated Password is satisfying")
    return password
