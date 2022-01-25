from django.shortcuts import render
from .models import AuthenticationKeys
from .serializer import AuthenticationKeySerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from technology.my_pagination import MyPageNumberPagination
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from responses.serializer import ResponsesSerializer
from utils.decode_token import get_user_id, get_user
from myUsers.models import CustomUser
from myUsers.serializer import UserSerializer
from rest_framework.views import APIView
from django.db.models import Q
import logging
logger = logging.getLogger(__name__)


# using Viewsets

class AuthenticationKeysViewSet(viewsets.ViewSet):
    # authentication_classes = [JWTAuthentication]

    # def get_permissions(self):
    #     if self.action in ('list', 'retrieve'):
    #         permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = AuthenticationKeys.objects.all()
        paginator = MyPageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = AuthenticationKeySerializer(result_page, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = AuthenticationKeySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data created'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        id = pk
        if not id:
            return Response({'msg': 'input(primarykey) is required'},status=status.HTTP_400_BAD_REQUEST)

        try:
            query_check=AuthenticationKeys.objects.get(id=id, is_active=True)
        except:
            logger.info({"msg": "Authentication key not found or user unable to delete"})
            return Response({"msg": "Authentication key not found or user unable to delete"},status=status.HTTP_400_BAD_REQUEST)
        query_check.is_active=False
        query_check.save()
        print(query_check.is_active)
        logger.info({"msg":"Authentication key deleted successfully"})
        return Response({"msg": "Authentication key deleted successfully"},status=status.HTTP_200_OK)
