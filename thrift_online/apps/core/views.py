from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.mail import message, send_mail

from apps.store.models import Category, Product

def frontpage(request):
    men_category = Category.objects.get(slug='men')
    women_category = Category.objects.get(slug='women')

    recently_added_products = Product.objects.all().order_by('-date_added')[0:12]
    ra_products_paginator = Paginator(recently_added_products,12)
    ra_page = ra_products_paginator.get_page(1)

    popular_products = Product.objects.all().order_by('num_visits')[0:6]
    poplar_products_paginator = Paginator(popular_products,6)
    popular_page = poplar_products_paginator.get_page(1)

    context = {
        'men_category' : men_category,
        'women_category' : women_category,
        'recently_added_products' : recently_added_products,
        'popular_page' : popular_page,
        'ra_page' : ra_page,
    }

    return render(request, 'frontpage.html', context)

def contacts(request):
    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_subject = request.POST['message-subject'] + ' from ' + message_name
        message_email = request.POST['message-email']
        message = request.POST['message']

        if message_subject == '':
            message_subject = '(no subject)Message from ' + message_name
        
        message_subject.encode('utf-8')

        send_mail(
            message_subject,
            message,
            message_email,
            ['emiltsanev2001@gmail.com'],
        )

    return render(request, 'contacts.html')

def terms(request):
    return render(request, 'terms.html')

def biscuits(request):
    return render(request, 'biscuits.html')

def declaration(request):
    return render(request, 'declaration.html')