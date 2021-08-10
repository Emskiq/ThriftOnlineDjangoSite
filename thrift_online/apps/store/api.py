import json
import stripe

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCaptureRequest, OrdersGetRequest

from apps.cart.cart import Cart
from .models import Product
from .utils import decrement_product_quantity, send_order_conf_mail
from apps.order.models import Order, OrderItem
from apps.order.utils import checkout

def api_add_to_cart(request):
    data = json.loads(request.body)
    json_response = {'success' : True}
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    cart = Cart(request)

    product = get_object_or_404(Product, pk=product_id)

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)

    return JsonResponse(json_response)


def api_remove_from_cart(request):
    data = json.loads(request.body)
    json_response = {'success' : True}
    product_id = str(data['product_id'])

    cart = Cart(request)
    cart.remove(product_id)

    return JsonResponse(json_response)

def api_checkout(request):
    cart = Cart(request)

    data = json.loads(request.body)
    jsonresponse = {'success': True}
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zip_code = data['zip_code']
    city = data['city']
    phone = data['phone']
    office = data['office']
    
    orderid = checkout(request, first_name, last_name, email, address, zip_code, city, phone, office)

    paid = True

    if paid == True:
        order = Order.objects.get(pk=orderid)
        order.paid = True
        order.paid_amount = cart.get_total_cost()
        order.save()

        cart.clear()
    
    return JsonResponse(jsonresponse)

def create_checkout_session(request):
    cart = Cart(request)
    data = json.loads(request.body)

    items = []
    
    for item in cart:
        product = item['product']

        obj = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.title
                },
                'unit_amount': int(product.price * 100)
            },
            'quantity': item['quantity']
        }

        items.append(obj)
    
    gateway = data['gateway']
    session = ''
    order_id = ''
    payment_intent = ''

    #Stripe
    if (gateway == "stripe"):
        stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
        
        session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = items,
            mode = 'payment',
            success_url = 'http://127.0.0.1:8000/cart/success',
            cancel_url = 'http://127.0.0.1:8000/cart/'
        )
        payment_intent = session.payment_intent
        

    # Create order
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zip_code']
    city = data['city']
    phone = data['phone']
    office = data['office']

    orderid = checkout(request, first_name, last_name, email, address, zipcode, city, phone, office)

    delivery_price = data['deliveryPrice']
    total_price = 0.00 + delivery_price

    for item in cart:
        product = item['product']
        total_price = total_price + (float(product.price) * int(item['quantity']))

    order = Order.objects.get(pk=orderid)
    order.payment_intent = payment_intent
    order.paid_amount = total_price
    order.save()

    
    #payAtArrival
    if (gateway == 'atArr'):
        payment_intent = str(orderid) + "atArr"
        session = 'http://127.0.0.1:8000/cart/success'

        decrement_product_quantity(order)
        send_order_conf_mail(order)

    #Paypal
    if gateway == 'paypal':
        order_id = data['order_id']
        environment = SandboxEnvironment(client_id=settings.PAYPAL_API_KEY_PUBLISHABLE, client_secret=settings.PAYPAL_API_KEY_HIDDEN)
        client = PayPalHttpClient(environment)

        print(client)

        request = OrdersGetRequest(order_id)
        print(request)
        response = client.execute(request)

        order = Order.objects.get(pk=orderid)
        order.paid_amount = total_price
        order.paid_amount = total_price
        print(response)

        if response.result.status == 'COMPLETED':
            print(response.result.status)
            order.paid = True
            order.payment_intent = order_id
            order.save()

            decrement_product_quantity(order)
            send_order_conf_mail(order)
        else:
            order.paid = True
            order.save()

    return JsonResponse({'session': session})
