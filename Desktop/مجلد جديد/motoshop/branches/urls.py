from django.urls import path
from . import views

urlpatterns = [
    path('', views.branch_list, name='branch_list'),
    path('<slug:slug>/', views.branch_detail, name='branch_detail'),
    path('types/', views.product_types, name='product_types'),
]
