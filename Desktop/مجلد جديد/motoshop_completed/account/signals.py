from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile


@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, **kwargs):
    """Create the one-to-one profile automatically and repair missing profiles."""
    UserProfile.objects.get_or_create(user=instance)
