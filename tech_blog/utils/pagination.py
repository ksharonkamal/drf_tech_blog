from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


class Pagination:
    def __init__(self, model, page=1, **kwargs):
        # Instance Variable
        self.model = model
        self.page = int(page)
        self.filters = kwargs
        self.limit = 10
        self.offset = 0

    def get_queries(self):
        try:
            if self.page <= 0:
                raise serializers.ValidationError({"msg": "page number should be positive"})
        except:
            raise serializers.ValidationError({"msg": "page in integer format required"})

        if self.page != 1:
            self.offset = (self.page - 1) * self.limit

        try:
            queryset = self.model.objects.filter(**(self.filters))[self.offset:(self.limit + self.offset)]
            if queryset:
                return queryset
            else:
                raise serializers.ValidationError({"msg": "records not found"})
        except Exception as e:
            raise serializers.ValidationError({"msg": str(e)})


