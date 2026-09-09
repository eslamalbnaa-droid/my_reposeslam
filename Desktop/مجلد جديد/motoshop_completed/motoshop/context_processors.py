from django.conf import settings


def site_contact(request):
    """Shared public contact information for all templates."""
    email = getattr(settings, 'CONTACT_EMAIL', '') or getattr(settings, 'EMAIL_HOST_USER', '') or 'info@motoshop.com'
    return {
        'site_contact_email': email,
        'site_contact_phone': getattr(settings, 'CONTACT_PHONE', '778 348 969'),
        'site_contact_phone_link': getattr(settings, 'CONTACT_PHONE_LINK', '+967778348969'),
        'site_country': getattr(settings, 'SITE_COUNTRY', 'اليمن'),
        'site_location': getattr(settings, 'SITE_LOCATION', 'اليمن'),
    }
