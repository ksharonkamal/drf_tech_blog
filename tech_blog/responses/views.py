from django.shortcuts import render
from .models import Responses
from .serializer import ResponsesSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from technology.my_pagination import MyPageNumberPagination
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.decode_token import get_user_id, get_user
from myUsers.serializer import UserSerializer
# Create your views here.
from . import logger


def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# using Viewsets
class ResponsesViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # def list(self, request):
    #     queryset = Responses.objects.all()
    #     paginator = MyPageNumberPagination()
    #     result_page = paginator.paginate_queryset(queryset, request)
    #     print(result_page)
    #     serializer = ResponsesSerializer(result_page, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):  # get all records
        offset = request.query_params.get('offset', 0)
        limit = request.query_params.get('limit', 3)
        queryset = Responses.objects.filter(is_active=1)[int(offset):(int(limit) + int(offset))]
        if not queryset:
            return Response({'message': 'no data found'}, status=status.HTTP_400_BAD_REQUEST)
        # paginator = StandardResultsSetPagination()
        # result_page = paginator.paginate_queryset(queryset, request)
        serializer = ResponsesSerializer(queryset, many=True)
        if not serializer:
            return Response({"data": serializer.errors, "message": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data": serializer.data, "message": "success"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            query = Responses.objects.get(id=pk)
            serializer = ResponsesSerializer(query)
            return Response(serializer.data)

    def create(self, request):
        serializer = ResponsesSerializer(data=request.data)
        user = get_user(request)
        if serializer.is_valid():
            serializer.save(u_id=user)
            return Response({'msg': 'Data created'}, status=status.HTTP_200_OK)
        return Response({"data": serializer.errors, "message": "failure"}, status=status.HTTP_400_BAD_REQUEST)

        # serializer = ResponsesSerializer(data=request.data)
        # user = get_user(request)
        # if 'file_path' not in request.FILES or not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     handle_uploaded_file(request.FILES['file_path'])
        #     serializer.save(u_id=user)
        #     return Response({'msg': 'Data created'}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if not pk:
            return Response({'msg': 'pk required'}, status=status.HTTP_400_BAD_REQUEST)
        id = pk
        try:
            query = Responses.objects.get(pk=id)
            serializer = ResponsesSerializer(query, data=request.data)
            user_id = request.user.id
            if serializer.is_valid():
                user_serializer_id = UserSerializer(query.u_id).data['id']
                if user_id == user_serializer_id:
                    serializer.save()
                    return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg": "failure"}, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk=None):
        if not pk:
            return Response({'msg': 'pk required'}, status=status.HTTP_400_BAD_REQUEST)
        id = pk
        try:
            query = Responses.objects.get(pk=id)
            serializer = ResponsesSerializer(query, data=request.data, partial=True)
            user_id = get_user_id(request)
            if serializer.is_valid():
                user_serializer_id = UserSerializer(query.u_id).data['id']
                if user_id == user_serializer_id:
                    serializer.save()
                    return Response({'msg': 'Data partial update'}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        id = pk
        if not id:
            return Response({'msg':'input(primarykey) is required'},status=status.HTTP_400_BAD_REQUEST)
        user_id=request.user.id
        print(user_id)
        try:
            query_check=Responses.objects.get(id=id,u_id=user_id,is_active=True)
            # print(query_check)
        except:
            logger.info({"msg": "response not found or user unable to delete"})
            return Response({"msg": "response not found or user unable to delete"},status=status.HTTP_400_BAD_REQUEST)
        query_check.is_active=False
        query_check.save()
        print(query_check.is_active)
        logger.info({"msg":"response deleted successfully"})
        return Response({"msg": "response deleted successfully"},status=status.HTTP_200_OK)

    # def delete(self, request, pk=None):
    #     if not pk:
    #         return Response({'msg': 'pk required'}, status=status.HTTP_400_BAD_REQUEST)
    #     id = pk
    #     query = Responses.objects.get(pk=id)
    #     query.delete()
    #     return Response({'msg': 'Data deleted'}, status=status.HTTP_200_OK)
