# Sistema de Control de Entrada y Salida — Personal de Seguridad

Sistema web desarrollado con **Django 5** y **SQLite** para registrar y gestionar los ingresos y salidas del personal de seguridad de una organización.

---

## Características

- Registro de entrada con hora automática
- Registro de salida con motivo obligatorio y área de destino
- Consulta de registros con filtros (fecha, nombre, motivo, área)
- Reporte de movimientos exportable a CSV
- Autenticación con tres roles: **Administrador**, **Supervisor**, **Consulta**
- Gestión de personal y catálogo de áreas
- Panel de administración Django integrado

## Reglas de negocio

- No se puede registrar salida sin entrada previa
- El motivo de salida es obligatorio
- El área de destino se selecciona de un catálogo predefinido
- Los registros son de solo lectura (no se modifican ni eliminan)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 2. Crear y activar el entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install django
```

### 4. Aplicar migraciones

```bash
cd sistema
python manage.py migrate
```

### 5. Cargar datos iniciales

```bash
python manage.py cargar_datos_iniciales
```

### 6. Iniciar el servidor

```bash
python manage.py runserver
```

Accede en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador (acceso total) |
| `supervisor` | `super123` | Supervisor (registra entradas/salidas) |
| `consulta` | `consulta123` | Solo lectura |

---

## Estructura del proyecto

```
ControlEntrada/
├── sistema/                  # Proyecto Django
│   ├── control/              # App principal
│   │   ├── migrations/
│   │   ├── management/commands/cargar_datos_iniciales.py
│   │   ├── models.py         # Personal, Area, Entrada, Salida, Perfil
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── decorators.py
│   ├── templates/control/    # Templates HTML (Bootstrap 5)
│   ├── sistema/              # Configuración Django
│   └── manage.py
└── README.md
```

## Tecnologías

- Python 3.10+
- Django 5.2
- SQLite 3
- Bootstrap 5.3
- Bootstrap Icons
