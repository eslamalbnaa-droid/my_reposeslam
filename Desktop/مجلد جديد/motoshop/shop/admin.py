from django.contrib import admin
from .models import Category, Motorcycle, MotorcycleImage, Cart, CartItem, Order, OrderItem


class MotorcycleImageInline(admin.TabularInline):
    model = MotorcycleImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'stock', 'is_featured', 'is_new', 'created_at']
    list_filter = ['brand', 'is_featured', 'is_new', 'category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_featured', 'is_new']
    inlines = [MotorcycleImageInline]
    date_hierarchy = 'created_at'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_items_count', 'get_total', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'motorcycle', 'quantity', 'get_subtotal']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['motorcycle', 'quantity', 'price', 'get_subtotal']
    extra = 0
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_address']
    readonly_fields = ['created_at', 'updated_at', 'total']
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
