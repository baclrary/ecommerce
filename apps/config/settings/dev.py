from os import getenv, path
from dotenv import load_dotenv
from config.settings import BASE_DIR

load_dotenv()

DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = [
    getenv("NGROK_SERVER")
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('DB_NAME'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASSWORD'),
        'HOST': getenv('DB_HOST'),
        'PORT': getenv('DB_PORT'),
    }
}

STATIC_URL = "/staticfiles/"

STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    path.join(BASE_DIR, 'media'),
    path.join(BASE_DIR, 'templates'),
    path.join(BASE_DIR, 'modules'),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = path.join(BASE_DIR, 'media')

