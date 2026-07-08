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

#Order View
class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many =True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        items_data = request.data.get('items',[])
        if not items_data :
            return Response({'error':'No items provided'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)
        total = 0

        for item_data in items_data:
            menu_item = MenuItem.objects.get(id=item_data['menu_item'])
            quantity = item_data.get('quantity',1)
            price = menu_item.price * quantity
            total += price
            OrderItem.objects.create(
                order=order,
                menu_item = menu_item,
                quantity = quantity,
                price = price
            )

        order.total_price =total
        order.save()

        #add loyalty points (1 point for 10 rupees)
        request.user.loyalty_points += int(total//10)
        request.user.save()

        serializer = OrderSerializer(order)
        return Response({
            'message':'Order placed successfully',
            'order':serializer.data
        }, status = status.HTTP_201_CREATED)

#Order Detail View
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            order = Order.objects.get(id=pk,user =request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error':'Order not found'},status=status.HTTP_404_NOT_FOUND)







