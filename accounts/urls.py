from django.urls import path
from .views import CreateUser, UserLogin, UserLogout, Follow, ActivateAccount

urlpatterns = [
    path("signup/", CreateUser.as_view(), name="sign-user"),
    path("login/", UserLogin.as_view(), name="login-user"),
    path("logout/", UserLogout.as_view(), name="logout-user"),
    path("f/", Follow.as_view(), name="follow-user"),
    path("<slug:username>/<slug:uuid>", ActivateAccount.as_view(), name="active-user"),
]
