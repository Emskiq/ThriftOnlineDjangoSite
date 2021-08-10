from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views

from . import settings
from apps.core.views import frontpage, contacts, terms, declaration, biscuits
from apps.store.views import product_detail, category_detail, search, all_products
from apps.store.api import api_add_to_cart, api_remove_from_cart, api_checkout, create_checkout_session
from apps.cart.views import cart_detail, success
from apps.cart.webhooks import webhook
from apps.order.views import admin_order_pdf
from apps.userprofile.views import  signup, myaccount

urlpatterns = [
    #Core
    path('', frontpage, name="frontpage"),
    path('contacts/', contacts, name="contacts"),
    path('terms/', terms, name="terms"),
    path('declaration/', declaration, name="declaration"),
    path('biscuits/', biscuits, name="biscuits"),
    path('admin/admin_order_pdf/<int:order_id>/', admin_order_pdf, name="admin_order_pdf"),
    path('admin/', admin.site.urls),

    #API
    path('api/create_checkout_session/', create_checkout_session, name = 'create_checkout_session'),
    path('api/add_to_cart/', api_add_to_cart, name="api_add_to_cart"),
    path('api/remove_from_cart/', api_remove_from_cart, name="api_remove_from_cart"),
    path('api/checkout/', api_checkout, name="api_checkout"),

    #Cart
    path('cart/', cart_detail, name="cart"),
    path('hooks/', webhook, name="webhook"),
    path('cart/success/', success, name="success"),

    #Users
    path('myaccount/', myaccount, name="myaccount"),
    path('signup/', signup, name="signup"),
    path('login/', views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), 
        name='password_change_done'),
    path('password_change/', views.PasswordChangeView.as_view(template_name='password_change.html'), 
        name='password_change'),
    path('password_reset/done/', views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
    
    #Store items
    path('search/', search, name="search"),
    path('all_products/', all_products, name="all_products"),
    path('<slug:category_slug>/<slug:slug>/', product_detail, name="product_detail"),
    path('<slug:slug>/', category_detail, name="category_detail"), 
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
