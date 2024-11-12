from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, UserExtendedSerializer
from rest_framework.authtoken.models import Token
from .models import CustomUser


# Create your views here.

from rest_framework import generics
from .models import Object
from .serializers import ObjectSerializer

class ObjectList(generics.ListAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

    def get(self, request, format=None):
        try:
            object = Object.objects.all()
            serializer = ObjectSerializer(object, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"code": 400, "message": "Invalid login or password"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response({"code": 400, "message": "Invalid login or password"}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({
                            "code": 200,
                            "message": "Login successful",
                            "token": token.key
                        }, status=status.HTTP_200_OK) 
    except:
        return Response({
                "code": 500,
                "message": "Server error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        # Jeżeli tu sie wywala, usuncie baze danych i stworzcie ponownie
        if serializer.is_valid():
            validated_data = serializer.validated_data
            password = validated_data.pop("password", None)
            user = CustomUser(**validated_data)
            if password:
                user.set_password(password)
            user.save()
            token = Token.objects.create(user=user)
            return Response({
                "code": 201,
                "message": "Register successful"
            }, status=status.HTTP_201_CREATED)
        return Response({
                "code": 400,
                "message": "Incorrect e-mail or password format"
            }, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({
                "code": 500,
                "message": "Server error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def logout_user(request):
    token_key = request.data.get('token')

    if not token_key:
        return Response({"code": 401, "message": "Sesion or token disactive"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        token = Token.objects.get(key=token_key)
        token.delete()
        return Response({"code": 200, "message": "Logout successful"}, status=status.HTTP_200_OK)

    except Token.DoesNotExist:
        # Token not found
        return Response({"code": 401, "message": "Sesion or token disactive"}, status=status.HTTP_401_UNAUTHORIZED)

    except:
        # Handle unexpected errors
        return Response({"code": 500, "message": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserExtendedSerializer

    def get(self, request, format=None):
        try:
            user = CustomUser.objects.all()
            serializer = UserExtendedSerializer(user, many=True)
            return Response({
                "code": 200,
                "user": serializer.data,
                }, status=status.HTTP_200_OK)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)