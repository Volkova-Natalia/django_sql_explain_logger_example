"""
Django settings for backend_django project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from dotenv import load_dotenv
from distutils.util import strtobool

# print(__file__)

# load_dotenv()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Redirect stdout to a file:
# import sys
# sys.stdout = open(BASE_DIR + '/log.txt', 'w')


load_dotenv(dotenv_path=BASE_DIR + '/.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(strtobool(os.getenv('DEBUG', 'False')))

ALLOWED_HOSTS = eval(os.getenv('ALLOWED_HOSTS', '[]'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.sample',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'backend_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {}
if 'DATABASES_DEFAULT' in os.environ:
    DATABASES['default'] = eval(os.getenv('DATABASES_DEFAULT'))
else:
    DATABASES['default'] = {
        # TODO: need to change
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR),                 # for swagger.json
]


FRONTEND_SCHEME = os.getenv('FRONTEND_SCHEME', None)
FRONTEND_HOST = os.getenv('FRONTEND_HOST', None)

CORS_ALLOW_ALL_ORIGINS = bool(strtobool(os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False')))

CORS_ALLOWED_ORIGINS = eval(os.getenv('CORS_ALLOWED_ORIGINS', '[]'))
if FRONTEND_HOST:
    CORS_ALLOWED_ORIGINS.append(FRONTEND_SCHEME + r'://' + FRONTEND_HOST)

CORS_ALLOW_CREDENTIALS = bool(strtobool(os.getenv('CORS_ALLOW_CREDENTIALS', 'True')))

CSRF_TRUSTED_ORIGINS = eval(os.getenv('CSRF_TRUSTED_ORIGINS', '[]'))
if FRONTEND_HOST:
    CSRF_TRUSTED_ORIGINS.append(FRONTEND_HOST)


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
