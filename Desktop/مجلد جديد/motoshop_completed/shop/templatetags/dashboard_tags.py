from django import template
from django.contrib.auth import get_user_model
from django.db.models import Sum
from shop.models import Motorcycle, Order, Review

register = template.Library()

@register.simple_tag
def admin_dashboard_stats():
    User = get_user_model()
    revenue = Order.objects.exclude(status='cancelled').aggregate(total=Sum('total'))['total'] or 0
    return {
        'users': User.objects.count(),
        'motorcycles': Motorcycle.objects.count(),
        'orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'reviews': Review.objects.count(),
        'revenue': revenue,
    }
