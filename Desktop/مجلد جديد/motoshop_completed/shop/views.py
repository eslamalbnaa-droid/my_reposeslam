from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.db import transaction
from django.db.models import Q, F, Avg, Count
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from .models import Motorcycle, Category, Cart, CartItem, Order, OrderItem, Favorite, Review, SentEmail
from .forms import OrderForm, ContactForm, ReviewForm, MotorcycleForm, AdminUserEmailForm
from .queryset_lab import build_queryset_report


def admin_permission_required(permission):
    """يسمح فقط لمستخدمي لوحة الإدارة الذين يملكون صلاحية Django المطلوبة."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(request, *args, **kwargs):
            if not request.user.is_staff or not request.user.has_perm(permission):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator


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
    motorcycles = Motorcycle.objects.annotate(avg_rating=Avg('reviews__rating'), reviews_count=Count('reviews', distinct=True))

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

    def number_or_none(value, kind=float):
        try:
            return kind(value) if value not in (None, '') else None
        except (TypeError, ValueError):
            return None

    min_price = number_or_none(min_price)
    max_price = number_or_none(max_price)
    min_cc = number_or_none(min_cc, int)
    max_cc = number_or_none(max_cc, int)
    min_year = number_or_none(min_year, int)
    max_year = number_or_none(max_year, int)

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
    else:
        motorcycles = motorcycles.order_by('-created_at')

    # الترقيم
    paginator = Paginator(motorcycles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ⭐ ألوان متاحة للفلتر
    available_colors = Motorcycle.objects.values_list('color', flat=True).distinct().exclude(color='').exclude(color__isnull=True)

    filters_query = request.GET.copy()
    filters_query.pop('page', None)
    sort_query = filters_query.copy()
    sort_query.pop('sort', None)

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'brands': Motorcycle.BRAND_CHOICES,
        'total_count': motorcycles.count(),
        'available_colors': available_colors,
        'filters_query': filters_query.urlencode(),
        'sort_query': sort_query.urlencode(),
        'current_sort': sort or '',
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    motorcycle = get_object_or_404(Motorcycle, slug=slug)
    Motorcycle.objects.filter(pk=motorcycle.pk).update(views_count=F('views_count') + 1)
    motorcycle.refresh_from_db(fields=['views_count'])

    related = Motorcycle.objects.filter(brand=motorcycle.brand).exclude(id=motorcycle.id)[:4]
    reviews = motorcycle.reviews.select_related('user').all()
    rating_summary = reviews.aggregate(average=Avg('rating'), count=Count('id'))
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    context = {
        'motorcycle': motorcycle,
        'related': related,
        'images': motorcycle.images.all(),
        'reviews': reviews,
        'rating_average': rating_summary['average'] or 0,
        'reviews_count': rating_summary['count'],
        'review_form': ReviewForm(instance=user_review),
        'user_review': user_review,
    }
    return render(request, 'shop/product_detail.html', context)


@login_required
def add_review(request, slug):
    motorcycle = get_object_or_404(Motorcycle, slug=slug)
    existing = Review.objects.filter(user=request.user, motorcycle=motorcycle).first()
    if request.method != 'POST':
        return redirect('product_detail', slug=slug)

    form = ReviewForm(request.POST, instance=existing)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.motorcycle = motorcycle
        review.save()
        messages.success(request, 'تم حفظ تقييمك بنجاح')
    else:
        messages.error(request, 'تعذر حفظ التقييم. تأكد من البيانات المدخلة.')
    return redirect('product_detail', slug=slug)


@login_required
def delete_review(request, slug):
    review = get_object_or_404(Review, motorcycle__slug=slug, user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.info(request, 'تم حذف تقييمك')
    return redirect('product_detail', slug=slug)


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
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        messages.error(request, 'الكمية المدخلة غير صحيحة')
        return redirect('cart')

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
            with transaction.atomic():
                cart_items = list(cart.items.select_related('motorcycle'))
                locked_motorcycles = {
                    motorcycle.pk: motorcycle
                    for motorcycle in Motorcycle.objects.select_for_update().filter(
                        pk__in=[item.motorcycle_id for item in cart_items]
                    )
                }

                for item in cart_items:
                    motorcycle = locked_motorcycles[item.motorcycle_id]
                    if item.quantity > motorcycle.stock:
                        messages.error(
                            request,
                            f'الكمية المطلوبة من {motorcycle.name} لم تعد متوفرة. المتاح حالياً: {motorcycle.stock}'
                        )
                        return redirect('cart')

                order = form.save(commit=False)
                order.user = request.user
                order.total = sum(
                    locked_motorcycles[item.motorcycle_id].price * item.quantity
                    for item in cart_items
                )
                order.save()

                for item in cart_items:
                    motorcycle = locked_motorcycles[item.motorcycle_id]
                    OrderItem.objects.create(
                        order=order,
                        motorcycle=motorcycle,
                        quantity=item.quantity,
                        price=motorcycle.price
                    )
                    motorcycle.stock -= item.quantity
                    motorcycle.save(update_fields=['stock'])

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
    orders = Order.objects.filter(user=request.user).prefetch_related('items__motorcycle')
    paginator = Paginator(orders, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'shop/my_orders.html', {'orders': page_obj, 'page_obj': page_obj})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__motorcycle'),
        id=order_id,
        user=request.user,
    )
    status_steps = [
        ('pending', 'قيد الانتظار'),
        ('processing', 'قيد المعالجة'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التوصيل'),
    ]
    status_order = {key: i for i, (key, _) in enumerate(status_steps)}
    current_index = status_order.get(order.status, -1)
    timeline = [
        {'key': key, 'label': label, 'done': current_index >= i and order.status != 'cancelled'}
        for i, (key, label) in enumerate(status_steps)
    ]
    return render(request, 'shop/order_detail.html', {'order': order, 'timeline': timeline})


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            site_email = (getattr(settings, 'CONTACT_EMAIL', '') or settings.EMAIL_HOST_USER).strip()
            if not site_email or not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                messages.error(
                    request,
                    'تعذر إرسال الرسالة لأن Gmail غير مضبوط بالكامل. أضف EMAIL_HOST_USER وEMAIL_HOST_PASSWORD (App Password) داخل ملف .env.',
                )
                return render(request, 'shop/contact.html', {'form': form})

            name = form.cleaned_data['name']
            visitor_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['message']

            admin_body = (
                f'رسالة جديدة من نموذج تواصل معنا في MotoShop Yemen\n\n'
                f'الاسم: {name}\n'
                f'البريد: {visitor_email}\n'
                f'الموضوع: {subject}\n\n'
                f'الرسالة:\n{body}\n'
            )

            try:
                # الرسالة الأساسية تصل إلى بريد الموقع، والرد عليها يذهب مباشرة لبريد الزائر.
                EmailMessage(
                    subject=f'[MotoShop] {subject}',
                    body=admin_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[site_email],
                    reply_to=[visitor_email],
                ).send(fail_silently=False)

                # تأكيد بسيط للزائر بأن رسالته وصلت للموقع.
                send_mail(
                    subject='تم استلام رسالتك - MotoShop Yemen',
                    message=(
                        f'مرحباً {name}،\n\n'
                        'تم استلام رسالتك بنجاح وسنتواصل معك في أقرب وقت.\n\n'
                        f'موضوع رسالتك: {subject}\n\n'
                        'MotoShop Yemen'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[visitor_email],
                    fail_silently=False,
                )
            except Exception:
                messages.error(
                    request,
                    'لم يتم إرسال الرسالة. تأكد من اتصال الإنترنت وإعداد EMAIL_HOST_USER وApp Password داخل ملف .env ثم حاول مرة أخرى.',
                )
                return render(request, 'shop/contact.html', {'form': form})

            messages.success(request, 'تم إرسال رسالتك إلى بريد الموقع، وتم إرسال تأكيد إلى بريدك الإلكتروني.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})


@login_required
def favorites(request):
    favorite_records = (
        Favorite.objects.filter(user=request.user)
        .select_related('motorcycle', 'motorcycle__category')
    )
    return render(request, 'shop/favorites.html', {'favorite_records': favorite_records})


@login_required
def toggle_favorite(request, slug):
    motorcycle = get_object_or_404(Motorcycle, slug=slug)

    if request.method != 'POST':
        return redirect('product_detail', slug=slug)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        motorcycle=motorcycle,
    )
    if created:
        messages.success(request, f'تمت إضافة {motorcycle.name} إلى المفضلة')
    else:
        favorite.delete()
        messages.info(request, f'تمت إزالة {motorcycle.name} من المفضلة')

    next_url = request.POST.get('next')
    return redirect(next_url) if next_url else redirect('product_detail', slug=slug)


@admin_permission_required('shop.view_motorcycle')
def manage_products(request):
    products = Motorcycle.objects.select_related('category').all()
    search = request.GET.get('search', '').strip()
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(brand__icontains=search) | Q(category__name__icontains=search)
        )
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'shop/manage_products.html', {'page_obj': page_obj, 'search': search})


@admin_permission_required('shop.add_motorcycle')
def product_create(request):
    if request.method == 'POST':
        form = MotorcycleForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'تمت إضافة {product.name} بنجاح.')
            return redirect('manage_products')
    else:
        form = MotorcycleForm()
    return render(request, 'shop/product_form.html', {'form': form, 'page_title': 'إضافة منتج جديد', 'submit_text': 'إضافة المنتج'})


@admin_permission_required('shop.change_motorcycle')
def product_update(request, pk):
    product = get_object_or_404(Motorcycle, pk=pk)
    if request.method == 'POST':
        form = MotorcycleForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'تم تحديث {product.name} بنجاح.')
            return redirect('manage_products')
    else:
        form = MotorcycleForm(instance=product)
    return render(request, 'shop/product_form.html', {
        'form': form, 'product': product, 'page_title': 'تعديل المنتج', 'submit_text': 'حفظ التعديلات'
    })


@admin_permission_required('shop.delete_motorcycle')
def product_delete(request, pk):
    product = get_object_or_404(Motorcycle, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'تم حذف {name} بنجاح.')
        return redirect('manage_products')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})


@login_required
def send_user_email(request):
    """واجهة داخل الموقع لإرسال بريد حقيقي لمستخدم مسجل، للأدمن فقط."""
    if not request.user.is_staff:
        raise PermissionDenied

    email_ready = bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD)

    if request.method == 'POST':
        form = AdminUserEmailForm(request.POST)
        if form.is_valid():
            if not email_ready:
                messages.error(
                    request,
                    'الإرسال الحقيقي غير جاهز. ضع EMAIL_HOST_USER وEMAIL_HOST_PASSWORD (App Password) داخل ملف .env ثم أعد تشغيل السيرفر.',
                )
                recent_emails = SentEmail.objects.select_related('sender', 'recipient_user')[:20]
                return render(request, 'shop/send_user_email.html', {
                    'form': form,
                    'recent_emails': recent_emails,
                    'email_ready': email_ready,
                })

            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject'].strip()
            body = form.cleaned_data['message'].strip()

            log = SentEmail.objects.create(
                sender=request.user,
                recipient_user=recipient,
                recipient_email=recipient.email,
                subject=subject,
                message=body,
                status='failed',
            )

            try:
                email = EmailMessage(
                    subject=f'MotoShop Yemen - {subject}',
                    body=(
                        f'مرحباً {recipient.get_full_name().strip() or recipient.username}،\n\n'
                        f'{body}\n\n'
                        'مع تحيات فريق MotoShop Yemen'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient.email],
                    reply_to=[getattr(settings, 'CONTACT_EMAIL', '') or settings.EMAIL_HOST_USER],
                )
                email.send(fail_silently=False)
            except Exception as exc:
                log.error_message = str(exc)[:2000]
                log.save(update_fields=['error_message'])
                messages.error(
                    request,
                    'فشل إرسال البريد. تأكد من الإنترنت وإعداد Gmail وApp Password داخل .env.',
                )
            else:
                log.status = 'sent'
                log.error_message = ''
                log.save(update_fields=['status', 'error_message'])
                messages.success(request, f'تم إرسال الرسالة إلى {recipient.email} بنجاح.')
                return redirect('send_user_email')
    else:
        form = AdminUserEmailForm()

    recent_emails = SentEmail.objects.select_related('sender', 'recipient_user')[:20]
    return render(request, 'shop/send_user_email.html', {
        'form': form,
        'recent_emails': recent_emails,
        'email_ready': email_ready,
    })
