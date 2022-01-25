import re
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ValidationError
# from django.utils.translation import ugettext as _


def validate_username(value):
    if re.match(r'^[ A-Za-z0-9_-]*$', value):
        if 2 < len(value) <= 30:
            return True
        # raise serializers.ValidationError(["Username is too short"])
    # raise serializers.ValidationError(['Invalid username'])
    return False


def validate_email(email):
    if re.match(r'^[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}$', email):
        username = email.split('@')[0]
        domain = email.split('@')[1]
        domain_name = domain.split('.')[0]
        domain_type = domain.split('.')[1]
        if 3 <= len(username) <= 64:
            if 1 <= len(domain_name) <= 30:
                if 1 <= len(domain_type) <= 5:
                    if not "@" in email or not (".com" or ".org" or ".edu" or ".gov" or ".net") in email[-4:]:
                        return False
                    return True
    return False


def validate_password(value: str):
    errors = dict()
    try:
        # validate the password and catch the exception
        validators.validate_password(password=value)
        # the exception raised here is different than serializers.ValidationError
    except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)
    if errors:
        return False
        # raise serializers.ValidationError(errors)
    print(make_password(value))
    return make_password(value)


def validate_mobile(mobile):
    if (re.match(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', mobile) and
            len(mobile) == 10):
        return True
    return False


def validate_firstname(firstname):
    if re.match(r'^([A-Za-z]+)( [A-Za-z]+)*( [A-Za-z]+)*$', firstname):
        if 2 < len(firstname) <= 40:
            return True
    return False


def validate_lastname(lastname):
    if re.match(r'^([A-Za-z]+)( [A-Za-z]+)*( [A-Za-z]+)*$', lastname):
        if 2 < len(lastname) <= 30:
            return True
    return False


# class CustomPasswordValidator():
#
#     def __init__(self, min_length=1):
#         self.min_length = min_length
#
#     def validate(self, password, user=None):
#         special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
#         if not any(char.isdigit() for char in password):
#             raise ValidationError(
#                 _('Password must contain at least %(min_length)d digit.') % {'min_length': self.min_length})
#         if not any(char.isalpha() for char in password):
#             raise ValidationError(
#                 _('Password must contain at least %(min_length)d letter.') % {'min_length': self.min_length})
#         if not any(char.isupper() for char in password):
#             raise ValidationError(
#                 _('Password must contain at least %(min_length)d uppercase letter.') % {'min_length': self.min_length})
#         if not any(char in special_characters for char in password):
#             raise ValidationError(
#                 _('Password must contain at least %(min_length)d special character.') % {'min_length': self.min_length})