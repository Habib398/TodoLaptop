import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# CONFIGURACIÓN BÁSICA
SECRET_KEY = config('SECRET_KEY', default='django-insecure-cambia-esta-clave-a-una-muy-segura')
AUTH_USER_MODEL = 'usuarios.Usuario'
DEBUG = config('DEBUG', default=True, cast=bool)

# Permite acceso local y desde túneles de Cloudflare
ALLOWED_HOSTS = ['*']  # Permite todos los hosts (solo para desarrollo)

# -------------------------
# APLICACIONES INSTALADAS
# -------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'inventario',
    'ventas',
    'servicios',
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

# Configuración para permitir iframes de Cloudflare (solo desarrollo)
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

ROOT_URLCONF = 'TodoLap.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Carpeta global de templates
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

WSGI_APPLICATION = 'TodoLap.wsgi.application'

# BASE DE DATOS - POSTGRESQL
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME', default='TodoLaptop'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='12345678'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# BASE DE DATOS - SQLITE (Configuración anterior comentada)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# BASE DE DATOS - MYSQL (Configuración original comentada)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'TLP_Manager',
#         'USER': 'root',         # Usuario de MySQL
#         'PASSWORD': '12345678',         # Contraseña de MySQL
#         'HOST': '127.0.0.1',    # Servidor
#         'PORT': '3306',         # Puerto de MySQL
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#         }
#     }
# }

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

# Cuando uses un túnel (Cloudflare / ngrok) para una DEMO y hagas POST (login, formularios),
# Django valida también el origen (origin) para CSRF. Debes añadir el dominio HTTPS completo
# a CSRF_TRUSTED_ORIGINS. Para Cloudflare quick tunnel normalmente es algo como:
#   https://<subdominio>.trycloudflare.com
# Sustituye la cadena de ejemplo por la que te aparezca en la terminal.
# Puedes dejar el comodín del dominio base para simplificar en una DEMO, pero NO en producción.
CSRF_TRUSTED_ORIGINS = [
    "https://*.trycloudflare.com",  # Demo rápida Cloudflare Tunnel
    # "https://<tu-subdominio>.ngrok-free.app",  # Descomenta si usas ngrok
]

# Configuraciones adicionales para túneles
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SESSION_COOKIE_SAMESITE = 'Lax'  # Permite cookies cross-site con cierta protección
CSRF_COOKIE_SAMESITE = 'Lax'

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
