import os
from pathlib import Path
from dotenv import load_dotenv

#loading .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv('DEBUG'))

allowed_host = os.getenv("DJANGO_ALLOWED_HOSTS") or 'localhost 127.0.0.1 [::1] '

# Application definition
INSTALLED_APPS = [
    "rest_framework",
    "api",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'sql_mode': 'traditional',
        },       
        'NAME': str(os.getenv('DB_NAME')),
        'USER': str(os.getenv('DB_USER')),
        'PASSWORD': str(os.getenv('DB_PASSWORD')),
        'HOST': str(os.getenv('DB_HOST')),
        'PORT': str(os.getenv('DB_PORT')),
    } 
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#log configurations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'handle_success_filelog': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './file_logs/success.log',
            'formatter': 'file_log',
            'maxBytes': 5242880, # 5*1024*1024 bytes (5MB)
        },
        'handle_error_filelog': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './file_logs/error.log',
            'formatter': 'file_log',
            'maxBytes': 5242880, # 5*1024*1024 bytes (5MB)
        },
    },
    'loggers': {
        'restapi.log.success.file': {
            'handlers': ['handle_success_filelog'],
            'level': 'INFO',
        },
        'restapi.log.error.file': {
            'handlers': ['handle_error_filelog'],
            'level': 'INFO',
        },
    },
    'formatters': {
        'file_log': {
            'format': '[{levelname}] [{asctime}] {msg}\n{params}\n',
            'style': '{',
        }
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DATETIME_FORMAT': '%s',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Coolest Districts API',
    'DESCRIPTION': 'This projects helps you out to skip hotness :)',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
