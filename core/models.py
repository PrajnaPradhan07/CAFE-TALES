from django.db import models
from django.contrib.auth.models import AbstractUser #django.contrib.auth is django's builtin login/authentication system

#--CUSTOM USER--
class User(AbstractUser):
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)
    loyalty_points = models.IntegerField(default=0)

    def __str__(self):
        return self.username

#--CATEGORY--
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#--MENU ITEM--
class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_images/',blank=True,null=True)

    def __str__(self):
        return self.name

#--ORDER--
class Order(models.Model):
    STATUS_CHOICE = [
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('preparing','Preparing'),
        ('delivered','Delivered'),
        ('Cancelled','Cancelled')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders')
    status = models.CharField(max_length=20,choices=STATUS_CHOICE, default='pending')
    created_at = models.DateTimeField(auto_now_add = True)
    total_price = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

#--ORDER ITEM--
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"