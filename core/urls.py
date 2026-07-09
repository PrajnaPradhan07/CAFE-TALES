from django.urls import path
from .views import RegisterView, LoginView, CategoryView, MenuItemView, OrderView, OrderDetailView
urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('categories/', CategoryView.as_view(),name='categories'),
    path('menu/', MenuItemView.as_view(),name='menu'),
    path('orders/', OrderView.as_view(),name='orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(),name='order-detail' )

]