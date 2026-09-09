from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم الفرع")
    slug = models.SlugField(unique=True, blank=True)
    address = models.TextField(verbose_name="العنوان")
    city = models.CharField(max_length=100, verbose_name="المدينة")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    email = models.EmailField(blank=True, verbose_name="البريد الإلكتروني")
    manager_name = models.CharField(max_length=100, blank=True, verbose_name="اسم المدير")
    image = models.ImageField(upload_to='branches/', blank=True, verbose_name="صورة الفرع")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, verbose_name="خط العرض")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True, verbose_name="خط الطول")
    opening_hours = models.CharField(max_length=200, default="9:00 ص - 9:00 م", verbose_name="ساعات العمل")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "فرع"
        verbose_name_plural = "الفروع"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.city}"


class ProductType(models.Model):
    name = models.CharField(max_length=100, verbose_name="نوع المنتج")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="الوصف")
    icon = models.CharField(max_length=50, default="fas fa-motorcycle", verbose_name="الأيقونة")
    is_active = models.BooleanField(default=True, verbose_name="نشط")

    class Meta:
        verbose_name = "نوع منتج"
        verbose_name_plural = "أنواع المنتجات"

    def __str__(self):
        return self.name


class BranchInventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventory', verbose_name="الفرع")
    motorcycle = models.ForeignKey('shop.Motorcycle', on_delete=models.CASCADE, verbose_name="الدراجة")
    quantity = models.PositiveIntegerField(default=0, verbose_name="الكمية")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "مخزون الفرع"
        verbose_name_plural = "مخزون الفروع"
        unique_together = ['branch', 'motorcycle']

    def __str__(self):
        return f"{self.branch.name} - {self.motorcycle.name} ({self.quantity})"
