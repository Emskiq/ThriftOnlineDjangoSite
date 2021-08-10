from django.test import TestCase

def cart(request):
    return render(request, 'cart.html')