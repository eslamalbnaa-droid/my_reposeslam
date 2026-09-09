from django.db.models import Avg, Count, Max, Min

from .models import Motorcycle, Category


def build_queryset_report():
    """
    مثال عملي يحقق متطلبات الواجب باستخدام QuerySet APIs.

    الدوال المستخدمة هنا أكثر من 7: all, filter, exclude, order_by,
    values, annotate, distinct, count, exists, aggregate,
    select_related, prefetch_related.
    """
    all_motorcycles = Motorcycle.objects.all()

    available_motorcycles = Motorcycle.objects.filter(stock__gt=0)

    non_new_motorcycles = Motorcycle.objects.exclude(is_new=True)

    expensive_motorcycles = Motorcycle.objects.filter(price__gte=5000).order_by('-price')[:10]

    categories = Category.objects.values('id', 'name').order_by('name')

    brand_stats = (
        Motorcycle.objects
        .values('brand')
        .annotate(total=Count('id'), average_price=Avg('price'))
        .order_by('-total', 'brand')
    )

    colors = (
        Motorcycle.objects
        .exclude(color='')
        .values_list('color', flat=True)
        .distinct()
        .order_by('color')
    )

    total_count = all_motorcycles.count()
    has_stock = available_motorcycles.exists()

    price_summary = Motorcycle.objects.aggregate(
        average_price=Avg('price'),
        minimum_price=Min('price'),
        maximum_price=Max('price'),
    )

    optimized_motorcycles = (
        Motorcycle.objects
        .select_related('category')
        .prefetch_related('images')
        .order_by('-created_at')[:6]
    )

    return {
        'total_count': total_count,
        'available_count': available_motorcycles.count(),
        'non_new_count': non_new_motorcycles.count(),
        'has_stock': has_stock,
        'expensive_motorcycles': expensive_motorcycles,
        'categories': categories,
        'brand_stats': brand_stats,
        'colors': colors,
        'price_summary': price_summary,
        'optimized_motorcycles': optimized_motorcycles,
    }
