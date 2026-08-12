from django.shortcuts import render, get_object_or_404
from .models import Branch, ProductType


def branch_list(request):
    branches = Branch.objects.filter(is_active=True)
    cities = Branch.objects.filter(is_active=True).values_list('city', flat=True).distinct()

    city = request.GET.get('city')
    if city:
        branches = branches.filter(city=city)

    return render(request, 'branches/branch_list.html', {
        'branches': branches,
        'cities': cities,
    })


def branch_detail(request, slug):
    branch = get_object_or_404(Branch, slug=slug, is_active=True)
    inventory = branch.inventory.select_related('motorcycle').all()
    return render(request, 'branches/branch_detail.html', {
        'branch': branch,
        'inventory': inventory,
    })


def product_types(request):
    types = ProductType.objects.filter(is_active=True)
    return render(request, 'branches/product_types.html', {'types': types})
