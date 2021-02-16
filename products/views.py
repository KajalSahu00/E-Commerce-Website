from django.shortcuts import render, HttpResponse, redirect
from products.models import Product, Category
from django.views import View
from django.contrib import messages

# Create your views here.
class index(View):
    def get(self, request):
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.objects.filter(product_category=category_id)
        else:
            products = Product.objects.all()
        return render(request, 'index.html', {'products': products, 'categories': categories})
    
    def post(self, request):
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                cart[product_id] += 1
            else:
                cart[product_id] = 1
        else:
            cart = {}
            cart[product_id] = 1
        request.session['cart'] = cart
        messages.success(request, 'This item added successfully in your cart.')
        return redirect('products:index')

def cart(request):
    cart = request.session.get('cart')
    if cart:
        product_ids_list = list(cart.keys())
        products = Product.objects.filter(id__in=product_ids_list)
        return render(request, 'cart.html', {'cart': cart, 'products': products})
    messages.info(request, 'Your cart is empty.')
    return redirect('products:index')

def quantity(request):
    sign = request.POST.get('change_quantity')
    cart = request.session.get('cart')
    product_id = request.POST.get('product_id')
    if sign == '-':
        cart[str(product_id)] -= 1
    else:
        cart[str(product_id)] += 1
    if cart[str(product_id)] <= 0:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('products:cart')