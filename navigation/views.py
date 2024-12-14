from .models import AreaObject, CustomUser, Object, PointObject, UserObjectSearch
from .serializers import AreaObjectSerializer, ObjectDynamicSerializer, PointObjectSerializer, UserSerializer, UserExtendedSerializer, UserObjectSearchSerializer, UserObjectSearchExtendedSerializer
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

class Login(APIView):
    
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"code": 400, "message": "Invalid login or password"}, status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(password):
                return Response({"code": 400, "message": "Invalid login or password"}, status=status.HTTP_400_BAD_REQUEST)
            token, _ = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(instance=user)
            return Response({
                                "code": 200,
                                "message": "Login successful",
                                "token": token.key,
                                "user_id": serializer.data.get("id")
                            }, status=status.HTTP_200_OK)
        except:
            return Response({
                    "code": 500,
                    "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Logout(APIView):

    def post(self, request):
        token_key = request.data.get('token')
        if not token_key:
            return Response({"code": 401, "message": "Sesion or token disactive"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = Token.objects.get(key=token_key)
            token.delete()
            return Response({"code": 200, "message": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"code": 401, "message": "Sesion or token disactive"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"code": 500, "message": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Object_list(generics.ListAPIView):

    def get(self, request):
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

class Object_single(generics.RetrieveAPIView):
    
    def get(self, request):
        try:
            id = request.query_params.get("id")
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

class Register(APIView):
    
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                password = validated_data.pop("password", None)
                user = CustomUser(**validated_data)
                if password:
                    user.set_password(password)
                user.save()
                _ = Token.objects.create(user=user)
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

class Reset_password(APIView):

    def patch(self, request):
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
            return Response({"code": 401, "message": "Sesion or token disactive"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Reset_password_request(APIView):

    def patch(self, request):
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

class User_history(APIView):

    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            history = UserObjectSearch.objects.filter(user=user_id).order_by('-timestamp')[:5]
            serializer = UserObjectSearchSerializer(history, many=True)
            return Response({
                "code": 200,
                "history": serializer.data
                }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({
                "code": 400,
                "message": "Incorrect user_id"
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            object_id = request.data.get('object_id')
            user = CustomUser.objects.get(id=user_id)
            object = Object.objects.get(id=object_id)
            request.data['user'] = request.data.pop('user_id')
            serializer = UserObjectSearchExtendedSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
        except Object.DoesNotExist:
                return Response({
                "code": 400,
                "message": "Incorrect object_id"
                }, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({
            "code": 400,
            "message": "Incorrect user_id"
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            user_id = request.data.get('user_id')
            object_id = request.data.get('object_id')
            user = CustomUser.objects.get(id=user_id)
            object = Object.objects.get(id=object_id)
            request.data['user'] = request.data.pop('user_id')
            user_object_search = UserObjectSearch.objects.get(user=user_id, object_id=object_id)
            serializer = UserObjectSearchSerializer(user_object_search, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
        except Object.DoesNotExist:
            return Response({
            "code": 400,
            "message": "Incorrect object_id"
            }, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({
            "code": 400,
            "message": "Incorrect user_id"
            }, status=status.HTTP_400_BAD_REQUEST)
        except UserObjectSearch.DoesNotExist:
            return Response({
            "code": 400,
            "message": "Combination of user_id and object_id does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class User_list(generics.ListAPIView):

    def get(self, request):
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

class User_statistics(APIView):

    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            distance_sum = user.distance_sum
            unique_places_visited_count = UserObjectSearch.objects.filter(user=user_id).count()
            top_five_visited_places = UserObjectSearch.objects.filter(user=user_id).order_by('-route_created_count')[:5]
            serializer = UserObjectSearchSerializer(top_five_visited_places, many=True)
            return Response({
                    "code": 200,
                    "statistics":{
                        "distance_sum": distance_sum,
                        "unique_places_visited_count": unique_places_visited_count,
                        "top_five_visited_places": serializer.data
                        }
                    }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
                    return Response({
                        "code": 400,
                        "message": "Incorrect user_id"
                        }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            user_id = request.data.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            serializer = UserExtendedSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "code": 200,
                    "message": "Data updated"
                    }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": "Incorrect user_id"
                    }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "code": 500,
                "message": "Server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)