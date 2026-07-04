from rest_framework import serializers
from .models import User, Category, MenuItem, Order, OrderItem

#USER SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','username','email','phone','loyalty_points']

#REGISTER SERIALIZER
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','phone','password']

    def create(self,validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            phone = validated_data['phone'],
            password = validated_data['password']
        )
        return user

#CATEGORY SERIALIZER
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

#MENU_ITEM SERIALIZER
class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name',read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','name','description','price','is_available','image','category','category_name']

#ORDER ITEM SERIALIZER
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name',read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','menu_item','menu_item_name','quantity','price']

#ORDER SERIALIZER
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True, read_only = True)

    class Meta:
        model = Order
        fields = ['id','user','status','created_at','total_price','items']