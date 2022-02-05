"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)
ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kashtanovdjango@gmail.com' 
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Python Project <kashtanovdjango@gmail.com>'
BASE_URL = env('BASE_URL', default='https://kashtanov1.herokuapp.com/')

MANAGERS = (
    ('Kashtanov Daniil', 'kashtanovdjango@gmail.com')
)

ADMINS = MANAGERS

# Application definition

INSTALLED_APPS = [
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages', 
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    #3rd party
    'crispy_forms',
    'allauth',
    'allauth.account',
    'django_extensions',
    'faker',
    'debug_toolbar',
    'storages',

    #Local
    'accounts',
    'blog',
    'blog2',
    'pages',
    'books',
    'polls',
    'doc',
    'doc4',
    'first_app',
    'companies',
    'basic_app',
    'ssocial',
    'posts',
    'groups',
    'products',
    'products_search',
    'products_tags',
    'products_carts',
    'products_orders',
    'products_billing',
    'products_addresses',
    'analytics',
    'marketing'
]
MAILCHIMP_API_KEY = env('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = "us20"
MAILCHIMP_EMAIL_LIST_ID = "840e38888d"
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_PUB_KEY = "pk_test_51KJHJ0JYFLEUlpihzbzd97r77iRueLXEFptTgk2bMVwkeU0P8bZiOmCRQUYgornyysru3E1RAJkPgbfyXA91UIuw00QPammCyR"
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": env.dj_db_url("DATABASE_URL",
    default="postgres://postgres@db/postgres")
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 9}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


USE_S3 = env.bool('USE_S3', default=True)

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public_read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'config.storage_backends.StaticStorage'
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'config.storage_backends.PublicMediaStorage'
    # s3 private media settings
    PROTECTED_DIR_NAME = 'protected'
    PROTECTED_MEDIA_URL = '//%s.s3.amazonaws.com/%s/' %( AWS_STORAGE_BUCKET_NAME, PROTECTED_DIR_NAME)
    S3DIRECT_REGION =  'us-east-2' 
else:

    MEDIA_URL = '/media/'
    MEDIA_ROOT = str(BASE_DIR.joinpath('media'))
    PROTECTED_ROOT = str(BASE_DIR.joinpath('protected_media'))

    STATIC_URL = '/static/'
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 
    STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))
    # STATICFILES_FINDERS = [
    #     "django.contrib.staticfiles.finders.FileSystemFinder",
    #     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # ]

STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]




# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

########
ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSignupForm', 'login': 'accounts.forms.ProductsLoginForm'}
AUTH_USER_MODEL = 'accounts.CustomUser'


CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=2592000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
default=True)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# django-storages


