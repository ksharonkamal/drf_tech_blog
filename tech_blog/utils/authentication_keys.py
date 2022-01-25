import myUsers.serializer
from authentication.models import AuthenticationKeys, AuthPermissions
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from rest_framework.serializers import ValidationError



def check_auth_token(**kwargs):
    check_token = AuthPermissions.objects.filter(platform_permissions__key=kwargs['token'])
    print(check_token.exists())
    if check_token.exists():
        check_api = check_token.filter(class_name=kwargs['class_name'])
        if check_api:
            if check_api.filter(method=kwargs['method']):
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def token_authentication(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            class_name = args[0].__class__.__name__
            token = args[1].headers['token']
            url = args[1].build_absolute_uri('?')
            method = args[1].method
        except:
            return Response({'msg': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
        if check_auth_token(class_name=class_name, token=token, url=url, method=method):
            return func(*args, **kwargs)
        return Response({'msg': 'authentication failed'}, status=status.HTTP_400_BAD_REQUEST)
    return decorated


def mandatory_token_authentication(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            token = args[1].headers['token']
            if AuthenticationKeys.objects.filter(key=token).exists():
                return func(*args, **kwargs)
        except:
            return Response({'msg': 'Token authentication failed'}, status=status.HTTP_400_BAD_REQUEST)
    return decorated


def optional_token_authentication(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            token = args[1].headers['token']
            url = args[1].build_absolute_uri('?')
            method = args[1].method
            absolute(args[1])
            return func(*args, **kwargs)
        except:
            pass
    return decorated


def absolute(request):
    print(request)
    urls = {
        'ABSOLUTE_ROOT': request.build_absolute_uri('/')[:-1].strip("/"),
        'ABSOLUTE_ROOT_URL': request.build_absolute_uri('/').strip("/"),
        'FULL_URL_WITH_QUERY_STRING': request.build_absolute_uri(),
        'FULL_URL': request.build_absolute_uri('?'),
        'test': request.build_absolute_uri('?').replace('http://127.0.0.1:8000', ""),
        'test2': request.path.split('/')[1]
    }
    print(urls)
    return urls





"""
def check_auth_token(**kwargs):
    try:
        obj = AuthPermissions.objects.get(**kwargs)
        if obj:
            return True
        else:
            return False
    except:
        return False


def platformcheck(func):
    def wrap(request, *args, **kwargs):
        if not request.headers.get('token'):
            raise ValidationError({'msg': 'token required'})
        url = request.build_absolute_uri('?')
        method = request.method
        if check_auth_token(platform_permissions__key=request.headers.get('token'), url=url, method=method):
            return func(request, *args, **kwargs)
        else:
            return Response({'msg': 'Invalid token for the request'}, status=status.HTTP_400_BAD_REQUEST)
    return wrap


def platformcheck_using_class_name(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            class_name = args[0].__class__.__name__
            token = args[1].headers['token']
            url = args[1].build_absolute_uri('?')
            method = args[1].method
            is_valid = check_auth_token(class_name=class_name, platform_permissions__key=token, url=url, method=method)
        except:
            return Response({'msg': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
        if is_valid:
            return func(*args, **kwargs)
        return Response({'msg': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    return decorated
"""


