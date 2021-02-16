from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('cart/', views.cart, name='cart'),
    path('cart/quantity/', views.quantity, name='quantity')
]