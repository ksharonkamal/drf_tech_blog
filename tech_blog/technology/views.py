from django.shortcuts import render
from .models import Technology
from .serializer import TechnologySerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .my_pagination import MyPageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from utils.authentication_keys import token_authentication
from django.utils.decorators import method_decorator


# Create your views here.

"""
class TechnologyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Technology.objects.all()
        paginator = MyPageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = TechnologySerializer(result_page, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            tech = Technology.objects.get(id=pk)
            seriliazer = TechnologySerializer(tech)
            return Response(seriliazer.data)

    def create(self, request):
        serializer = TechnologySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data created'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        id = pk
        tech = Technology.objects.get(pk=id)
        serializer = TechnologySerializer(tech, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        id = pk
        tech = Technology.objects.get(pk=id)
        serializer = TechnologySerializer(tech, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data partial update'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        id = pk
        stu = Technology.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data deleted'}, status=status.HTTP_200_OK)
"""


class TechnologyAPI(APIView):
    authentication_classes = [JWTAuthentication]

    # def get_permissions(self):
    #     if self.action in ('list', 'retrieve'):
    #         permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]

    # @method_decorator(platformcheck)
    # @platformcheck_using_class_name
    @token_authentication
    def get(self, request, pk=None):
        id = pk
        print("my req")
        print(request)
        if id is not None:
            queryset = Technology.objects.get(id=id)
            paginator = MyPageNumberPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = TechnologySerializer(result_page, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Technology.objects.all()
        serializer = TechnologySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TechnologySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data created'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        id = pk
        queryset = Technology.objects.get(pk=id)
        serializer = TechnologySerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        id = pk
        queryset = Technology.objects.get(pk=id)
        serializer = TechnologySerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'msg': 'pk required'}, status=status.HTTP_400_BAD_REQUEST)
        id = pk
        queryset = Technology.objects.get(pk=id)
        queryset.delete()
        return Response({'msg': 'Data deleted'}, status=status.HTTP_200_OK)
