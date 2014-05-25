"""
Django settings for pims4 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from django.contrib import messages

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '16--&m%zo=i+kqgy$d#2le%ph*k76%fo-t8fp12v(_w9t32gi6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools', 
    'bootstrap3',
    'system', 
    'bootstrap3_datetime', 
    
)

MIDDLEWARE_CLASSES = (
  #  'django.middleware.cache.UpdateCacheMiddleware',     #
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
  #  'django.middleware.cache.FetchFromCacheMiddleware',#
)

ROOT_URLCONF = 'pims.urls'

WSGI_APPLICATION = 'pims.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pims',
        'USER': 'pims', 
        'PASSWORD': 'admin', 
        'HOST': '127.0.0.1', 
        'port': '3306', 
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(pathname)s %(funcName)s %(process)d [%(thread)d] - %(threadName)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/django/pims-debug.log',
            'formatter': 'verbose'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'system': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        }, 
        'django.request':{
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}



BOOTSTRAP3 = {
    'jquery_url': '//cdn.bootcss.com/jquery/2.1.1/jquery.min.js',
    'base_url': '//cdn.bootcss.com/bootstrap/3.1.1/',
    'css_url': '//cdn.bootcss.com/bootstrap/3.1.1/css/bootstrap.css',
    'theme_url': '//cdn.bootcss.com/bootstrap/3.1.1/css/bootstrap-theme.css',
    'javascript_url': '//cdn.bootcss.com/bootstrap/3.1.1/js/bootstrap.min.js',
    'javascript_in_head': False,
    'include_jquery': False,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-10',
       'set_required': True,
    'form_required_class': '',
    'form_error_class': '',
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
    


}
