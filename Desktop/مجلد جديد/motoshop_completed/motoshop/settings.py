"""
Django settings for motoshop project.
"""

from pathlib import Path
import importlib.util
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-only-change-me')

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in {'1', 'true', 'yes', 'on'}

ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if host.strip()]

GRAPPELLI_AVAILABLE = importlib.util.find_spec('grappelli') is not None

INSTALLED_APPS = [
    *(['grappelli'] if GRAPPELLI_AVAILABLE else []),
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'account',
    'branches',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'account.middleware.RedirectAuthenticatedUsersMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'motoshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'shop' / 'templates',
            BASE_DIR / 'account' / 'templates',
            BASE_DIR / 'branches' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'motoshop.context_processors.site_contact',
            ],
        },
    },
]

WSGI_APPLICATION = 'motoshop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':'ESLAMDB'   ,    # ضع اسم قاعدة البيانات التي أنشأتها في PostgreSQL
        'USER': 'postgres',                # اسم المستخدم (غالباً postgres افتراضياً)
        'PASSWORD': 'eslam',          # كلمة المرور الخاصة بقاعدة البيانات لديك
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ نموذج المستخدم المخصص
AUTH_USER_MODEL = 'account.User'

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Aden'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

#==============================================
# Django Admin theme: Grappelli (enabled automatically when installed)
GRAPPELLI_ADMIN_TITLE = 'MotoShop - لوحة الإدارة'

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Use SMTP only when credentials are configured; otherwise print emails to the console.
EMAIL_BACKEND = (
    'django.core.mail.backends.smtp.EmailBackend'
    if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
    else 'django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or 'noreply@motoshop.local'

# Public site identity/contact information
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', EMAIL_HOST_USER)
CONTACT_PHONE = os.getenv('CONTACT_PHONE', '778 348 969')
CONTACT_PHONE_LINK = os.getenv('CONTACT_PHONE_LINK', '+967778348969')
SITE_COUNTRY = os.getenv('SITE_COUNTRY', 'اليمن')
SITE_LOCATION = os.getenv('SITE_LOCATION', 'اليمن')
