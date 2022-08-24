from django.contrib.auth import get_user_model, authenticate, login
from django.urls import is_valid_path
from django.shortcuts import redirect, render
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse



from .serializers import *

User = get_user_model()

class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Account created', 201)

@api_view(['GET'])
def activate(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()
    return redirect('http://127.0.0.1:3000/')




# class LoginView(TokenObtainPairView):
#     serializer_class = LoginSerializer

# class LogoutAPIView(GenericAPIView):
#     serializer_class = LogoutSerializer
#     permission_classes = [IsAuthenticated, ]

#     def post(self, request):
#         serializers = self.serializer_class(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(
#             {"msg":"You successfully logged out"}, 
#             status=status.HTTP_204_NO_CONTENT
#         )
    

