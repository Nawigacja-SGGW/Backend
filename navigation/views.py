from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from .models import User


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
    return Response({})

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    #return Response({ 'tu jeszcze dzila' })
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    return Response({})

# do usuniecia po przetestowaniu
@api_view(['GET'])
def test(request):
    return Response({})

