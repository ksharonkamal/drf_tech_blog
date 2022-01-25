from .models import Queries
from .serializer import QuerySerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from technology.my_pagination import MyPageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.decode_token import get_user_id, get_user
from myUsers.serializer import UserSerializer
from utils.authentication_keys import token_authentication
from django.utils.decorators import method_decorator

import logging
logger = logging.getLogger(__name__)


# Create your views here.


# def handle_uploaded_file(f):
#     print("1", f)
#     for itr in f:
#         print("itr:", itr)
#         with open(itr, 'wb+') as destination:
#             for chunk in itr.chunks():
#                 destination.write(chunk)


def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# using Viewsets

class QueryViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # def list(self, request):
    #     queryset = Queries.objects.all()
    #     paginator = MyPageNumberPagination()
    #     result_page = paginator.paginate_queryset(queryset, request)
    #     serializer = QuerySerializer(result_page, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @method_decorator(platformcheck)
    # @token_authentication
    def list(self, request):  # get all records
        offset = request.query_params.get('offset', 0)
        limit = request.query_params.get('limit', 3)
        queryset = Queries.objects.filter(is_active=1)[int(offset):(int(limit) + int(offset))]
        if not queryset:
            return Response({'message': 'no data found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = QuerySerializer(queryset, many=True)
        if not serializer:
            return Response({"data": serializer.errors, "message": "failure"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data": serializer.data, "message": "success"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            query = Queries.objects.get(id=pk)
            serializer = QuerySerializer(query)
            return Response(serializer.data)

    def create(self, request):
        serializer = QuerySerializer(data=request.data)
        user = get_user(request)
        if serializer.is_valid():
            serializer.save(u_id=user)
            return Response({'msg': 'Data created'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # if 'file_path' not in request.FILES or not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     handle_uploaded_file(request.FILES['file_path'])
        #     serializer.save(u_id=user)
        #     return Response({'msg': 'Data created'}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        id = pk
        query = Queries.objects.get(pk=id)
        serializer = QuerySerializer(query, data=request.data)
        # user_id = get_user_id(request)
        user_id = request.user.id
        print("user_id", user_id)
        if serializer.is_valid():
            user_serializer_id = UserSerializer(query.u_id).data['id']
            if user_id == user_serializer_id:
                serializer.save()
                return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        id = pk
        query = Queries.objects.get(pk=id)
        serializer = QuerySerializer(query, data=request.data, partial=True)
        user_id = get_user_id(request)
        if serializer.is_valid():
            user_serializer_id = UserSerializer(query.u_id).data['id']
            if user_id == user_serializer_id:
                serializer.save()
                return Response({'msg': 'Data partial update'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        id = pk
        if not id:
            return Response({'msg':'input(primarykey) is required'},status=status.HTTP_400_BAD_REQUEST)
        user_id=request.user.id
        print(user_id)
        try:
            query_check=Queries.objects.get(id=id,u_id=user_id,is_active=True)
            # print(query_check)
        except:
            logger.info({"msg": "query not found or user unable to delete"})
            return Response({"msg": "query not found or user unable to delete"},status=status.HTTP_400_BAD_REQUEST)
        query_check.is_active=False
        query_check.save()
        print(query_check.is_active)
        logger.info({"msg":"query deleted successfully"})
        return Response({"msg": "query deleted successfully"},status=status.HTTP_200_OK)
    # def delete(self, request, pk=None):
    #     if not pk:
    #         return Response({'msg': 'pk required'}, status=status.HTTP_400_BAD_REQUEST)
    #     id = pk
    #     query = Queries.objects.get(pk=id)
    #     serializer = QuerySerializer(query, data=request.data, partial=True)
    #     user_id = get_user_id(request)
    #     if serializer.is_valid():
    #         user_serializer_id = serializer.data['u_id']
    #         if user_id == user_serializer_id:
    #             query.delete()
    #         else:
    #             return Response({'msg': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({'msg': 'Data deleted'}, status=status.HTTP_200_OK)


class QueryBasedOnTechnology(viewsets.ViewSet):

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        data = request.data
        tech_id = data.get('tech_id')
        user_id = data.get('user_id')

        if tech_id and user_id:
            queryset = Queries.objects.filter(t_id__in=tech_id, u_id__in=user_id)
        elif tech_id:
            queryset = Queries.objects.filter(t_id__in=tech_id)
        elif user_id:
            queryset = Queries.objects.filter(u_id__in=user_id)
        else:
            queryset = Queries.objects.all()

        # queryset = Queries.objects.filter(t_id__in=tech_id, u_id)

        # queryset = Queries.objects.filter(Q(t_id__in=tech_id) | Q(u_id__in=user_id))

        paginator = MyPageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = QuerySerializer(result_page, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
