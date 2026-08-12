from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'is_verified', 'is_staff', 'date_joined']
    list_filter = ['is_verified', 'is_staff', 'gender', 'date_joined']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('معلومات إضافية', {
            'fields': ('phone', 'address', 'city', 'gender', 'birth_date', 'avatar', 'is_verified')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_brand', 'notifications_enabled']
    search_fields = ['user__username', 'favorite_brand']
