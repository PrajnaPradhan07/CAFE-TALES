from django.contrib import admin
from .models import User, Category, MenuItem, Order, OrderItem

admin.site.register(User)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
