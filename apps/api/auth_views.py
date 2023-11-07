from rest_framework import status
from rest_framework.views import APIView
from django.db import utils

from. import mixins
from .utils import get_tokens_for_user
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from account.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer  # Vous devez créer ce serializer


class LoginApi(APIView, mixins.HttpResponseMixin):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        username = request.data.get("email")
        password = request.data.get("password")
        print(request)
        if not username or not password:
            return self.error_response(message="Must Provide user id and password")
        user: User = authenticate(username=username, password=password)
        if not user:
            return self.error_response(message="Invalid Credentials")
        tokens = get_tokens_for_user(user=user)
        
        data = {
            'success':'true',
            "user": {
                "_id": user.pk, 
                "email": user.email, 
                "admin":user.admin,
                "helpdesk":user.is_helpdesk, 
                "tech":user.is_technicien 
                    },
            "token": tokens.get("access_token"),
            "refresh": tokens.get("refresh_token"),
        }
        return self.success_response(message="Login success", data=data)


class RegisterApi(APIView, mixins.HttpResponseMixin):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        password2 = request.data.get("password2")
        if not email or not password:
            return self.error_response(message="Must Provide username and password")
        if password != password2:
            return self.error_response(message="Passwords do not match")
        try:
            User.objects.create_user(password=password, email=email)
        except utils.IntegrityError as e:
            return self.error_response(
                message=f"User with this username already exists"
            )

        return self.success_response(
            message="Registration successful",
        )


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.method == 'POST':
        request.auth.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
