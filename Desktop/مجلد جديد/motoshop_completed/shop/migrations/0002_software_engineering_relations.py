from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')),
                ('motorcycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_records', to='shop.motorcycle', verbose_name='الدراجة')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motorcycle_favorites', to=settings.AUTH_USER_MODEL, verbose_name='المستخدم')),
            ],
            options={
                'verbose_name': 'مفضلة',
                'verbose_name_plural': 'المفضلات',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='favorite_by',
            field=models.ManyToManyField(blank=True, related_name='favorite_motorcycles', through='shop.Favorite', to=settings.AUTH_USER_MODEL, verbose_name='المستخدمون المفضلون'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'motorcycle'), name='unique_user_motorcycle_favorite'),
        ),
    ]
