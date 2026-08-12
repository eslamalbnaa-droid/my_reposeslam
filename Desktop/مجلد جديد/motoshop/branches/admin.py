from django.contrib import admin
from .models import Branch, ProductType, BranchInventory


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'manager_name', 'is_active', 'created_at']
    list_filter = ['city', 'is_active']
    search_fields = ['name', 'address', 'manager_name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BranchInventory)
class BranchInventoryAdmin(admin.ModelAdmin):
    list_display = ['branch', 'motorcycle', 'quantity', 'last_updated']
    list_filter = ['branch']
    search_fields = ['branch__name', 'motorcycle__name']
