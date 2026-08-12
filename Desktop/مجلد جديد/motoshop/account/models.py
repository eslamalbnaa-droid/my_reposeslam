from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    ]

    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم الهاتف")
    address = models.TextField(blank=True, verbose_name="العنوان")
    city = models.CharField(max_length=100, blank=True, verbose_name="المدينة")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, verbose_name="الجنس")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name="الصورة الشخصية")
    is_verified = models.BooleanField(default=False, verbose_name="حساب موثق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمين"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="المستخدم")
    bio = models.TextField(blank=True, verbose_name="نبذة")
    favorite_brand = models.CharField(max_length=50, blank=True, verbose_name="العلامة المفضلة")
    notifications_enabled = models.BooleanField(default=True, verbose_name="تفعيل الإشعارات")

    class Meta:
        verbose_name = "الملف الشخصي"
        verbose_name_plural = "الملفات الشخصية"

    def __str__(self):
        return f"ملف {self.user.username}"
