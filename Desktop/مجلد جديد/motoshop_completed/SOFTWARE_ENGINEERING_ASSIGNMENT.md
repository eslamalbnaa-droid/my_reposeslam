# واجب هندسة البرمجيات العملي

## 1) علاقة واحد إلى واحد (One-to-One)
المشروع يحتوي على العلاقة التالية:

- `account.User` ↔ `account.UserProfile`
- الحقل: `UserProfile.user = models.OneToOneField(...)`
- الجدولان: `account_user` و `account_userprofile`.

## 2) علاقة كثير إلى كثير (Many-to-Many)
تمت إضافة علاقة المفضلة بين المستخدمين والدراجات:

- `shop.Motorcycle.favorite_by` ↔ `account.User`
- نوع العلاقة: `models.ManyToManyField(...)`
- تم استخدام جدول وسيط صريح: `shop.Favorite`
- يوجد قيد يمنع تكرار نفس المستخدم مع نفس الدراجة.

## 3) QuerySet
يوجد ملف مستقل `shop/queryset_lab.py` يحتوي على تطبيق عملي لأكثر من 7 دوال QuerySet، منها:

1. `all()`
2. `filter()`
3. `exclude()`
4. `order_by()`
5. `values()`
6. `annotate()`
7. `distinct()`
8. `count()`
9. `exists()`
10. `aggregate()`
11. `select_related()`
12. `prefetch_related()`

## صفحة العرض العملي
يمكن فتح صفحة العرض من:

`/shop/queryset-lab/`

وهي تعرض إحصائيات واستعلامات QuerySet المستخدمة في المشروع.

## migration
تمت إضافة:

`shop/migrations/0002_software_engineering_relations.py`
