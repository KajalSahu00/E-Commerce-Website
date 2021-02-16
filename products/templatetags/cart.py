from django import template

register = template.Library()

@register.filter
def product_quantity(product_id, cart):
    return cart[str(product_id)]

@register.filter
def total_price(products, cart):
    sum = 0
    for product in products:
        sum += product.price * cart[str(product.id)]
    return sum
