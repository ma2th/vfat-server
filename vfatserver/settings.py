# Copyright 2019 Matthias Ring
# Machine Learning and Data Analytics Lab
# Friedrich-Alexander-University Erlangen-Nuremberg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'rest_framework',
    'rest_framework.authtoken',
    'registration',
    'main.apps.MainConfig',
    'assessment.apps.AssessmentConfig',
    'api.apps.ApiConfig',
    'stats.apps.StatsConfig',
    'clientconf.apps.ClientconfConfig',
    'train.apps.TrainConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middleware.LoginRequiredMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates'],
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

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# SECURITY WARNING: keep the secret key used in production secret!
with open(BASE_DIR + '/non-opensource/config/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/2.0/ref/middleware/#http-strict-transport-security
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True

# https://docs.djangoproject.com/en/2.0/ref/clickjacking/#setting-x-frame-options-for-all-responses
X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['.vfat.mad.tf.fau.de']

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

WSGI_APPLICATION = 'vfatserver.wsgi.application'

ROOT_URLCONF = 'vfatserver.urls'

STATIC_URL = '/static/'

with open(BASE_DIR + '/non-opensource/config/static_root.txt') as f:
    STATIC_ROOT = f.read().strip()

MEDIA_URL = '/media/'

with open(BASE_DIR + '/non-opensource/config/media_root.txt') as f:
    MEDIA_ROOT = f.read().strip()

AUTH_USER_MODEL = 'main.User'

LOGIN_REDIRECT_URL = '/main/'

# LoginRequiredMiddleware
# Important: This must be a tuple with at least one ,

LOGIN_REQUIRED_URLS_EXCEPTIONS = (r'^/home/',
                                  r'^/accounts/login/$',
                                  r'^/accounts/register/$',
                                  r'^/api/',
                                  r'^/admin/')

# django-registration-redux

SIMPLE_BACKEND_REDIRECT_URL = LOGIN_REDIRECT_URL




