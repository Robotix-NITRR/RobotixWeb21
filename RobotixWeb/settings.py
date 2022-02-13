import dj_database_url
import django_on_heroku
from .production import *
import os

ALLOWED_HOSTS.append('.herokuapp.com')
SECRET_KEY = os.environ.get('SECRET_KEY')

if os.environ.get('DEBUG'):
    DEBUG = True


# Installed apps
INSTALLED_APPS.append('whitenoise.runserver_nostatic')


# Middlewares
temp = ['whitenoise.middleware.WhiteNoiseMiddleware']
for i in range(len(MIDDLEWARE)):
    temp.append(MIDDLEWARE[i])
MIDDLEWARE = temp


WSGI_APPLICATION = 'RobotixWeb.wsgi.application'

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# Database
if os.environ.get('DEBUG'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('POSTGRES_HOST'),
            'PORT': os.environ.get('POSTGRES_PORT')
        }
    }
else:
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
    WHITENOISE_USE_FINDERS = True
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
