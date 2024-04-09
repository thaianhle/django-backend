"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from django.conf.global_settings import CSRF_COOKIE_SECURE, SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, STATICFILES_DIRS
import environ
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_TYPE = os.environ.get("ENV_TYPE")
#ENV = environ.Env()
if ENV_TYPE == "dev":
    environ.Env.read_env(".env.dev", overwrite=True)
    #print("read env success")
if ENV_TYPE == "prod":
    environ.Env.read_env(".env.prod", overwrite=True)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '/wIgCPRUGlGMYakNVuOcC2#<#~F`yiLFg5LPFJD=.a!KtJF_;$c_UZ}=OH#,QO6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False

# Application definition

INSTALLED_APPS = [
    #'django-admin-tailwind',
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    #"unfold.contrib.import_export",  # optional, if django-import-export package is used
    #"unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    #'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',

    'rest_framework_simplejwt',

    'allauth',
    'allauth.account',

    #'dj_rest_auth',
    #'dj_rest_auth.registration'
    'adrf',
    'django_jsonform',
    'user',
    'property',
    'product',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

print(os.environ.get("DB_NAME"))
print(os.environ.get("DB_USER"))
print(os.environ.get("DB_PASS"))
print(os.environ.get("DB_HOST"))
print(os.environ.get("DB_PORT"))
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        #'ENGINE': 'django.db.backends.mysql',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASS"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVER_FLOW': 0,
            'RECYCLE': 24*60*60,
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
WEBSITE_URL = 'http://localhost:8000'
AUTH_USER_MODEL = 'user.User'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:3000'
]

# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# dj_rest_auth
# must config if you want return jwt token
# if not have config, then django rest_auth_register return 204 no content
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": True
}

# all-auth
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = None


JAZZMIN_SETTINGS = {
    "user_avatar": "avatar",
}



#LOGGING = {
#    "version": 1,
#    "disable_existing_loggers": False,
#    "handlers": {
#        "file": {
#            "level": "DEBUG",
#            "class": "logging.FileHandler",
#            "filename": "./debug.log",
#        },
#        "console": {
#            "class": "logging.StreamHandler",
#        },
#    },
#    "loggers": {
#        "django.db": {
#            "handlers": ["console"],
#            "level": "DEBUG",
#            "propagate": True,
#        },
#    },
#}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, '../venv/unfold/static/')]
#print(STATIC_ROOT)