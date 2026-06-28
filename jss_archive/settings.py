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

if USE_SQLITE_ENV or 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(DATABASE_URL)
        
        scheme = parsed.scheme
        if scheme == 'mysql':
            DB_ENGINE = 'django.db.backends.mysql'
        elif scheme in ('postgresql', 'postgres'):
            DB_ENGINE = 'django.db.backends.postgresql'
        elif scheme == 'sqlite':
            DB_ENGINE = 'django.db.backends.sqlite3'
        else:
            DB_ENGINE = scheme

        DB_NAME = parsed.path[1:] if parsed.path else ''
        if '?' in DB_NAME:
            DB_NAME = DB_NAME.split('?')[0]
        DB_USER = parsed.username or ''
        DB_PASSWORD = parsed.password or ''
        DB_HOST = parsed.hostname or ''
        DB_PORT = str(parsed.port) if parsed.port else ''
        
        query_params = parse_qs(parsed.query)
        ssl_mode = query_params.get('ssl-mode') or query_params.get('ssl_mode')
    else:
        DB_ENGINE = os.environ.get('DB_ENGINE', 'django.db.backends.mysql')
        DB_NAME = os.environ.get('DB_NAME', 'jss_archive')
        DB_USER = os.environ.get('DB_USER', 'root')
        DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Prajju@5129')
        DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
        DB_PORT = os.environ.get('DB_PORT', '3306')
        ssl_mode = None

    if not has_mysql_driver and DB_ENGINE == 'django.db.backends.mysql':
        print("\n" + "="*80)
        print(" WARNING: MySQL driver was not found. Falling back to SQLite.")
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
                'ENGINE': DB_ENGINE,
                'NAME': DB_NAME,
                'USER': DB_USER,
                'PASSWORD': DB_PASSWORD,
                'HOST': DB_HOST,
                'PORT': DB_PORT,
            }
        }
        if 'mysql' in DB_ENGINE:
            DATABASES['default']['OPTIONS'] = {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
            if ssl_mode:
                DATABASES['default']['OPTIONS']['ssl'] = {}


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

