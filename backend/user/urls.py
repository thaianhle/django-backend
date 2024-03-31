from dj_rest_auth.jwt_auth import get_refresh_view

from dj_rest_auth.registration.views import RegisterView

from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView

from rest_framework_simplejwt.views import TokenVerifyView

from django.urls import path
urlpatterns = [
    path('register/', RegisterView.as_view(), name="rest_auth_register"),
    path('login/', LoginView.as_view(), name="rest_auth_login"),
    path('logout/', LogoutView.as_view(), name="rest_auth_logout"),
]