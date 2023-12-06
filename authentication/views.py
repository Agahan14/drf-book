from rest_framework import status, generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from authentication.serializers import (
    UserRegisterSerializer,
    ConfirmationCodeSerializer,
    LoginSerializer,
    LogoutSerializer,
)
from authentication.models import User, ConfirmationCode
from authentication.utils import Util


class TokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=['Authentication'],
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
    )
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                'error': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        email = request.data.get('email').lower()
        password = request.data.get('password')

        user = User.objects.create_user(
            email=email,
            password=password,
        )
        confirmation_code = ConfirmationCode.generate_code()
        ConfirmationCode.objects.create(user=user, code=confirmation_code)

        data = {
            "email_body": f'Your confirmation code: {confirmation_code}',
            "to_email": email,
            "email_subject": 'Confirmation Code',
        }

        Util.send_email(data)
        response_data = {
            "message": "User successfully registered. Confirmation code sent to your email.",
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class ConfirmCodeView(generics.GenericAPIView):
    serializer_class = ConfirmationCodeSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')
        try:
            confirmation_code = ConfirmationCode.objects.get(code=code)
        except ConfirmationCode.DoesNotExist:
            return Response({"error": "Invalid or already confirmed code."}, status=400)

        user = confirmation_code.user
        user.is_verified = True
        user.save()
        confirmation_code.delete()
        return Response({
            "message": "You successfully verified your account!",
        }, status=200)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
    )
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({
                "error": "User not found!"
            }, status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            raise AuthenticationFailed({
                "error": "Incorrect password!"
            })

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Authentication'],
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh_token"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message": "You have successfully logged out."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "Unable to log out."
            }, status=status.HTTP_400_BAD_REQUEST)
