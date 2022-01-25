from rest_framework import serializers


def validate_description(description):
    if 2 < len(description) <= 1000:
        return description
    return serializers.ValidationError(["Description too long or too short"])
