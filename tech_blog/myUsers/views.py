from .models import CustomUser
from .serializer import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.core.mail import send_mail
from utils.email import register_email, forgot_password_email
from django.contrib.auth.hashers import make_password, check_password
from utils.generate_new_password import generate_temp_password_and_check
from utils.decode_token import get_user
from utils.generate_new_password import password_validator
from utils.pagination import Pagination
from utils.authentication_keys import token_authentication
from utils.authentication_keys import mandatory_token_authentication, optional_token_authentication
from django.utils.decorators import method_decorator

# Create your views here.


# using Viewsets
class UserViewSet(viewsets.ViewSet):

    # permission_classes = [CreateAndIsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # def get_authenticators(self):
    #     if self.action == 'create':
    #         authentication_classes = []
    #     else:
    #         authentication_classes = [JWTAuthentication]
    #     return [authenticate() for authenticate in authentication_classes]

    # authentication_classes = (JWTAuthentication,)

    # def get_authenticators(self):
    #     if self.action == 'create':
    #         return []
    #     return JWTAuthentication

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    # @app_authentication
    # @method_decorator(platformcheck)
    # @platformcheck_using_class_name
    @optional_token_authentication
    # @mandatory_token_authentication
    # @token_authentication
    def list(self, request):
        page = request.query_params.get('page', 1)
        filters = {'is_active': 1, 'firstname': 'kamal'}
        obj = Pagination(CustomUser, page, **filters)
        result = obj.get_queries()
        serializer = UserSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def list(self, request):
    #     queryset = CustomUser.objects.all()
    #     paginator = MyPageNumberPagination()
    #     result_page = paginator.paginate_queryset(queryset, request)
    #     print(result_page)
    #     serializer = UserSerializer(result_page, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            tech = CustomUser.objects.get(id=pk)
            serializer = UserSerializer(tech)
            return Response(serializer.data)

    # @method_decorator(platformcheck)
    @token_authentication
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            name = serializer.validated_data["username"]
            serializer.save()
            register_email(email, name)
            return Response({'msg': 'Data created'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        id = pk
        user = CustomUser.objects.get(pk=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            return Response({'msg': 'Data updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        id = pk
        if not id:
            return Response({'msg': 'id is required in the url'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(pk=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data partial update'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({'msg': 'input(primarykey) is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(id=pk, is_active=True)
        except:
            return Response({'msg': 'user not found'})
        # if user.is_active == False:
        #     return Response({"msg": "User disabled"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        return Response({"msg": "User Deleted Successfully"}, status=status.HTTP_200_OK)
    # def delete(self, request, pk=None):
    #     if not pk:
    #         return Response({'msg': 'pk is required in the url'}, status=status.HTTP_400_BAD_REQUEST)
    #     id = pk
    #     stu = CustomUser.objects.get(pk=id)
    #     stu.delete()
    #     return Response({'msg': 'Data deleted'}, status=status.HTTP_200_OK)


class ForgotPassword(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print(request)
        email = request.data['email']
        print(email)
        if not email:
            return Response({'msg: email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.get(email=email)
        if user:
            password = generate_temp_password_and_check()
            user.password = make_password(password)
            forgot_password_email(user.email, user.username, password)
            user.save()
            return Response({'msg': 'Data partial update'}, status=status.HTTP_200_OK)
        return Response({'msg': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = get_user(request)
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        confirm_new_password = request.data['confirm_new_password']
        if not (old_password or new_password or confirm_new_password):
            return Response({'msg: old_password, new_password, confirm_new_password'},
                            status=status.HTTP_400_BAD_REQUEST)

        if check_password(old_password, user.password):
            if password_validator(new_password):
                if new_password == confirm_new_password:
                    user.password = make_password(new_password)
                    user.save()
                    return Response({'msg: Password Changed'}, status=status.HTTP_200_OK)
                return Response({'msg: new password and confirm new password does not match'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {'msg: password should have min 8 characters, an upper case & lower case letter,'
                 ' a special character and a digit.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg: Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)


# class Login(viewsets.ModelViewSet):
#     permission_classes = [AllowAny]
#
#     def create(request):
#
#         email = request.data.get('email')
#         password = request.data.get('password')
#         response = Response()
#         if (email is None) or (password is None):
#             raise exceptions.AuthenticationFailed(
#                 'username and password required')
#
#         user = User.objects.filter(username=username).first()
#         if (user is None):
#             raise exceptions.AuthenticationFailed('user not found')
#         if (not user.check_password(password)):
#             raise exceptions.AuthenticationFailed('wrong password')
#
#         serialized_user = UserSerializer(user).data
#
#         access_token = generate_access_token(user)
#         refresh_token = generate_refresh_token(user)
#
#         response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
#         response.data = {
#             'access_token': access_token,
#             'user': serialized_user,
#         }
#
#         return response
