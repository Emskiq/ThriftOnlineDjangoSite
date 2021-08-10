import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-up-lu0i5koze2v8anhmhyeyz@*n_uictsz4!mfg2+w%b(7=5%!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # During development only

#AUTH backend
AUTHENTICATION_BACKENDS = ( 'apps.userprofile.backends.EmailOrUsernameModelBackend', 'django.contrib.auth.backends.ModelBackend', )

#Cart - how much time before auto remove
SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = 'cart'

ALLOWED_HOSTS = ['4bbdc0cff880.ngrok.io', '127.0.0.1']

#Login/out
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'cart'
LOGOUT_REDIRECT_URL = 'frontpage'

#Stripe keys
STRIPE_API_KEY_PUBLISHABLE = "pk_test_51Im2CxJd0NuNl9Yw4FObGfn4fZq6sAikEQGEYIirRuSZYg4pKuvLPeypDXshXD0jLP2lc5n6iBFp0i1EhxIBAyOk00YpIg5kRv"
STRIPE_API_KEY_HIDDEN = "sk_test_51Im2CxJd0NuNl9YwP2YbAlDggwWowY5x29Ys2eDYme7xjzhBs4l4MbKA6fCq3jhEKmf1RYulWpBTUsR8WNTSUovI00yt5gBALa"

#PayPal keys
PAYPAL_API_KEY_PUBLISHABLE = "AYWcH_TjVR6kklVaumv2Y-L-Ki1sLeTvglLD0Pl5ghGyRlo-IeZ8Af-QMnNfYh87Reaor5grhb4elnkw"
PAYPAL_API_KEY_HIDDEN  = "EH_qvk5pDY-N1nl0CHpEtcefqMW2qodT1hj0Z-KcRc3O4TFV2dzDhNyIzhas5BxDUJ14P6a7veLb2e4X"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.core',
    'apps.store',
    'apps.cart',
    'apps.order',
    'apps.userprofile',
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

ROOT_URLCONF = 'thrift_online.urls'

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

                #my context processors
                'apps.store.context_processors.menu_categories',
                'apps.cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'thrift_online.wsgi.application'


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
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static'),
  os.path.join(BASE_DIR, 'static/css_files'),
)
STATIC_ROOT = BASE_DIR / "static_export/"

MEDIA_URL = '/media/'
MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media\\')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False