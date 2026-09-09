# Generated for MotoShop admin-to-user email log
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_review'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SentEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient_email', models.EmailField(max_length=254, verbose_name='البريد المستلم')),
                ('subject', models.CharField(max_length=255, verbose_name='عنوان الرسالة')),
                ('message', models.TextField(verbose_name='نص الرسالة')),
                ('status', models.CharField(choices=[('sent', 'تم الإرسال'), ('failed', 'فشل الإرسال')], default='sent', max_length=10, verbose_name='الحالة')),
                ('error_message', models.TextField(blank=True, verbose_name='تفاصيل الخطأ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإرسال')),
                ('recipient_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_site_emails', to=settings.AUTH_USER_MODEL, verbose_name='المستخدم المستلم')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_site_emails', to=settings.AUTH_USER_MODEL, verbose_name='المرسل من الإدارة')),
            ],
            options={
                'verbose_name': 'رسالة بريد مرسلة',
                'verbose_name_plural': 'سجل البريد المرسل',
                'ordering': ['-created_at'],
            },
        ),
    ]
