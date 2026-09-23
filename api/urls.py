from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Phase 1 — Basic Authentication
    path("basic/", views.basic_auth_view, name="basic-auth"),

    # Phase 2 — Session Authentication
    path("session/", views.session_auth_view, name="session-auth"),

    # Phase 3 — Token Authentication (Opaque)
    #   Generate token first:  python manage.py drf_create_token admin
    path("token/", views.token_auth_view, name="token-auth"),

    # Phase 4 — JWT
    #   Obtain token pair: POST /api/jwt/login/
    #   Refresh access token: POST /api/jwt/refresh/
    path("jwt/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/protected/", views.jwt_protected_view, name="jwt-protected"),
]
