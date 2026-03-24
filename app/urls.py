from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('search/', views.search, name="search"),
    path('category/', views.category_view, name='category_all'),
    path('category/<str:category_slug>/', views.category_view, name='category'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('logout/', views.logoutPage, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('cancel-order/<int:order_id>/', views.cancel_order, name="cancel_order"),
    path('my-orders/', views.user_orders, name="user_orders"),
    path('order-detail/<int:order_id>/', views.order_detail, name="order_detail"),
    path('checkout/', views.checkout, name="checkout"),
    path('payment/<int:order_id>/', views.payment_gateway, name="payment_gateway"),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('update_item/', views.updateItem, name="update_item"),
    path("api/suggest/", views.search_suggestions, name="search_suggestions"),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]