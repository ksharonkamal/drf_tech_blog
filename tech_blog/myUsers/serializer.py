from rest_framework import serializers
from .models import CustomUser
from technology.serializer import TechnologySerializer
from technology.models import Technology
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import SlugRelatedField
import django.contrib.auth.password_validation as validators
from django.core import exceptions
import re
from .validators import validate_email, validate_lastname, validate_firstname,validate_mobile, validate_password, validate_username


class UserSerializer(serializers.ModelSerializer):
    technology = SlugRelatedField(many=True, slug_field='name', read_only=True)
    # technology = TechnologySerializer(many=True, read_only=True)
    print("technology: ", technology)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'mobile', 'firstname', 'lastname', 'technology', 'password']
        # fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if 'username' not in self.initial_data.keys() or (not data.get('username')):
            raise serializers.ValidationError({'username': 'username is required field.'})
        if CustomUser.objects.filter(username=data.get('username')).exists():
            msg = "username with {} already exists".format(data.get('username'))
            raise serializers.ValidationError(msg)
        if not validate_username(data.get('username')):
            msg = "{} invalid username".format(data.get('username'))
            raise serializers.ValidationError(msg)

        if 'email' not in self.initial_data.keys() or (not data.get('email')):
            raise serializers.ValidationError({'email': 'email is required field.'})
        if CustomUser.objects.filter(email=data.get('email')).exists():
            msg = "email with {} already exists".format(data.get('email'))
            raise serializers.ValidationError(msg)
        if not validate_email(data.get('email')):
            msg = "email with {} already exists".format(data.get('email'))
            raise serializers.ValidationError(msg)

        if 'password' not in self.initial_data.keys() or (not data.get('password')):
            raise serializers.ValidationError({'password': 'password is required field.'})
        password_test = validate_password(data.get('password'))
        if not password_test:
            msg = "Invalid password"
            raise serializers.ValidationError(msg)
        else:
            data['password'] = password_test

        if 'firstname' not in self.initial_data.keys() or (not data.get('firstname')):
            raise serializers.ValidationError({'username': 'firstname is required field.'})
        if not validate_firstname(data.get('firstname')):
            msg = "{} invalid firstname".format(data.get('firstname'))
            raise serializers.ValidationError(msg)

        if 'lastname' not in self.initial_data.keys() or (not data.get('lastname')):
            raise serializers.ValidationError({'lastname': 'lastname is required field.'})
        if not validate_lastname(data.get('lastname')):
            msg = "{} invalid lastname".format(data.get('lastname'))
            raise serializers.ValidationError(msg)

        if 'mobile' not in self.initial_data.keys() or (not data.get('mobile')):
            raise serializers.ValidationError({'mobile': 'mobile is required field.'})
        if CustomUser.objects.filter(mobile=data.get('mobile')).exists():
            msg = "mobile with {} already exists".format(data.get('mobile'))
            raise serializers.ValidationError(msg)
        if not validate_mobile(data.get('mobile')):
            msg = "{} invalid mobile number".format(data.get('mobile'))
            raise serializers.ValidationError(msg)
        return data




    # def create(self, validated_data):
    #     tracks_data = validated_data.pop('technology')
    #     album = CustomUser.objects.create(**validated_data)
    #     for track_data in tracks_data:
    #         Technology.objects.create(album=album, **track_data)
    #     return album


    # def create(self, validated_data):
    #     technology_data = validated_data.pop("technology")
    #     user = CustomUser.objects.create(**validated_data)
    #     for tech_data in technology_data:
    #         Technology.objects.create(artist=artist, song= ** song_data)
    #         return artist

