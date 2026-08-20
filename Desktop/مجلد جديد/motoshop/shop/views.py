from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Motorcycle, Category, Cart, CartItem, Order, OrderItem
from .forms import OrderForm, ContactForm
from .queryset_lab import build_queryset_report


def home(request):
    featured = Motorcycle.objects.filter(is_featured=True)[:6]
    latest = Motorcycle.objects.filter(is_new=True)[:8]
    categories = Category.objects.all()[:6]
    brands = dict(Motorcycle.BRAND_CHOICES)

    context = {
        'featured': featured,
        'latest': latest,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'shop/home.html', context)


def queryset_lab(request):
    """صفحة عملية توضح متطلبات واجب هندسة البرمجيات."""
    report = build_queryset_report()
    return render(request, 'shop/queryset_lab.html', {'report': report})


def product_list(request):
    motorcycles = Motorcycle.objects.all()

    # ✅ الفلاتر المطورة
    brand = request.GET.get('brand')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_cc = request.GET.get('min_cc')          # ⭐ فلتر سعة المحرك
    max_cc = request.GET.get('max_cc')          # ⭐ فلتر سعة المحرك
    min_year = request.GET.get('min_year')      # ⭐ فلتر سنة الصنع
    max_year = request.GET.get('max_year')      # ⭐ فلتر سنة الصنع
    color = request.GET.get('color')            # ⭐ فلتر اللون
    search = request.GET.get('search')
    sort = request.GET.get('sort')

    if brand:
        motorcycles = motorcycles.filter(brand=brand)
    if category:
        motorcycles = motorcycles.filter(category__slug=category)
    if min_price:
        motorcycles = motorcycles.filter(price__gte=min_price)
    if max_price:
        motorcycles = motorcycles.filter(price__lte=max_price)
    if min_cc:
        motorcycles = motorcycles.filter(engine_cc__gte=min_cc)
    if max_cc:
        motorcycles = motorcycles.filter(engine_cc__lte=max_cc)
    if min_year:
        motorcycles = motorcycles.filter(model_year__gte=min_year)
    if max_year:
        motorcycles = motorcycles.filter(model_year__lte=max_year)
    if color:
        motorcycles = motorcycles.filter(color__icontains=color)
    if search:
        motorcycles = motorcycles.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(brand__icontains=search) |
            Q(color__icontains=search)
        )

    # الترتيب
    if sort == 'price_asc':
        motorcycles = motorcycles.order_by('price')
    elif sort == 'price_desc':
        motorcycles = motorcycles.order_by('-price')
    elif sort == 'name':
        motorcycles = motorcycles.order_by('name')
    elif sort == 'newest':
        motorcycles = motorcycles.order_by('-created_at')
    elif sort == 'cc_asc':
        motorcycles = motorcycles.order_by('engine_cc')
    elif sort == 'cc_desc':
        motorcycles = motorcycles.order_by('-engine_cc')
    elif sort == 'year_asc':
        motorcycles = motorcycles.order_by('model_year')
    elif sort == 'year_desc':
        motorcycles = motorcycles.order_by('-model_year')

    # الترقيم
    paginator = Paginator(motorcycles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ⭐ ألوان متاحة للفلتر
    available_colors = Motorcycle.objects.values_list('color', flat=True).distinct().exclude(color='').exclude(color__isnull=True)

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'brands': Motorcycle.BRAND_CHOICES,
        'total_count': motorcycles.count(),
        'available_colors': available_colors,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    motorcycle = get_object_or_404(Motorcycle, slug=slug)
    motorcycle.views_count += 1
    motorcycle.save()

    related = Motorcycle.objects.filter(brand=motorcycle.brand).exclude(id=motorcycle.id)[:4]

    context = {
        'motorcycle': motorcycle,
        'related': related,
        'images': motorcycle.images.all(),
    }
    return render(request, 'shop/product_detail.html', context)


@login_required
def add_to_cart(request, slug):
    motorcycle = get_object_or_404(Motorcycle, slug=slug)

    if motorcycle.stock < 1:
        messages.error(request, 'عذراً، هذه الدراجة غير متوفرة حالياً')
        return redirect('product_detail', slug=slug)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, motorcycle=motorcycle)

    if not created:
        if cart_item.quantity < motorcycle.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'تمت زيادة الكمية لـ {motorcycle.name}')
        else:
            messages.warning(request, 'لقد وصلت للحد الأقصى من المخزون')
    else:
        messages.success(request, f'تمت إضافة {motorcycle.name} إلى السلة')

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'تم حذف العنصر من السلة')
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0 and quantity <= cart_item.motorcycle.stock:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'تم تحديث الكمية')
    elif quantity > cart_item.motorcycle.stock:
        messages.error(request, 'الكمية المطلوبة غير متوفرة')
    else:
        cart_item.delete()
        messages.success(request, 'تم حذف العنصر')

    return redirect('cart')


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    context = {'cart': cart}
    return render(request, 'shop/cart.html', context)


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, 'سلة التسوق فارغة')
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = cart.get_total()
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    motorcycle=item.motorcycle,
                    quantity=item.quantity,
                    price=item.motorcycle.price
                )
                item.motorcycle.stock -= item.quantity
                item.motorcycle.save()

            cart.items.all().delete()
            messages.success(request, f'تم إرسال طلبك بنجاح! رقم الطلب: #{order.id}')
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'shop/checkout.html', context)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/my_orders.html', {'orders': orders})


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'تم إرسال رسالتك بنجاح! سنتواصل معك قريباً')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})
