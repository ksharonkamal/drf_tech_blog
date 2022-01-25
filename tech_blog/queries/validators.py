from rest_framework import serializers


def validate_title(title):
    if 2 < len(title) <= 100:
        return title
    return serializers.ValidationError(["Title too long or too short"])


def validate_description(description):
    if 2 < len(description) <= 1000:
        return description
    return serializers.ValidationError(["Description too long or too short"])
