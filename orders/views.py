from django.shortcuts import render, redirect
from products.models import Product
from consumers.models import Customer
from orders.models import Order
from orders.middlewares.auth import auth_middleware

# Create your views here.
def checkout(request):
    return render(request, 'checkout.html')

@auth_middleware
def order(request):
    address = request.POST.get('address')
    customer_id = request.session.get('customer')
    customer = Customer.objects.get(id=customer_id)
    cart = request.session.get('cart')
    products = Product.objects.filter(id__in=list(cart.keys()))
    for product in products:
        order = Order(customer=customer, product=product, 
        quantity=cart[str(product.id)], price=product.price, address=address)
        order.save()
    request.session['cart'] = {}
    return redirect('orders:orderview')

@auth_middleware
def orderview(request):
    customer_id = request.session.get('customer')
    orders = Order.objects.filter(customer=customer_id).order_by('-date')
    return render(request, 'order.html', {'orders': orders})