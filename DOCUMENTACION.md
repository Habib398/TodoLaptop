# 📖 TodoLap - Sistema de Gestión para Reparación de Laptops

## 🎯 Descripción General
TodoLap es un sistema web desarrollado con Django para gestionar el negocio de reparación y venta de productos para laptops. Permite controlar inventario, servicios técnicos, ventas y usuarios con diferentes roles.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.1.3 (Python)
- **Base de Datos**: PostgreSQL (con psycopg2-binary)
- **Frontend**: HTML, CSS, JavaScript
- **Librerías adicionales**:
  - Django REST Framework (APIs)
  - ReportLab (Generación de PDFs)
  - OpenPyXL (Exportación a Excel)
  - Pillow (Manejo de imágenes)
  - python-decouple (Variables de entorno)

---

## 🗄️ Base de Datos

### Estructura General
La base de datos utiliza **PostgreSQL** y está organizada en 4 módulos principales:

#### Tablas Principales:
1. **Usuario** (usuarios_usuario)
   - Gestiona usuarios con roles (admin/técnico)
   - Hereda de AbstractUser de Django

2. **Producto** (inventario_producto)
   - Almacena productos con nombre, descripción, precio y stock

3. **Servicio** (servicios_servicio)
   - Registra servicios técnicos con descripción, costo y técnico asignado
   - Relaciona productos utilizados en el servicio

4. **ServicioPagado** (servicios_serviciopagado)
   - Almacena cotizaciones y servicios pagados
   - Estados: cotizado/pagado

5. **Venta** (ventas_venta)
   - Registra ventas con total y método de pago

6. **DetalleVenta** (ventas_detalleventa)
   - Detalle de productos vendidos en cada venta

---

## 📦 Módulos del Sistema

### 1️⃣ **Inventario**
**Función**: Gestión de productos disponibles para venta y reparaciones.

**Características**:
- Agregar, editar y eliminar productos
- Control de stock (cantidad disponible)
- Registro de precio y descripción
- Validación de stock antes de ventas

**Modelo Principal**: `Producto`
- nombre
- descripcion
- precio
- cantidad_stock

---

### 2️⃣ **Servicios**
**Función**: Administración de servicios técnicos y cotizaciones.

**Características**:
- Crear servicios de reparación
- Asignar técnico responsable
- Asociar productos utilizados en el servicio
- Generar cotizaciones para clientes
- Marcar servicios como pagados
- Calcular costos totales (servicio + productos)

**Modelos Principales**:
- `Servicio`: Servicios básicos con técnico y productos
- `ServicioPagado`: Cotizaciones y servicios facturados
- `ProductoServicioPagado`: Relación de productos usados en cada servicio

---

### 3️⃣ **Usuarios**
**Función**: Control de acceso y gestión de personal.

**Características**:
- Sistema de autenticación de Django
- Dos roles principales:
  - **Admin**: Acceso completo al sistema
  - **Técnico**: Gestión de servicios técnicos
- Login y logout
- Dashboard personalizado según rol

**Modelo Principal**: `Usuario`
- Extiende AbstractUser de Django
- Campo adicional: `rol` (admin/técnico)

---

### 4️⃣ **Ventas**
**Función**: Registro de ventas de productos directas.

**Características**:
- Crear ventas con múltiples productos
- Cálculo automático de totales
- Registro de método de pago (efectivo, tarjeta, etc.)
- Descuento automático de stock al vender
- Historial de ventas

**Modelos Principales**:
- `Venta`: Encabezado de venta con total y método de pago
- `DetalleVenta`: Detalle de productos vendidos (cantidad, precio, subtotal)

---

## 🔄 Flujo de Trabajo

### Venta de Productos:
1. Usuario selecciona productos del inventario
2. Sistema verifica stock disponible
3. Se crea una Venta con sus DetalleVenta
4. Se actualiza el stock automáticamente
5. Se calcula el total de la venta

### Servicio Técnico:
1. Se crea un Servicio con descripción y técnico asignado
2. Se agregan productos necesarios (opcional)
3. Se genera cotización (ServicioPagado en estado "cotizado")
4. Al pagar, se cambia estado a "pagado"
5. Se descuenta el stock de productos utilizados

---

## 📁 Estructura de Archivos

```
TODOLAP/
├── inventario/      # Módulo de productos
├── servicios/       # Módulo de servicios técnicos
├── usuarios/        # Autenticación y roles
├── ventas/          # Registro de ventas
├── static/          # CSS y JavaScript
├── fixtures/        # Datos iniciales (JSON)
├── Scripts/         # Scripts de automatización (PowerShell)
└── TodoLap/         # Configuración principal de Django
```

---

## 🚀 Scripts de Automatización

El sistema incluye scripts PowerShell para facilitar la administración:

- **Complete_Setup.ps1**: Configuración completa inicial
- **Setup_Database.ps1**: Configuración de base de datos
- **Load_Initial_Data.ps1**: Carga datos de prueba
- **Start_TodoLap.ps1**: Inicia el servidor Django
- **Stop_TodoLap.ps1**: Detiene el servidor
- **Export_Data.ps1**: Exporta datos de la BD

---

## 🔐 Seguridad

- Autenticación basada en Django Auth
- Control de acceso por roles
- CSRF protection activado
- Variables sensibles en archivo `.env`
- Validación de permisos en vistas

---

## 📊 Características Adicionales

- **Exportación de datos**: Excel y PDF
- **API REST**: Endpoints para integración externa
- **Responsive Design**: Interfaz adaptable
- **Dashboard**: Vista general de métricas del negocio
- **Fixtures**: Datos de prueba incluidos

---

## 💡 Resumen de Funcionalidades

| Módulo | Función Principal |
|--------|------------------|
| **Inventario** | Control de productos y stock |
| **Servicios** | Gestión de reparaciones y cotizaciones |
| **Usuarios** | Autenticación y control de roles |
| **Ventas** | Registro de ventas directas |

---

**Desarrollado con Django 5.1.3 y PostgreSQL**
