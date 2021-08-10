from .models import Category
from django.shortcuts import get_object_or_404

def menu_categories(request):
    women_category = get_object_or_404(Category, slug='women')
    men_category = get_object_or_404(Category, slug='men')

    context = {
        'women_category' : women_category,
        'men_category' : men_category,
    }

    return context