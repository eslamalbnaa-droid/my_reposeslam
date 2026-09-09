# MotoShop — Offline Frontend

تم تجهيز واجهة MotoShop لتعمل محليًا بدون اتصال بالإنترنت بعد تثبيت متطلبات Python وتشغيل المشروع.

## ما أصبح محليًا
- Tailwind-compatible CSS: `static/css/tailwind.css`
- JavaScript الأساسي: `static/js/main.js`
- JavaScript الفلتر الذكي: `static/js/smart-filter.js`
- Font Awesome CSS/Webfonts: `static/fontawesome/`
- صور الموقع: `static/images/`
- لا تعتمد القوالب على Tailwind CDN أو Google Fonts أو Font Awesome CDN.

## ملاحظات
- الخط العربي يستخدم خطوط النظام المحلية (Tahoma / Arial / Segoe UI)، لذلك لا يحتاج Google Fonts.
- رابط Google Maps في صفحة التواصل هو رابط اختياري لخدمة خارجية؛ لا يؤثر على شكل الموقع أو JavaScript، لكنه بطبيعته يحتاج إنترنت عند فتحه.
- إرسال البريد عبر Gmail يحتاج إنترنت لأنه خدمة خارجية، وهذا منفصل عن تشغيل تصميم الموقع ووظائف الواجهة المحلية.
- تثبيت مكتبات Python من `requirements.txt` يحتاج أن تكون المكتبات مثبتة مسبقًا أو يتوفر إنترنت مرة واحدة للتثبيت.

## التشغيل
```bash
python manage.py runserver
```
