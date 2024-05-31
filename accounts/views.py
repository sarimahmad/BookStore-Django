from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import StoreUser
from .serializers import SignUpSerializer, LoginSerializer, LoginResponseSerializer
from django.db import transaction


# Create your views here.
class SignUpAPIView(APIView):
    serializer_class = SignUpSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if StoreUser.objects.filter(email=request.data['email']).exists():
            return Response({"message": "Email already exists"}, status=status.HTTP_226_IM_USED)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            response_data = {
                "Token": str(access_token),
                "user": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginAPIView(APIView):

    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            user_info = LoginResponseSerializer(user).data
            update_last_login(None, user)
            response_data = {
                "Token": str(access_token),
                "user": user_info

            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
