# INSTALACIÓN - TodoLap
## Para Clientes / Nuevos Usuarios

---

## PASO 1: Requisitos Previos (5 minutos)

### A) Instalar Python
1. Descargar: https://www.python.org/downloads/
2. Durante instalación: ✅ Marcar "Add Python to PATH"
3. Verificar: Abrir PowerShell y ejecutar:
   ```powershell
   python --version
   ```
   Debe mostrar: Python 3.10.x o superior

### B) Instalar PostgreSQL
1. Descargar: https://www.postgresql.org/download/windows/
2. Durante instalación:
   - Recordar la contraseña que pongas
   - Puerto predeterminado: 5432
3. Verificar que el servicio esté corriendo:
   - Buscar "Services" en Windows
   - Buscar "postgresql-x64-XX"
   - Estado debe ser: "Running"

### C) Crear la Base de Datos
1. Abrir "pgAdmin" (instalado con PostgreSQL)
2. Conectar al servidor local (usuario: postgres)
3. Click derecho en "Databases" → "Create" → "Database"
4. Nombre: `TodoLaptop`
5. Click "Save"

### D) Configurar Variables de Entorno
1. En la carpeta del proyecto, encontrar el archivo `.env.example`
2. Hacer una copia y renombrarla a `.env`
3. Abrir `.env` con un editor de texto (Notepad, VS Code, etc.)
4. Editar las credenciales de PostgreSQL:
   ```
   DB_NAME=TodoLaptop
   DB_USER=postgres
   DB_PASSWORD=TU_CONTRASEÑA_AQUI
   DB_HOST=localhost
   DB_PORT=5432
   ```
5. Guardar el archivo

**⚠️ IMPORTANTE:** El archivo `.env` NO debe compartirse públicamente.

---

## PASO 2: Instalación Automática (1 comando)

1. Abrir PowerShell en la carpeta del proyecto
2. Ejecutar:
   ```powershell
   .\Scripts\Complete_Setup.ps1
   ```

3. Responder las preguntas:
   - **¿Deseas continuar?** → Escribe `S` y presiona Enter
   - **¿Cargar datos iniciales?** → Escribe `S` (si hay carpeta fixtures/)
   - **¿Crear usuario administrador?** → Escribe `S` y sigue instrucciones

4. **Esperar...** (puede tomar 2-5 minutos)

---

## PASO 3: Iniciar la Aplicación

```powershell
.\Scripts\Start_TodoLap.ps1
```

Abrir navegador en: **http://127.0.0.1:8000**

---

## Para Detener el Servidor

```powershell
.\Scripts\Stop_TodoLap.ps1
```

O simplemente: **Ctrl + C** en la ventana del servidor

---

## SOLUCIÓN DE PROBLEMAS

### Error: "Python no está instalado"
- Instalar Python desde: https://www.python.org/downloads/
- Marcar "Add Python to PATH" durante instalación

### Error: "No se puede conectar a PostgreSQL"
- Verificar que PostgreSQL esté corriendo (Services de Windows)
- Verificar las credenciales en el archivo `.env`
- Asegurarse de que la contraseña sea la correcta

### Error: "Base de datos no existe"
- Abrir pgAdmin
- Crear base de datos llamada `TodoLaptop`

### Error al cargar datos
- Si no existe carpeta `fixtures/`, omite ese paso
- Los datos se pueden agregar después manualmente

### ¿No ve los datos después de instalar?
```powershell
.\Scripts\Load_Initial_Data.ps1
```