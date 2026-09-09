from django import forms
from django.contrib.auth import get_user_model
from .models import Order, Review, Motorcycle


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
                'placeholder': '7xxxxxxxx',
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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-red-500'}),
            'comment': forms.Textarea(attrs={
                'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-red-500',
                'rows': 4,
                'placeholder': 'اكتب تجربتك مع هذه الدراجة...',
            }),
        }
        labels = {'rating': 'التقييم', 'comment': 'المراجعة'}


class MotorcycleForm(forms.ModelForm):
    """نموذج إدارة المنتجات داخل الموقع مع تحقق أساسي من الصورة والأسعار."""
    MAX_IMAGE_SIZE = 5 * 1024 * 1024
    ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp'}

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image
        content_type = getattr(image, 'content_type', None)
        if content_type and content_type not in self.ALLOWED_IMAGE_TYPES:
            raise forms.ValidationError('صيغة الصورة غير مدعومة. استخدم JPG أو PNG أو WEBP.')
        size = getattr(image, 'size', 0)
        if size and size > self.MAX_IMAGE_SIZE:
            raise forms.ValidationError('حجم الصورة يجب ألا يتجاوز 5 ميجابايت.')
        return image

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get('price')
        old_price = cleaned.get('old_price')
        if price is not None and price <= 0:
            self.add_error('price', 'السعر يجب أن يكون أكبر من صفر.')
        if old_price is not None and old_price <= 0:
            self.add_error('old_price', 'السعر القديم يجب أن يكون أكبر من صفر.')
        return cleaned

    class Meta:
        model = Motorcycle
        fields = [
            'name', 'brand', 'model_year', 'price', 'old_price', 'description',
            'short_description', 'image', 'category', 'stock', 'engine_cc',
            'horsepower', 'weight', 'color', 'is_featured', 'is_new',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'short_description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = 'w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-red-500'
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'w-5 h-5 accent-red-600'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': base_class})
            else:
                field.widget.attrs.update({'class': base_class})


User = get_user_model()


class AdminUserEmailForm(forms.Form):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label='المستخدم المستلم',
        empty_label='اختر المستخدم',
        widget=forms.Select(attrs={'class': 'admin-mail-input'}),
    )
    subject = forms.CharField(
        max_length=255,
        label='عنوان الرسالة',
        widget=forms.TextInput(attrs={
            'class': 'admin-mail-input',
            'placeholder': 'مثال: تحديث بخصوص طلبك',
        }),
    )
    message = forms.CharField(
        label='نص الرسالة',
        widget=forms.Textarea(attrs={
            'class': 'admin-mail-input admin-mail-textarea',
            'rows': 9,
            'placeholder': 'اكتب الرسالة التي تريد إرسالها للمستخدم...',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = (
            User.objects.exclude(email='').filter(is_active=True).order_by('username')
        )
        self.fields['recipient'].label_from_instance = self._recipient_label

    @staticmethod
    def _recipient_label(user):
        full_name = user.get_full_name().strip()
        name = full_name or user.username
        return f"{name} — {user.email}"

    def clean_recipient(self):
        user = self.cleaned_data['recipient']
        if not user.email:
            raise forms.ValidationError('هذا المستخدم لا يملك بريدًا إلكترونيًا.')
        return user
