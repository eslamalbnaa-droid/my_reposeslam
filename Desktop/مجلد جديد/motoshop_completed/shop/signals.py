from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def send_order_confirmation(sender, instance, created, **kwargs):
    """Send a non-blocking confirmation email when an order is first created."""
    if not created or not instance.user.email:
        return

    send_mail(
        subject=f'تأكيد طلبك #{instance.pk} - MotoShop',
        message=(
            f'مرحباً {instance.user.first_name or instance.user.username},\n\n'
            f'تم استلام طلبك رقم #{instance.pk} بنجاح.\n'
            f'إجمالي الطلب: {instance.total}\n'
            'سنقوم بإبلاغك عند تحديث حالة الطلب.\n\nMotoShop'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.user.email],
        fail_silently=True,
    )
