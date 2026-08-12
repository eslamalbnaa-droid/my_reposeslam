from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone', 'notes']
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500 transition',
                'placeholder': 'أدخل عنوان الشحن الكامل',
                'rows': 3,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500 transition',
                'placeholder': '05xxxxxxxx',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500 transition',
                'placeholder': 'ملاحظات إضافية (اختياري)',
                'rows': 2,
            }),
        }
        labels = {
            'shipping_address': 'عنوان الشحن',
            'phone': 'رقم الهاتف',
            'notes': 'ملاحظات',
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'اسمك الكامل'
        }),
        label='الاسم'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'بريدك@example.com'
        }),
        label='البريد الإلكتروني'
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'موضوع الرسالة'
        }),
        label='الموضوع'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'اكتب رسالتك هنا...',
            'rows': 5
        }),
        label='الرسالة'
    )
