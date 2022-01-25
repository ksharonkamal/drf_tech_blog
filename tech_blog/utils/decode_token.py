import jwt
from tech_blog import settings
from myUsers.models import CustomUser


def get_user_id(request):
    try:
        bearer_token = request.headers['Authorization']
        # print("bearer token=", bearer_token)
        x = bearer_token.split(' ', 1)
        # print(x)
        decodedPayload = jwt.decode(x[1], settings.SECRET_KEY, algorithms=['HS256'])
        return decodedPayload['user_id']
    except:
        return None


def get_user(request):
    try:
        bearer_token = request.headers['Authorization']
        x = bearer_token.split(" ", 1)
        decodedPayload = jwt.decode(x[1], settings.SECRET_KEY, algorithms=['HS256'])
        return CustomUser.objects.get(id=decodedPayload['user_id'])
    except:
        return None
