from django.core.mail import send_mail
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ObjectDynamicSerializer, UserSerializer, UserExtendedSerializer, UserObjectSearchSerializer, UserObjectSearchExtendedSerializer, PointObjectSerializer, AreaObjectSerializer
from rest_framework.authtoken.models import Token
from .models import CustomUser, Object, UserObjectSearch, PointObject, AreaObject


class Object_list(generics.ListAPIView):

    def get(self, request, format=None):
        try:
            point_objects = PointObject.objects.all()
            point_object_serializer = PointObjectSerializer(point_objects, many=True)
            area_objects = AreaObject.objects.all()
            area_object_serializer = AreaObjectSerializer(area_objects, many=True)
            return Response({
                    "code": 200,
                    "point_objects": point_object_serializer.data,
                    "area_objects": area_object_serializer.data
                }, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Object_single(generics.ListAPIView):
    def get(self, request, format=None):
        try:
            id = request.data.get("id")
            object = Object.objects.get(id=id)
            serializer = ObjectDynamicSerializer(object, data=request.data, partial=True)
            if serializer.is_valid():
                return Response({
                    "code": 200,
                    "object": serializer.data
                }, status=status.HTTP_200_OK)
        except Object.DoesNotExist:
            return Response({
                "code": 400,
                "message": "Incorrect id",
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                            "token": token.key,
                            "userID": serializer.data.get("id")
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
        except Token.DoesNotExist:
            # Token not found
            return Response({"code": 401, "message": "Sesion or token disactive"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Reset_password_request(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def put(self, request):
        try:
            email = request.data.get('email')
            user = CustomUser.objects.get(email=email)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                token, _ = Token.objects.get_or_create(user=user)
                reset_url = f"{request.scheme}://{request.get_host()}/password-reset-confirm/{token.key}/"
                send_mail(
                    subject='Nawigacja SGGW - resetowanie hasla/password reset',
                    message=f"Link:\n\n{reset_url}",
                    from_email=None,
                    recipient_list=[email],
                )
                return Response({
                "code": 200,
                "message": "E-mail send",
                }, status=status.HTTP_200_OK)
            return Response({
                "code": 400,
                "message": "Incorrect e-mail",
                }, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({
                "code": 400,
                "message": "Incorrect e-mail",
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

    def get(self, request):
        try:
            id = request.data.get('userID')
            user = CustomUser.objects.get(id=id)
            serializer = UserExtendedSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                return Response({
                        "code": 200,
                        "distance_sum": serializer.data.get("distance_sum"),
                        }, status=status.HTTP_200_OK)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            object_id = request.data.get("object_id")
            user = request.data.get("user")
            try:
                Object.objects.get(id=object_id)
                CustomUser.objects.get(id=user)
            except Object.DoesNotExist:
                raise serializers.ValidationError("Object does not exist.")
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("User does not exist.")
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
            object_id = request.data.get('object_id')
            user_object_search = UserObjectSearch.objects.get(user=user, object_id=object_id)
            serializer = UserObjectSearchSerializer(user_object_search, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
