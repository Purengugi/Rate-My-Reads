from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, sign_up, TokenObtainPairView, TokenRefreshView, UserListAPIView, homepage


router = DefaultRouter()
router.register("users", UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path("sign_up/", sign_up, name="sign_up"),
    path("sign_in/",TokenObtainPairView.as_view(), name='sign_in'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("user/list/", UserListAPIView.as_view(), name="user-list-search"),
    path("homepage/", homepage, name="homepage"),
]