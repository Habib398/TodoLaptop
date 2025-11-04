"""
CONFIGURACIÓN PRINCIPAL DEL PROYECTO TODOLAP
============================================

Este archivo contiene todas las configuraciones del proyecto Django TodoLap,
un sistema de gestión para negocios de reparación y venta de laptops.

CARACTERÍSTICAS PRINCIPALES:
- Sistema de autenticación con usuario personalizado
- Gestión de inventario de productos
- Sistema de servicios y cotizaciones
- Módulo de ventas y facturación
- Soporte para múltiples bases de datos (PostgreSQL, MySQL, SQLite)
- Configuración para desarrollo local y túneles (Cloudflare/ngrok)

MÓDULOS PRINCIPALES:
- usuarios: Autenticación y gestión de usuarios (admin, técnico, vendedor)
- inventario: Control de productos y stock
- servicios: Catálogo de servicios y cotizaciones
- ventas: Registro de ventas de productos y servicios

NOTA IMPORTANTE:
Este archivo usa python-decouple para gestionar variables de entorno.
Crear archivo .env en la raíz del proyecto para configuraciones sensibles.
"""

import os
from pathlib import Path
from decouple import config

# ==================== CONFIGURACIÓN DE RUTAS ====================

# Directorio base del proyecto (raíz donde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== CONFIGURACIÓN BÁSICA DE SEGURIDAD ====================

# Clave secreta para firmas criptográficas (NUNCA compartir en producción)
# Se carga desde variable de entorno o usa un default inseguro para desarrollo
SECRET_KEY = config('SECRET_KEY', default='django-insecure-cambia-esta-clave-a-una-muy-segura')

# Modelo de usuario personalizado (usuarios.Usuario en lugar del default de Django)
# Permite agregar campos personalizados como 'rol', 'telefono', etc.
AUTH_USER_MODEL = 'usuarios.Usuario'

# Modo debug (True solo para desarrollo, False en producción)
# Muestra errores detallados y permite el servidor de desarrollo
DEBUG = config('DEBUG', default=True, cast=bool)

# Hosts permitidos para acceder a la aplicación
# ['*'] permite todos los hosts (solo para desarrollo)
# En producción, especificar dominios exactos: ['midominio.com', 'www.midominio.com']
ALLOWED_HOSTS = ['*']  # Permite todos los hosts (solo para desarrollo)

# ==================== APLICACIONES INSTALADAS ====================

INSTALLED_APPS = [
    # Aplicaciones core de Django
    'django.contrib.admin',        # Panel de administración
    'django.contrib.auth',         # Sistema de autenticación
    'django.contrib.contenttypes', # Framework de tipos de contenido
    'django.contrib.sessions',     # Gestión de sesiones
    'django.contrib.messages',     # Framework de mensajes
    'django.contrib.staticfiles',  # Gestión de archivos estáticos
    
    # Aplicaciones personalizadas del proyecto TodoLap
    'usuarios',     # Gestión de usuarios y autenticación personalizada
    'inventario',   # Control de productos y stock
    'ventas',       # Registro de ventas y facturación
    'servicios',    # Catálogo de servicios y cotizaciones
]

# ==================== MIDDLEWARE ====================

MIDDLEWARE = [
    # Middleware de seguridad (headers de seguridad HTTP)
    'django.middleware.security.SecurityMiddleware',
    
    # Gestión de sesiones de usuario
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # Middleware común (normalización de URLs, etc.)
    'django.middleware.common.CommonMiddleware',
    
    # Protección contra Cross-Site Request Forgery (CSRF)
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Autenticación de usuarios en cada request
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # Sistema de mensajes (flash messages)
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Protección contra clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================== CONFIGURACIONES PARA TÚNELES (Cloudflare/ngrok) ====================

# Permite que la aplicación sea embebida en iframes del mismo origen
# Necesario para túneles de Cloudflare en desarrollo
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Desactiva la política de opener cross-origin para túneles
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# ==================== CONFIGURACIÓN DE URLs ====================

# Archivo principal de enrutamiento
ROOT_URLCONF = 'TodoLap.urls'

# ==================== CONFIGURACIÓN DE TEMPLATES ====================

TEMPLATES = [
    {
        # Motor de plantillas de Django
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # Directorios adicionales para buscar templates
        # Permite templates globales fuera de las apps
        'DIRS': [BASE_DIR / "templates"],
        
        # Permite que cada app tenga su carpeta templates/
        'APP_DIRS': True,
        
        # Procesadores de contexto (variables disponibles en todos los templates)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',      # Variable DEBUG
                'django.template.context_processors.request',    # Variable request
                'django.contrib.auth.context_processors.auth',   # Usuario autenticado
                'django.contrib.messages.context_processors.messages',  # Mensajes flash
            ],
        },
    },
]

