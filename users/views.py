from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Профиль пользователя"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TelegramConnectView(APIView):
    """Привязка Telegram аккаунта"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')

        if not code:
            return Response(
                {'error': 'Код не указан'},
                status=status.HTTP_400_BAD_REQUEST
            )


        return Response({
            'message': 'Telegram аккаунт успешно привязан',
            'code': code
        })
