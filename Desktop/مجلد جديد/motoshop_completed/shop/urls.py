from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.product_list, name='product_list'),
    path('shop/queryset-lab/', views.queryset_lab, name='queryset_lab'),
    path('management/products/', views.manage_products, name='manage_products'),
    path('management/email-users/', views.send_user_email, name='send_user_email'),
    path('management/products/add/', views.product_create, name='product_create'),
    path('management/products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('management/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('shop/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/<slug:slug>/review/', views.add_review, name='add_review'),
    path('shop/<slug:slug>/review/delete/', views.delete_review, name='delete_review'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/toggle/<slug:slug>/', views.toggle_favorite, name='toggle_favorite'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
