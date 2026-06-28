"""
Django settings for jss_archive project.
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nxdcce1q(5r1ud1#tpyks6j1hvhq_a3qmc3&p$$!6w%(t!x7*8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom apps
    'papers.apps.PapersConfig',
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

ROOT_URLCONF = 'jss_archive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'jss_archive.wsgi.application'
ASGI_APPLICATION = 'jss_archive.asgi.application'


# Database Configuration
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# By default, we use MySQL. If python-mysqlclient/pymysql is missing, or DJANGO_USE_SQLITE=True is set,
# we fall back to SQLite for easier local demonstration and testing.

USE_SQLITE_ENV = os.environ.get('DJANGO_USE_SQLITE', 'False').lower() in ('true', '1', 'yes')

# Detect if any MySQL backend driver is installed
has_mysql_driver = False
try:
    import MySQLdb  # Check for mysqlclient
    has_mysql_driver = True
except ImportError:
    try:
        import pymysql  # Check for pymysql
        pymysql.install_as_MySQLdb()
        has_mysql_driver = True
    except ImportError:
        pass

if USE_SQLITE_ENV or 'test' in sys.argv or not has_mysql_driver:
    if not has_mysql_driver and not (USE_SQLITE_ENV or 'test' in sys.argv):
        print("\n" + "="*80)
        print(" WARNING: MySQL driver ('mysqlclient' or 'pymysql') was not found.")
        print(" Django is automatically falling back to SQLite for local development/review.")
        print(" To connect to a MySQL server, please run:")
        print("     pip install mysqlclient")
        print("     OR")
        print("     pip install pymysql")
        print("="*80 + "\n")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'jss_archive',
            'USER': 'root',
            'PASSWORD': 'Prajju@5129',  # Replace with actual MySQL password
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
        }
    }


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (Uploaded Question Papers)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings for file uploads
# Limit max upload size to 10MB (in bytes)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

