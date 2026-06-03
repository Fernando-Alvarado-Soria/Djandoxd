# Instrucciones para GitHub Copilot — Djandoxd

## REGLA OBLIGATORIA: Actualizar CONTEXT.md

**Cada vez que se realice cualquier cambio en el proyecto, se DEBE actualizar el archivo `CONTEXT.md`** en la sección correspondiente:

- **Nuevo modelo o campo:** actualizar sección 7 (Modelos) y sección 14 (Historial)
- **Nueva migración:** actualizar sección 5 (Migraciones aplicadas) y sección 14
- **Nueva URL o vista:** actualizar sección 8 (URLs) y sección 14
- **Nueva dependencia:** actualizar sección 6 (Dependencias) y `requirements.txt`
- **Cambio de lógica de negocio:** actualizar sección correspondiente y sección 14
- **Nuevo template o cambio de frontend:** actualizar sección 11 (Frontend) y sección 14
- **Cambio de configuración/deploy:** actualizar sección 2, 4 o 13 según corresponda

El formato de entrada en el historial es: `| YYYY-MM-DD | Descripción del cambio |`

---

## Contexto del Proyecto

Lee siempre `CONTEXT.md` antes de hacer cambios para entender el estado actual del proyecto. El archivo contiene:
- Arquitectura completa y estructura de archivos
- Todos los modelos y sus campos
- Variables de entorno y API keys
- Lógica de negocio de reportes y cálculo de diesel
- Historial cronológico de todos los cambios

## Convenciones del Proyecto

- **Framework:** Django 5.2.12, Python 3.13
- **App principal:** `trailers` (proyecto: `patios`)
- **Templates:** extienden de `trailers/base.html` con Bootstrap 5 y dark mode
- **Puerto local:** 3000 (`python manage.py runserver 3000`)
- **Variables de entorno:** usar siempre `config('VARIABLE', default=...)` de `python-decouple`
- **Login requerido:** todas las vistas usan `@login_required`
- **Vistas solo para staff:** usar `@user_passes_test(staff_check)`
- **ORS Profile:** usar `driving-car` (NO `driving-hgv`, no tiene datos para México)
- **Reporte:** solo incluye viajes con `fecha_viaje` lleno (no nulo)
- **Utilidad:** `costo_viaje - gastos_diesel - gastos_casetas - otros_gastos`
