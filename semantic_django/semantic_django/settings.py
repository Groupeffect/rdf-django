"""
Django settings for semantic_django project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# use .env to set custom variables
ENVS = environ.Env(
    DJANGO_DEBUG=(bool, True),
    DJANGO_SECRET_KEY=(
        str, 'django-insecure-j3^o0)_*%jkx^6zt+4a((t42b26q)1v5-x5mn9%y9$%vlzo@st'
    ),
    DJANGO_GLOBAL_GRAPH_IO_FORMAT=(str, "xml"),
    DJANGO_GLOBAL_HOST_URL=(str, "http://localhost:8000"),
)
GLOBAL_GRAPH_IO_FORMAT = ENVS.str('DJANGO_GLOBAL_GRAPH_IO_FORMAT')
GLOBAL_HOST_URL = ENVS.str('DJANGO_GLOBAL_HOST_URL')
GLOBAL_API_ACCOUNT_PERSON_URL = os.path.join(GLOBAL_HOST_URL, 'api', 'account', 'person')
GLOBAL_API_ACCOUNT_ORGANIZATION_URL = os.path.join(GLOBAL_HOST_URL, 'api', 'account', 'organization')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENVS.bool('DJANGO_DEBUG')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENVS.str('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS_DJANGO_CORE = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS_EXTERNAL = [
    'rest_framework',
]

INSTALLED_APPS = [
    *INSTALLED_APPS_DJANGO_CORE,
    *INSTALLED_APPS_EXTERNAL,
    'account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'semantic_django.urls'

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

WSGI_APPLICATION = 'semantic_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
