from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/checkout/order/', views.order, name='order'),
    path('overview/', views.orderview, name='orderview')
]