from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="الوصف")
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name="الصورة")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تصنيف"
        verbose_name_plural = "التصنيفات"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Motorcycle(models.Model):
    BRAND_CHOICES = [
        ('honda', 'هوندا'),
        ('yamaha', 'ياماها'),
        ('kawasaki', 'كاواساكي'),
        ('ducati', 'دوكاتي'),
        ('bmw', 'بي إم دبليو'),
        ('harley', 'هارلي ديفيدسون'),
        ('suzuki', 'سوزوكي'),
        ('ktm', 'كاي تي إم'),
        ('triumph', 'ترايمف'),
        ('aprilia', 'أبريليا'),
    ]

    name = models.CharField(max_length=200, verbose_name="اسم الدراجة")
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, verbose_name="العلامة التجارية")
    model_year = models.PositiveIntegerField(verbose_name="سنة الصنع")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="السعر")
    old_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="السعر القديم")
    description = models.TextField(verbose_name="الوصف")
    short_description = models.TextField(blank=True, verbose_name="وصف مختصر")
    image = models.ImageField(upload_to='motorcycles/', verbose_name="الصورة الرئيسية")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='motorcycles', verbose_name="التصنيف")
    stock = models.PositiveIntegerField(default=1, verbose_name="المخزون")
    engine_cc = models.PositiveIntegerField(verbose_name="سعة المحرك (CC)")
    horsepower = models.PositiveIntegerField(blank=True, null=True, verbose_name="القوة الحصانية")
    weight = models.PositiveIntegerField(blank=True, null=True, verbose_name="الوزن (كجم)")
    color = models.CharField(max_length=50, blank=True, verbose_name="اللون")
    is_featured = models.BooleanField(default=False, verbose_name="مميز")
    is_new = models.BooleanField(default=False, verbose_name="جديد")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "دراجة نارية"
        verbose_name_plural = "الدراجات النارية"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.name}-{self.model_year}")
        super().save(*args, **kwargs)

    def get_discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    def __str__(self):
        return f"{self.get_brand_display()} {self.name} ({self.model_year})"


class MotorcycleImage(models.Model):
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, related_name='images', verbose_name="الدراجة")
    image = models.ImageField(upload_to='motorcycles/gallery/', verbose_name="الصورة")
    caption = models.CharField(max_length=200, blank=True, verbose_name="الوصف")

    class Meta:
        verbose_name = "صورة إضافية"
        verbose_name_plural = "الصور الإضافية"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart', verbose_name="المستخدم")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سلة"
        verbose_name_plural = "السلات"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_items_count(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"سلة {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="السلة")
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, verbose_name="الدراجة")
    quantity = models.PositiveIntegerField(default=1, verbose_name="الكمية")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "عنصر السلة"
        verbose_name_plural = "عناصر السلة"
        unique_together = ['cart', 'motorcycle']

    def get_subtotal(self):
        return self.motorcycle.price * self.quantity

    def __str__(self):
        return f"{self.motorcycle.name} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('processing', 'قيد المعالجة'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التوصيل'),
        ('cancelled', 'ملغي'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="المستخدم")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="الحالة")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="المجموع")
    shipping_address = models.TextField(verbose_name="عنوان الشحن")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    notes = models.TextField(blank=True, verbose_name="ملاحظات")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"

    def __str__(self):
        return f"طلب #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="الطلب")
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, verbose_name="الدراجة")
    quantity = models.PositiveIntegerField(default=1, verbose_name="الكمية")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="السعر عند الشراء")

    class Meta:
        verbose_name = "عنصر الطلب"
        verbose_name_plural = "عناصر الطلب"

    def get_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.motorcycle.name} x {self.quantity}"
