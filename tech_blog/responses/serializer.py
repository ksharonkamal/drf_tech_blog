from rest_framework import serializers
from .models import Responses
from technology.models import Technology
from .validators import validate_description


class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responses
        # fields = ['id','name','email','phone','technology']
        fields = "__all__"
        extra_kwargs = {'u_id': {'read_only': True}}

        def validate(self, data):
            if 'description' not in self.initial_data.keys() or (not data.get('description')):
                raise serializers.ValidationError({'description': 'description is required field.'})
            # if Responses.objects.filter(description=data.get('description')).exists():
            #     msg = "description with {} already exists".format(data.get('description'))
            #     raise serializers.ValidationError(msg)
            if not validate_description(data.get('description')):
                msg = "invalid description"
                raise serializers.ValidationError(msg)
