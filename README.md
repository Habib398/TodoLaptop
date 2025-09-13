# TodoLaptop
---CUALQUIER DUDA QUEDO A TU DISPOSICION CON PABLO (cuidate(opcional))---

Aplicación Django para gestión básica de inventario, ventas, servicios y usuarios. Incluye CRUD de productos con modales y mensajes de confirmación.

## Requisitos previos

- Python 3.10+ (recomendado el que usas en tu entorno actual)
- Git
- (Opcional) Virtualenv / venv
- Nota: PREFERIBLEMENTE TODOS LOS COMANDOS RELACIONADOS A LA INSTALACION DE DEPENDENCIAS Y LIBRERIAS USA LA TERMINAL DE VISUAL STUDIO

## Clonar el repositorio

```bash
git clone https://github.com/<TU_USUARIO>/<TU_REPO>.git
cd <TU_REPO>
```
Reemplaza `<TU_USUARIO>` y `<TU_REPO>` por los reales.

## Crear y activar entorno virtual

Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

Si agregas más librerías después, recuerda actualizar `requirements.txt` con:
```bash
pip freeze > requirements.txt
```

### Instalación manual (si prefieres comando por comando)

Si no deseas usar `requirements.txt`, puedes instalar las librerías clave manualmente:

```bash
pip install django==5.2.5
```

Librerías opcionales que podrías querer añadir más adelante:

| Librería | Comando | Uso previsto |
|----------|---------|--------------|
| Pillow | `pip install Pillow` | Manejo de imágenes (si agregas campos ImageField) |
| python-dotenv | `pip install python-dotenv` | Cargar variables desde `.env` |
| whitenoise | `pip install whitenoise` | Servir estáticos en producción simple |
| gunicorn | `pip install gunicorn` | Servidor WSGI para despliegues Linux |

Después de instalar cualquiera de ellas, no olvides congelar versiones:
```bash
pip freeze > requirements.txt
```

## Configuración inicial

Asegúrate de que el archivo `TodoLap/settings.py` tiene `INSTALLED_APPS` con las apps: `inventario`, `usuarios`, `ventas`, `servicios`.

## Migraciones

Generar (si fuera necesario) y aplicar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

> El repo ya incluye migraciones. Generalmente bastará con `migrate`.

### ¿Qué son y para qué sirven las migraciones?

Las migraciones son archivos que describen los cambios en tu modelo de datos (tablas y columnas) a lo largo del tiempo. Django las genera comparando tus modelos Python con el estado actual de la base de datos.

Funcionan como un “historial versionado” del esquema. Cada migración contiene instrucciones (crear tabla, añadir campo, renombrar, eliminar, etc.) que Django ejecuta en orden.

Flujo típico:
1. Modificas un modelo en `models.py` (por ejemplo, agregas un campo).
2. Ejecutas `python manage.py makemigrations` → Django crea un nuevo archivo en `app/migrations/` con la operación.
3. Ejecutas `python manage.py migrate` → Aplica esas operaciones a la base de datos real (SQLite, PostgreSQL, etc.).

Beneficios clave:
- Permite trabajar en equipo sin perder sincronización del esquema.
- Evita tener que escribir SQL manual.
- Facilita revertir cambios (rollback) si es necesario.
- Mantiene un registro claro de la evolución del modelo de datos.

Si la base de datos se “desincroniza” (errores de campos inexistentes) en desarrollo, puedes borrar `db.sqlite3` y volver a ejecutar `migrate` (solo recomendado si no necesitas los datos existentes).

Para ver el plan de migraciones pendiente:
```bash
python manage.py showmigrations
```
Para revertir (ejemplo volver a un estado anterior):
```bash
python manage.py migrate inventario 0001
```
Lo anterior aplicará solo hasta la migración `0001` de la app `inventario`.

## Base de datos

### SQLite (por defecto)
Este proyecto usa SQLite por defecto. No necesitas crear nada manualmente: al ejecutar por primera vez:
```bash
python manage.py migrate
```
Se generará el archivo `db.sqlite3` en la raíz del proyecto con todas las tablas.

Si quieres “reiniciar” la base de datos en desarrollo:
```bash
del db.sqlite3              # Windows PowerShell / CMD
python manage.py migrate    # Recrea estructura
```
o en Linux/macOS:
```bash
rm db.sqlite3
python manage.py migrate
```

### Notas
- Para usar otra base de datos (PostgreSQL, MySQL, MariaDB, etc.) modifica `DATABASES` en `settings.py` siguiendo la documentación oficial de Django.

## Crear superusuario (para admin)
```bash
python manage.py createsuperuser
```
Sigue las instrucciones interactivas.

## Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```
Abre en el navegador: http://127.0.0.1:8000/

## Flujo de autenticación
- La raíz redirige a `/login/`.
- Tras autenticación se accede al dashboard (`/dashboard/`).
- Desde dashboard se puede ir al inventario.

## CRUD de Inventario
- Página: `/inventario/`
- Modal "Agregar nuevo" permite crear producto.
- Selecciona una fila para habilitar "Editar" y "Eliminar" (si se mantiene la versión con acciones en modales).
- Mensajes de éxito aparecen como toasts en la esquina inferior derecha.

## Estructura de la aplicación
```
TodoLap/          # Configuración principal
inventario/       # CRUD de productos
usuarios/         # Login / dashboard
ventas/           # (Lógica de ventas - placeholder inicial)
servicios/        # (Servicios - placeholder inicial)
static/           # Archivos estáticos
```

## Variables de entorno (opcional)
Si deseas usar un `.env`, instala `python-dotenv` y luego en `manage.py` / `settings.py` cargar variables. Ejemplo:
```bash
pip install python-dotenv
```
Ejemplo `.env`:
```
SECRET_KEY=tu_clave_segura
DEBUG=True
```
Luego en `settings.py`:
```python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)
DEBUG = os.getenv('DEBUG', 'True') == 'True'
```

## Actualizar dependencias
1. Instala/actualiza paquetes:
```bash
pip install <paquete>
```
2. Congela versión:
```bash
pip freeze > requirements.txt
```
3. Haz commit de los cambios.

## Tests (si se agregan a futuro)
Ejecutar:
```bash
python manage.py test
```

## Despliegue rápido (ejemplo con Railway / Render / etc.)
1. Configurar variable `SECRET_KEY` y `DEBUG=False`.
2. Ejecutar migraciones en el servidor.
3. Recoger estáticos:
```bash
python manage.py collectstatic --noinput
```
4. Asegurar que se sirve `static/` (según plataforma).