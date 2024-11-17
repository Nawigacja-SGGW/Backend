from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ObjectSerializer, UserSerializer, UserExtendedSerializer, UserObjectSearchSerializer, UserObjectSearchExtendedSerializer
from rest_framework.authtoken.models import Token
from .models import CustomUser, Object, UserObjectSearch


class Object_list(generics.ListAPIView):
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



class Reset_password(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def put(self, request):
        try:
            token_key = request.data.get('token')
            token = Token.objects.get(key=token_key)
            user = CustomUser.objects.get(auth_token=token)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                password = request.data.get('password')      
                user.set_password(password)
                user.save()
                return Response({
                    "code": 200,
                    "message": "Password reset successful",
                    }, status=status.HTTP_200_OK)
            return Response({
                "code": 400,
                "message": "Password reset failed",
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class User_list(generics.ListAPIView):
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
        

class Distance_sum_update(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserExtendedSerializer

    def put(self, request):
        try:
            id = request.data.get('id')
            user = CustomUser.objects.get(id=id)
            serializer = UserExtendedSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class Route_created_count_update(generics.UpdateAPIView):
    queryset = UserObjectSearch.objects.all()
    serializer_class = UserObjectSearchExtendedSerializer

    def post(self, request):
        try:
            serializer = UserObjectSearchExtendedSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            user = request.data.get('user')
            object_latitude = request.data.get('object_latitude')
            object_longitude = request.data.get('object_longitude')
            user_object_search = UserObjectSearch.objects.get(user=user, object_latitude=object_latitude, object_longitude=object_longitude)
            serializer = UserObjectSearchSerializer(user_object_search, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"user": serializer.data,},status=status.HTTP_200_OK)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