# ==================== CONFIGURACIÓN WSGI ====================

# Aplicación WSGI para servidores de producción (Gunicorn, uWSGI, etc.)
WSGI_APPLICATION = 'TodoLap.wsgi.application'

# ==================== CONFIGURACIÓN DE BASE DE DATOS ====================

# --- OPCIÓN 1: POSTGRESQL (ACTUAL) ---
# Base de datos robusta y escalable, ideal para producción
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME', default='TodoLaptop'),      # Nombre de la base de datos
        'USER': config('DB_USER', default='postgres'),        # Usuario de PostgreSQL
        'PASSWORD': config('DB_PASSWORD', default='12345678'), # Contraseña del usuario
        'HOST': config('DB_HOST', default='localhost'),       # Servidor (localhost o IP)
        'PORT': config('DB_PORT', default='5432'),           # Puerto de PostgreSQL
    }
}

# --- OPCIÓN 2: SQLITE (COMENTADA) ---
# Base de datos simple en archivo, ideal para desarrollo rápido
# No requiere instalación de servidor de base de datos
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',  # Archivo de base de datos
#     }
# }

# --- OPCIÓN 3: MYSQL (COMENTADA) ---
# Base de datos popular y ampliamente usada
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'TLP_Manager',       # Nombre de la base de datos
#         'USER': 'root',              # Usuario de MySQL
#         'PASSWORD': '12345678',      # Contraseña del usuario
#         'HOST': '127.0.0.1',         # Servidor MySQL
#         'PORT': '3306',              # Puerto de MySQL
#         'OPTIONS': {
#             # Modo estricto de transacciones
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#         }
#     }
# }

# ==================== VALIDADORES DE CONTRASEÑA ====================

# Validadores para asegurar contraseñas seguras
AUTH_PASSWORD_VALIDATORS = [
    # Evita contraseñas similares a atributos del usuario
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # Requiere una longitud mínima
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # Evita contraseñas comunes
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    # Evita contraseñas puramente numéricas
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==================== CONFIGURACIÓN CSRF PARA TÚNELES ====================

# Cuando se usa un túnel (Cloudflare / ngrok) para demos, Django valida
# el origen (origin) en peticiones POST para CSRF.
# Se debe añadir el dominio HTTPS completo a CSRF_TRUSTED_ORIGINS.
#
# Ejemplos:
#   Cloudflare: https://<subdominio>.trycloudflare.com
#   ngrok:      https://<tu-subdominio>.ngrok-free.app
#
# IMPORTANTE: En producción, usar dominios específicos, NO comodines
CSRF_TRUSTED_ORIGINS = [
    "https://*.trycloudflare.com",  # Demo rápida con Cloudflare Tunnel
    # "https://<tu-subdominio>.ngrok-free.app",  # Descomenta si usas ngrok
]

# ==================== CONFIGURACIONES DE COOKIES ====================

# Configuración de cookies para sesiones y CSRF
# secure=True requiere HTTPS (False para desarrollo local)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)

# SameSite 'Lax' permite cookies cross-site con cierta protección
# Necesario para que funcionen túneles externos
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# ==================== INTERNACIONALIZACIÓN ====================

# Idioma principal del proyecto
LANGUAGE_CODE = 'es-mx'  # Español de México

# Zona horaria para fechas y horas
TIME_ZONE = 'America/Mexico_City'

# Habilitar sistema de traducción de Django
USE_I18N = True

# Usar zonas horarias en la base de datos (recomendado)
USE_TZ = True

# ==================== ARCHIVOS ESTÁTICOS ====================

# URL para acceder a archivos estáticos (CSS, JS, imágenes)
STATIC_URL = '/static/'

# Directorios donde Django busca archivos estáticos
# Permite tener una carpeta static/ global en la raíz del proyecto
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# ==================== ARCHIVOS MEDIA (uploads de usuarios) ====================

# URL para acceder a archivos subidos por usuarios
MEDIA_URL = '/media/'

# Directorio donde se guardan los archivos subidos
MEDIA_ROOT = BASE_DIR / "media"

# ==================== CONFIGURACIÓN DE CAMPOS AUTOMÁTICOS ====================

# Tipo de campo por defecto para claves primarias
# BigAutoField permite hasta ~9 quintillones de registros
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
