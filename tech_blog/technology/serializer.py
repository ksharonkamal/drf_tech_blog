from rest_framework import serializers
from .models import Technology
from .validators import validate_name


class TechnologySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10, validators=[validate_name])
    is_active = serializers.BooleanField(required=False)
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    def create(self, validate_data):
        return Technology.objects.create(**validate_data)

    def update(self, instance, validate_data):  # instance is the new data, validate_data has the old data
        instance.name = validate_data.get('name', instance.name)
        instance.is_active = validate_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    # object level validations
    # def validate(data):
    #     nm = data.get('name')
    #     if len(nm) > 10:
    #         raise serializers.ValidationError('Name not with in the range')
    #     return data
