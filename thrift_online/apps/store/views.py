import random
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Category, Product
from apps.cart.cart import Cart

PRODUCTS_PAR_PAGE = 6

def category_detail(request,slug):
    category = get_object_or_404(Category, slug=slug)
    category_childrens = category.children.all()
    products = category.products.all()

    if 'query' in request.GET:
        price_from = request.GET.get('price_from', -9797979)
        price_to = request.GET.get('price_to', 9797979)
        sorting = request.GET.get('sorting', '-date_added')
        query = request.GET.get('query', '')
        instock = request.GET.get('instock')

        if price_from == '':
            price_from = -9797979
        if price_to == '':
            price_to = 9797979

    else:
        price_from = -9797979
        price_to = 9797979
        sorting = '-date_added'
        query = ''
        instock = False

    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(price__gte=price_from).filter(price__lte=price_to).filter(category=category)

    for c in category_childrens:
        products |= Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(price__gte=price_from).filter(price__lte=price_to).filter(category=c)

    products = products.order_by(sorting)
        
    if instock:
        products = products.filter(num_available__gte=1)

    products_paginator = Paginator(products,PRODUCTS_PAR_PAGE)
    page_num = request.GET.get('page', 1)
    page_obj = products_paginator.get_page(page_num)

    context = {
        'category' : category,
        'query': query,
        'instock': instock,
        'products': products,
        'price_from': price_from,
        'price_to': price_to,
        'page_obj': page_obj,
        'products_paginator': products_paginator,
        'sorting': sorting,
    }

    return render(request, 'category_view.html', context)


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    product.num_visits += 1
    product.last_visit = datetime.now()
    product.super_save()
    
    related_products = list(product.category.products.filter().exclude(id=product.id))
    
    if len(related_products) >= 6:
        related_products = random.sample(related_products, 6)
    
    related_products_paginator = Paginator(related_products,12)
    related_products_page = related_products_paginator.get_page(1)

    cart = Cart(request)

    imagesstring = "{'thumbnail' : '%s', 'image': '%s'}," % (product.get_thumbnail(), product.get_image())
    for image in product.images.all():
        imagesstring = imagesstring + ("{'thumbnail' : '%s', 'image': '%s',}," % (image.get_thumbnail(), image.get_image()))
    
    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False

    context = {
        'product' : product,
        'imagesstring' : imagesstring,
        'related_products_page' : related_products_page,
    } 

    return render(request, 'product_detail.html', context)


def search(request):
    price_from = request.GET.get('price_from', -9797979)
    price_to = request.GET.get('price_to', 9797979)
    sorting = request.GET.get('sorting', '-date_added')
    query = request.GET.get('query', '')
    instock = request.GET.get('instock')

    if price_from == '':
        price_from = -9797979
    if price_to == '':
        price_to = 9797979

    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(price__gte=price_from).filter(price__lte=price_to)
    products = products.order_by(sorting)

    if instock:
        products = products.filter(num_available__gte=1)

    products_paginator = Paginator(products,PRODUCTS_PAR_PAGE)
    page_num = request.GET.get('page')

    try:
        page_obj= products_paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = products_paginator.page(1)
    except EmptyPage:
        page_obj = products_paginator.page(products_paginator.num_pages)


    context = {
        'query': query,
        'instock': instock,
        'products': products,
        'price_from': price_from,
        'price_to': price_to,
        'page_obj': page_obj,
        'products_paginator': products_paginator,
        'sorting': sorting,
    }


    return render(request, 'search.html', context)

def all_products(request):
    products = Product.objects.all().order_by('-date_added')

    products_paginator = Paginator(products,PRODUCTS_PAR_PAGE)
    page_num = request.GET.get('page', 1)
    page_obj = products_paginator.get_page(page_num)
    
    context = {
        'products' : products,
        'page_obj' : page_obj,
        'products_paginator' : products_paginator,
    } 
    return render(request, 'all_products.html', context)