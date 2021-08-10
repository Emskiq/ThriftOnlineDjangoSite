import datetime
import os

from random import randint

from apps.cart.cart import Cart

from apps.order.models import Order, OrderItem

def checkout(request, first_name, last_name, email, address, zip_code, city, phone, office):
    order = Order(first_name=first_name, last_name=last_name, email=email, address=address, zip_code=zip_code, city=city, phone=phone, office = office)
    
    if request.user.is_authenticated:
        order.user = request.user
    
    order.save()

    cart = Cart(request)

    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

    return order.id