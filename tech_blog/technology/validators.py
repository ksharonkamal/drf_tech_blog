from rest_framework import serializers


def validate_name(name):
    if len(name) > 10:
        raise serializers.ValidationError('Name Invalid')
    return name
