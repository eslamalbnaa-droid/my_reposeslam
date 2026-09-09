from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'بريدك@example.com'
        }),
        label='البريد الإلكتروني'
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': '7xxxxxxxx'
        }),
        label='رقم الهاتف',
        required=False
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'الاسم الأول'
        }),
        label='الاسم الأول'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'الاسم الأخير'
        }),
        label='الاسم الأخير'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
                'placeholder': 'اسم المستخدم'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'كلمة المرور'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'تأكيد كلمة المرور'
        })


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'اسم المستخدم أو البريد'
        }),
        label='اسم المستخدم'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
            'placeholder': 'كلمة المرور'
        }),
        label='كلمة المرور'
    )


class ProfileForm(forms.ModelForm):
    MAX_AVATAR_SIZE = 2 * 1024 * 1024  # 2 MB
    ALLOWED_AVATAR_TYPES = {'image/jpeg', 'image/png', 'image/webp'}

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar:
            return avatar

        content_type = getattr(avatar, 'content_type', None)
        if content_type and content_type not in self.ALLOWED_AVATAR_TYPES:
            raise forms.ValidationError('صيغة الصورة غير مدعومة. استخدم JPG أو PNG أو WEBP.')

        size = getattr(avatar, 'size', 0)
        if size and size > self.MAX_AVATAR_SIZE:
            raise forms.ValidationError('حجم الصورة يجب ألا يتجاوز 2 ميجابايت.')

        return avatar

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'gender', 'birth_date', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500'}),
            'phone': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500'}),
            'address': forms.Textarea(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500'}),
            'gender': forms.Select(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500'}),
            'birth_date': forms.DateInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500'}),
        }
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'الاسم الأخير',
            'email': 'البريد الإلكتروني',
            'phone': 'رقم الهاتف',
            'address': 'العنوان',
            'city': 'المدينة',
            'gender': 'الجنس',
            'birth_date': 'تاريخ الميلاد',
            'avatar': 'الصورة الشخصية',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'favorite_brand', 'notifications_enabled']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
                'rows': 4,
                'placeholder': 'اكتب نبذة قصيرة عنك...',
            }),
            'favorite_brand': forms.TextInput(attrs={
                'class': 'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-500',
                'placeholder': 'مثال: Honda',
            }),
            'notifications_enabled': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 accent-red-600',
            }),
        }
        labels = {
            'bio': 'نبذة عني',
            'favorite_brand': 'العلامة التجارية المفضلة',
            'notifications_enabled': 'تفعيل الإشعارات',
        }
