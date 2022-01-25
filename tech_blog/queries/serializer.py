from rest_framework import serializers
from .models import Queries
from technology.models import Technology
from responses.models import Responses
from responses.serializer import ResponsesSerializer
from .validators import validate_title, validate_description

# class FilesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Files
#         # fields = ['id', 'file_path', 'created_at', 'updated_at']
#         fields = "__all__"

# class ResponseSerial(serializers.ModelSerializer):
#     class Meta:
#         model = Responses
#         fields = "__all__"


class QuerySerializer(serializers.ModelSerializer):
    responses = ResponsesSerializer(many=True, read_only=True)

    class Meta:
        model = Queries
        # fields = ['id',  'title', 'description', 'file_path', 't_id', 'responses']
        fields = "__all__"
        extra_kwargs = {
            'u_id': {'read_only': True}
        }

        def validate(self, data):
            if 'title' not in self.initial_data.keys() or (not data.get('title')):
                raise serializers.ValidationError({'title': 'title is required field.'})
            if Queries.objects.filter(title=data.get('title')).exists():
                msg = "title with {} already exists".format(data.get('title'))
                raise serializers.ValidationError(msg)
            if not validate_title(data.get('title')):
                msg = "{} invalid title".format(data.get('title'))
                raise serializers.ValidationError(msg)

            if 'description' not in self.initial_data.keys() or (not data.get('description')):
                raise serializers.ValidationError({'description': 'description is required field.'})
            # if Queries.objects.filter(description=data.get('description')).exists():
            #     msg = "description with {} already exists".format(data.get('description'))
            #     raise serializers.ValidationError(msg)
            if not validate_description(data.get('description')):
                msg = "invalid description"
                raise serializers.ValidationError(msg)



"""
class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)


class QuerySerializer(serializers.ModelSerializer):
    child = RelatedFieldAlternative(queryset=Responses.objects.all(), serializer=ResponsesSerializer)

    class Meta:
        model = Queries
        # fields = '__all__'
        fields = ['id', 'u_id', 'title', 'description', 'file_path', 't_id', 'child']
"""
