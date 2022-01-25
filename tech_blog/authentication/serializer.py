from rest_framework import serializers
from .models import AuthenticationKeys
from technology.models import Technology
from responses.models import Responses
from responses.serializer import ResponsesSerializer


class AuthenticationKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationKeys
        # fields = ['id',  'title', 'description', 'file_path', 't_id', 'responses']
        fields = "__all__"
