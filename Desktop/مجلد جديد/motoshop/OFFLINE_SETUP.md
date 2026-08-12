# MotoShop Offline

هذه النسخة مبنية على مشروع MotoShop الأصلي.

- لا تعتمد قوالب HTML على Tailwind CDN أو Google Fonts أو Font Awesome CDN.
- CSS وJavaScript الأساسيان محليان داخل `static/`.
- الفلتر الذكي مستقل داخل `shop/smart_filter/` ويصحح/يقترح أسماء الدراجات بالعربية والإنجليزية باستخدام خوارزميات نصية حتمية فقط.
- واجهة الفلتر الذكي موجودة في `shop/templates/shop/product_list.html` بجانب البحث العادي.

تشغيل المشروع:
```bash
python manage.py runserver
```
ثم افتح `http://127.0.0.1:8000/`.
