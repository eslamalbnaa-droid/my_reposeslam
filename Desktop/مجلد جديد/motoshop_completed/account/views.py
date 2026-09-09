from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm, UserProfileForm
from .models import UserProfile
from shop.models import Order


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'مرحباً {user.username}! تم إنشاء حسابك بنجاح.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'مرحباً بعودتك {user.username}!')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح.')
    return redirect('home')


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)[:5]
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    stats = {
        'orders_count': request.user.orders.count(),
        'favorites_count': request.user.motorcycle_favorites.count(),
        'reviews_count': request.user.motorcycle_reviews.count(),
    }
    return render(request, 'account/profile.html', {'orders': orders, 'profile': profile, 'stats': stats})


@login_required
def edit_profile_view(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'account/edit_profile.html', {'form': form, 'profile_form': profile_form})
