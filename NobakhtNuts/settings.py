from email.policy import default
from pathlib import Path
import os
from decouple import config, Config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG' ,default=True ,cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost"
).split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'cachalot',
    'ckeditor',
    'ckeditor_uploader',
    'iranian_cities',
    'django_jalali',
    'account_module',
    'product_module',
    'home_module',
    'support_module',
    'order_module',
    'polls',
    'article_module',
    'userpanel_module',
    'django_render_partial',
    'site_settings',
    'documents_module',
    'adminpanel_module',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NobakhtNuts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'NobakhtNuts.context_processors.global_context',
                'site_settings.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'NobakhtNuts.wsgi.application'

DB_ENGINE = config('DB_ENGINE' ,default="django.db.backends.sqlite3")

if DB_ENGINE == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            "OPTIONS": {
                "unix_socket": "/tmp/mysql.sock",
                "charset": "utf8mb4",
            },
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

logging_status = config('LOGGING' ,default=False, cast=bool)
if logging_status:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': '/home/nobakhtn/logs/nobakhtnuts_errors.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True
USE_L10N = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'account_module.User'

SANDBOX = True

SMS_API_KEY = "https://console.melipayamak.com/api/send/otp/410281e7a9a74a2283fd51b6b8653654"


CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
        'filebrowserUploadUrl': "/ckeditor/upload/",
        'filebrowserBrowseUrl': "/ckeditor/browse/",
    },
}

SITE_ID= 1

ZP_API_REQUEST = 'https://payment.zarinpal.com/pg/v4/payment/request.json'
ZP_API_VERIFY = 'https://payment.zarinpal.com/pg/v4/payment/verify.json'
ZP_API_STARTPAY = 'https://payment.zarinpal.com/pg/StartPay/'
# ZP_API_REQUEST = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
# ZP_API_VERIFY = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
# ZP_API_STARTPAY = 'https://sandbox.zarinpal.com/pg/StartPay/'
