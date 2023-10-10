from django.urls import path
from .views import CreateUser, UserLogin, UserLogout


urlpatterns = [
    path("signup/", CreateUser.as_view(), name="sign-user"),
    path("login/", UserLogin.as_view(), name="login-user"),
    path("logout/", UserLogout.as_view(), name="logout-user"),
]
