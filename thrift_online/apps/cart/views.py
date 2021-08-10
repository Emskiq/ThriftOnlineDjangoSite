from django.shortcuts import render
from django.conf import settings

from .cart import Cart

def cart_detail(request):
    cart = Cart(request)

    products_string = ''

    for item in cart:
        product = item['product']
        url = '/%s/%s/' % (product.category.slug, product.slug)
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'url': '%s'}, " % (product.id, product.title, product.price, item['quantity'], item['total_price'], product.get_thumbnail() , url)
        products_string += b

    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        address = request.user.userprofile.address
        zip_code = request.user.userprofile.zip_code
        city = request.user.userprofile.city
        phone = request.user.userprofile.phone
    else:
        first_name = last_name = email = address = zip_code = city = phone = ''

    context = {
        'cart' : cart,
        'first_name' : first_name,
        'last_name' : last_name,
        'email' : email,
        'address' : address,
        'zip_code' : zip_code,
        'city' : city,
        'phone' : phone,
        'pub_key_stripe' : settings.STRIPE_API_KEY_PUBLISHABLE,
        'pub_key_paypal' : settings.PAYPAL_API_KEY_PUBLISHABLE,
        'products_string' : products_string,
    }

    return render(request, 'cart.html', context )

def success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "success.html")