# CONTEXT.md — Sistema de Gestión de Trailers

> **INSTRUCCIÓN PERMANENTE:** Cada vez que se realice un cambio en el proyecto (nueva funcionalidad, modificación de modelo, nuevo endpoint, cambio de dependencia, corrección de bug, etc.) se debe actualizar este archivo con una entrada en el historial de cambios y actualizar la sección correspondiente.

---

## 1. Descripción del Proyecto

Aplicación web Django para gestión de viajes de una empresa de trailers/fletamiento. Permite registrar viajes, calcular gastos de diesel automáticamente usando la API de OpenRouteService, y generar reportes mensuales de utilidad y gastos exportables en PDF y Excel.

---

## 2. Datos del Proyecto

| Campo | Valor |
|---|---|
| **Nombre del proyecto Django** | `patios` |
| **Nombre de la app principal** | `trailers` |
| **Framework** | Django 5.2.12 |
| **Python** | 3.13 |
| **Virtual env** | `env\` (Windows) |
| **Base de datos local** | SQLite (fallback) |
| **Base de datos producción** | PostgreSQL — DigitalOcean |
| **Servidor local** | `python manage.py runserver 3000` (puerto 3000, el 8000 estaba ocupado) |
| **Repositorio** | https://github.com/Fernando-Alvarado-Soria/Djandoxd |
| **Rama principal** | `main` |

---

## 3. Estructura de Archivos Clave

```
Djandoxd/
├── .env                          # Variables de entorno locales (NO en git)
├── manage.py
├── requirements.txt
├── CONTEXT.md                    # Este archivo
├── Procfile                      # Para deploy en DigitalOcean App Platform
├── patios/
│   ├── settings.py               # Configuración Django
│   ├── urls.py                   # URLs raíz
│   └── wsgi.py
└── trailers/
    ├── models.py                 # Modelos: Cliente, Operador, TipoUnidad, Unidad, Viaje
    ├── views.py                  # Todas las vistas y lógica de negocio
    ├── urls.py                   # URLs de la app trailers
    ├── forms.py                  # ViajeForm y AdminUserCreationForm
    ├── admin.py                  # Registro de modelos en Django Admin
    ├── migrations/               # 0001 al 0009 aplicadas
    └── templates/trailers/
        ├── base.html             # Template base con navbar, dark mode, Bootstrap 5
        ├── lista_viajes.html     # Listado de todos los viajes
        ├── agregar_viaje.html    # Formulario nuevo viaje + JS cálculo diesel
        ├── editar_viaje.html     # Formulario edición viaje + JS cálculo diesel
        ├── detalle_viaje.html    # Vista solo lectura de un viaje
        ├── borrar_viaje.html     # Confirmación de borrado
        ├── reportes.html         # Dashboard de reportes mensuales
        └── registration/
            └── login.html
