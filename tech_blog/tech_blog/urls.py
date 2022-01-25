from django.contrib import admin
from django.urls import path, include
from technology import views
from rest_framework.routers import DefaultRouter
from myUsers.views import UserViewSet, ForgotPassword, ChangePassword
from queries.views import QueryViewSet, QueryBasedOnTechnology
from responses.views import ResponsesViewSet
from authentication.views import AuthenticationKeysViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static

# creating router object
router = DefaultRouter()

# registering our api with the router
# router.register('technology', views.TechnologyViewSet, basename='technology')
# router.register('technology', views.TechnologyAPI.as_view(), basename='technology')

router.register('user', UserViewSet, basename='user')
router.register('queries', QueryViewSet, basename='query')
router.register('responses', ResponsesViewSet, basename='response')
router.register('forgotpassword', ForgotPassword, basename='forgotpassword')
router.register('changepassword', ChangePassword, basename='changepassword')
router.register('querytech', QueryBasedOnTechnology, basename='querytech')
router.register('authkeys', AuthenticationKeysViewSet, basename='authkeys')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('gettoken/', TokenObtainPairView.as_view(), name='get_token'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='refresh_token'),
    path('verifytoken/', TokenVerifyView.as_view(), name='verify_token'),
    path('technology/', views.TechnologyAPI.as_view()),
    path('technology/<int:pk>', views.TechnologyAPI.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# print(urlpatterns)
# print(type(urlpatterns))
# for itr in urlpatterns:
#     print(itr, type(itr))
#
# print(router)
