from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User,Category,MenuItem,Order,OrderItem
from .serializers import UserSerializer,RegisterSerializer,CategorySerializer,MenuItemSerializer,OrderSerializer,OrderItemSerializer

#Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully!',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username,password = password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message':'Login successful!',
                'access':str(refresh.access_token),
                'refresh':str(refresh),
                'user': UserSerializer(user).data
            },status = status.HTTP_200_OK)
        return Response({'error':'Invalid credentials'},status = status.HTTP_401_UNAUTHORIZED)

#Category View
class CategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Menu item view
class MenuItemView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        items = MenuItem.objects.filter(is_available = True)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)