```

---

## 4. Variables de Entorno (.env)

El archivo `.env` está en la raíz del proyecto y **no se sube a git** (está en `.gitignore`).

```env
DEBUG=True
SECRET_KEY=p^7m-_5o0tts$#kz#=*cv39a&2*52fy!g&x2!2x8^x-r#!=3x+
ALLOWED_HOSTS=localhost,127.0.0.1,.ondigitalocean.app
DATABASE_URL=postgresql://dev-db-246747:AVNS_25IXDfHBsacqt1oWTRH@app-1da7fb19-99d6-4d9c-8572-7c9f8053fefd-do-user-30743590-0.h.db.ondigitalocean.com:25060/dev-db-246747?sslmode=require
ORS_API_KEY=eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijg1MWQ2MDE0N2U5NTQzMDA5N2EwMmFkOTgxMDhkNmQ5IiwiaCI6Im11cm11cjY0In0=
```

**En producción (DigitalOcean):** estas variables se configuran en el panel de DigitalOcean → Apps → Settings → Environment Variables (con `ORS_API_KEY` marcada como Encrypt).

---

## 5. Base de Datos

### Producción — DigitalOcean PostgreSQL

| Campo | Valor |
|---|---|
| **Host** | `app-1da7fb19-99d6-4d9c-8572-7c9f8053fefd-do-user-30743590-0.h.db.ondigitalocean.com` |
| **Puerto** | `25060` |
| **Base de datos** | `dev-db-246747` |
| **Usuario** | `dev-db-246747` |
| **SSL** | `sslmode=require` |

La DB de desarrollo también es la misma de DigitalOcean (no se usa SQLite local). La conexión se configura automáticamente a través de `DATABASE_URL` usando `dj-database-url`.

### Migraciones aplicadas

| Migración | Descripción |
|---|---|
| `0001_initial` | Modelo base Viaje |
| `0002_alter_viaje_ganancia` | Ganancia nullable |
| `0003_viaje_fecha_pago_viaje_fecha_viaje_and_more` | Fechas y campos adicionales |
| `0004_alter_viaje_id` | Cambio de ID |
| `0005_cliente_operador_unidad` | Nuevos modelos Cliente, Operador, Unidad |
| `0006_unidad_rendimiento_km_litro_viaje_km_distancia_and_more` | Campos de combustible y km en Unidad y Viaje |
| `0007_tipounidad_viaje_tipo_unidad` | Modelo TipoUnidad, FK en Viaje |
| `0008_seed_tipos_unidad` | Data migration: 9 tipos de unidad precargados |
| `0009_alter_viaje_precio_diesel_litro` | precio_diesel_litro a 3 decimales |

---

## 6. Dependencias (requirements.txt)

```
Django==5.2.12
gunicorn==23.0.0
dj-database-url==2.3.0
python-decouple==3.8
whitenoise==6.8.2
psycopg2-binary==2.9.10
requests==2.32.3
reportlab==4.5.1
openpyxl==3.1.5
```

| Paquete | Para qué se usa |
|---|---|
| `Django` | Framework principal |
| `gunicorn` | Servidor WSGI para producción |
| `dj-database-url` | Parsea `DATABASE_URL` en dict de Django |
| `python-decouple` | Lee variables del `.env` con `config()` |
| `whitenoise` | Sirve archivos estáticos en producción |
| `psycopg2-binary` | Adaptador PostgreSQL para Python |
| `requests` | Llamadas HTTP a la API de OpenRouteService |
| `reportlab` | Generación de PDFs |
| `openpyxl` | Generación de archivos Excel (.xlsx) |

---

## 7. Modelos de Base de Datos

### `Cliente`
| Campo | Tipo | Notas |
|---|---|---|
| `nombre` | CharField(200) | |
| `rfc` | CharField(13) | Único, validado con regex |
| `activo` | BooleanField | default=True |
| `fecha_creacion` | DateTimeField | auto_now_add |
| `fecha_actualizacion` | DateTimeField | auto_now |

### `Operador`
| Campo | Tipo | Notas |
|---|---|---|
| `nombre` | CharField(200) | |
| `licencia` | CharField(50) | Único |
| `activo` | BooleanField | default=True |
| `fecha_creacion` | DateTimeField | auto_now_add |
| `fecha_actualizacion` | DateTimeField | auto_now |

### `TipoUnidad`
| Campo | Tipo | Notas |
|---|---|---|
| `nombre` | CharField(100) | Ej: "Tractocamión 3 ejes" |
| `descripcion` | TextField | Opcional |
| `rendimiento_km_litro` | DecimalField(5,2) | Ej: 3.50 km/L |

**9 tipos precargados:** Tractocamión 3 ejes, Camión sencillo, Rabón, Torton, Full, Mega, Doble remolque, Plataforma 3 ejes, Caja seca 53 pies.

### `Unidad`
| Campo | Tipo | Notas |
|---|---|---|
| `numero_economico` | CharField(50) | Único |
| `placas` | CharField(20) | Único |
| `marca` | CharField(100) | |
| `modelo` | CharField(100) | |
| `anio` | PositiveIntegerField | |
| `rendimiento_km_litro` | DecimalField(5,2) | default=3.50 |
| `activo` | BooleanField | default=True |
| `fecha_creacion` | DateTimeField | auto_now_add |
| `fecha_actualizacion` | DateTimeField | auto_now |

### `Viaje` (modelo principal)
| Campo | Tipo | Notas |
|---|---|---|
| `numero_viaje` | CharField(100) | Único, es el ID de negocio |
| `numero_contenedor` | CharField(100) | Opcional |
| `numero_factura` | CharField(100) | Opcional |
| `unidad` | FK → Unidad | SET_NULL, opcional |
| `tipo_unidad` | FK → TipoUnidad | SET_NULL, opcional |
| `origen` | CharField(200) | Ciudad de origen |
| `destino` | CharField(200) | Ciudad de destino |
| `km_distancia` | DecimalField(10,2) | Calculado por ORS, solo ida |
| `viaje_redondo` | BooleanField | default=False |
| `precio_diesel_litro` | DecimalField(8,3) | 3 decimales, ej: 28.015 |
| `pagado` | BooleanField | default=False |
| `fecha_pago` | DateField | Opcional |
| `fecha_viaje` | DateField | **REQUERIDO para aparecer en reportes** |
| `gastos_casetas` | DecimalField(10,2) | default=0 |
| `gastos_diesel` | DecimalField(10,2) | default=0, auto-calculado en frontend |
| `otros_gastos` | DecimalField(10,2) | default=0 |
| `costo_viaje` | DecimalField(10,2) | Lo que cobra la empresa |
| `ganancia` | DecimalField(10,2) | Opcional |
| `fecha_creacion` | DateTimeField | auto_now_add |
| `fecha_actualizacion` | DateTimeField | auto_now |

**Cálculo de utilidad:** `utilidad = costo_viaje - gastos_diesel - gastos_casetas - otros_gastos`

---

## 8. URLs de la Aplicación

| URL | Nombre | Vista | Descripción |
|---|---|---|---|
| `/` | `lista_viajes` | `lista_viajes` | Lista todos los viajes |
| `/agregar/` | `agregar_viaje` | `agregar_viaje` | Formulario nuevo viaje |
| `/editar/<id>/` | `editar_viaje` | `editar_viaje` | Formulario edición |
| `/borrar/<id>/` | `borrar_viaje` | `borrar_viaje` | Confirmar borrado |
| `/viaje/<id>/` | `detalle_viaje` | `detalle_viaje` | Vista solo lectura |
| `/accounts/login/` | `login` | Django built-in | Login |
| `/accounts/logout/` | `logout` | Django built-in | Logout |
| `/accounts/register/` | `register` | `register` | Crear usuario (solo staff) |
| `/api/calcular-distancia/` | `calcular_distancia` | `calcular_distancia` | GET, retorna JSON `{km: float}` |
| `/reportes/` | `reportes` | `reportes` | Dashboard reportes mensuales |
| `/reportes/exportar/excel/` | `exportar_reporte_excel` | `exportar_reporte_excel` | Descarga .xlsx |
| `/reportes/exportar/pdf/` | `exportar_reporte_pdf` | `exportar_reporte_pdf` | Descarga .pdf |
| `/admin/` | — | Django Admin | Panel admin |

**Parámetros de query:** `/reportes/?anio=2026`, `/reportes/exportar/excel/?anio=2026`

---

## 9. API de OpenRouteService (ORS)

| Campo | Valor |
|---|---|
| **API Key** | `eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijg1MWQ2MDE0N2U5NTQzMDA5N2EwMmFkOTgxMDhkNmQ5IiwiaCI6Im11cm11cjY0In0=` |
| **Plan** | Standard (gratuito) — 2000 req/día Directions, 3000 Geocoding |
| **Endpoints usados** | `GET /geocode/search` y `POST /v2/directions/driving-car` |
| **Perfil de ruta** | `driving-car` (driving-hgv no tiene datos para México, solo Europa) |
| **Variable de entorno** | `ORS_API_KEY` en `.env` y en DigitalOcean |
| **Setting Django** | `ORS_API_KEY = config('ORS_API_KEY', default='')` en `settings.py` |

**Flujo del endpoint `/api/calcular-distancia/`:**
1. Recibe `?origen=...&destino=...` (nombres de ciudades)
2. Geocodifica origen → coordenadas `[lon, lat]` con `boundary.country=MX`
3. Geocodifica destino → coordenadas `[lon, lat]`
4. Llama a `POST /v2/directions/driving-car` con las dos coordenadas
5. Retorna `{"km": float}` o `{"error": "..."}` con código HTTP apropiado

---

## 10. Lógica de Reportes

Los reportes filtran viajes por `fecha_viaje__year=anio` y `fecha_viaje__isnull=False`.

> ⚠️ **Importante:** Un viaje **solo aparece en el reporte** si tiene el campo `fecha_viaje` lleno. Si está vacío, no aparece.

**Cálculos en el reporte:**
- `total_gastos = gastos_diesel + gastos_casetas + otros_gastos`
- `utilidad = costo_viaje - total_gastos`
- Si `utilidad < 0` → se muestra en **rojo** como pérdida
- Si `utilidad >= 0` → se muestra en **verde** como ganancia

**Secciones del reporte:**
1. **Resumen mensual:** agrupado por mes (`TruncMonth`), incluye los números de viaje del mes como enlaces al detalle
2. **Por unidad:** agrupado por `unidad__numero_economico`, ordenado de mayor a menor utilidad
3. **Detalle por viaje:** tabla completa viaje a viaje, con link al detalle

**Exportaciones:**
- **Excel (.xlsx):** 3 hojas — Resumen Mensual, Por Unidad, Detalle Viajes. Colores verde/rojo en columna utilidad.
- **PDF:** Documento horizontal (landscape letter) con las 3 secciones. Generado con `reportlab`.

---

## 11. Frontend

- **CSS Framework:** Bootstrap 5.3 (CDN)
- **Iconos:** Font Awesome 6.4 (CDN)
- **Dark Mode:** Implementado con CSS variables en `base.html`, toggle guardado en `localStorage`
- **Template base:** `trailers/base.html` — todos los demás templates extienden de este
- **Navbar incluye:** Lista de Viajes, Agregar Viaje, 📊 Reportes, Panel Admin, Cerrar sesión, Toggle dark mode

**JS en formularios de viaje (agregar/editar):**
- `getRendimiento()` → lee el rendimiento del tipo de unidad seleccionado
- `calcularGastosDiesel()` → calcula automáticamente `gastos_diesel = (km_total / rendimiento) * precio_litro`
- `actualizarStatusKm()` → muestra km ida o km×2 si es viaje redondo
- `calcularDistancia()` → llama al endpoint ORS y rellena el campo `km_distancia`

---

## 12. Autenticación y Permisos

- Login requerido en todas las vistas (`@login_required`)
- Crear usuarios: solo accesible para `is_staff=True` (`@user_passes_test(staff_check)`)
- No hay roles de cliente ni vistas públicas — todos los usuarios son administradores por el momento
- `LOGIN_REDIRECT_URL = '/'`, `LOGOUT_REDIRECT_URL = '/'`, `LOGIN_URL = '/accounts/login/'`

---

## 13. Deploy — DigitalOcean App Platform

- **Procfile:** `web: gunicorn patios.wsgi`
- **runtime.txt:** especifica versión de Python
- **Variables de entorno en producción:** configuradas en el panel de DigitalOcean (DEBUG=False, SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS, ORS_API_KEY)
- **Archivos estáticos:** servidos por `whitenoise` con `CompressedManifestStaticFilesStorage`
- **HTTPS:** forzado en producción mediante `SECURE_SSL_REDIRECT = True` (cuando `DEBUG=False`)

---

## 14. Historial de Cambios

| Fecha | Cambio |
|---|---|
| Inicio | Setup inicial: Django + PostgreSQL DigitalOcean + .env local |
| Inicio | Limpieza de __pycache__ del tracking de git |
| — | Modelo `Viaje` base con campos de costo, gastos, origen, destino |
| — | Modelos `Cliente`, `Operador`, `Unidad` (migración 0005) |
| — | Campo `rendimiento_km_litro` en `Unidad`; campos `km_distancia`, `viaje_redondo`, `precio_diesel_litro`, `unidad` en `Viaje` (migración 0006) |
| — | Modelo `TipoUnidad` con rendimiento típico; FK `tipo_unidad` en `Viaje` (migración 0007) |
| — | Data migration 0008: 9 tipos de unidad precargados |
| — | Migración 0009: `precio_diesel_litro` cambiado a 3 decimales |
| — | Integración OpenRouteService: endpoint `/api/calcular-distancia/`, cálculo automático de diesel en frontend |
| — | Cambio de perfil ORS de `driving-hgv` a `driving-car` (hgv no cubre México) |
| — | Vista `detalle_viaje` (solo lectura) + `numero_viaje` clickeable en lista |
| — | `ORS_API_KEY` agregada como variable de entorno en DigitalOcean producción |
| 2026-05-26 | Módulo de reportes: vista `/reportes/`, exportar Excel y PDF, resumen mensual + por unidad + detalle por viaje |
| 2026-05-26 | Enlace 📊 Reportes agregado al navbar en `base.html` |
| 2026-05-26 | `reportlab==4.5.1` y `openpyxl==3.1.5` agregados a `requirements.txt` |
| 2026-06-03 | Creación de `CONTEXT.md` con documentación completa del proyecto |
| 2026-06-03 | Resumen mensual de reportes actualizado para mostrar números de viaje con enlaces al detalle |
