# 2 - Arquitectura

El proyecto usa una arquitectura por capas con FastAPI, SQLAlchemy, Alembic y MySQL.

La separacion busca que cada parte tenga una responsabilidad clara: los controllers reciben requests, los services aplican reglas de negocio, los repositories acceden a base de datos y los models representan las tablas.

## Estructura principal

```text
app/
|- core/
|- controller/
|- services/
|- repositories/
|- models/
|- dto/
|- enums/
`- db/
```

## Responsabilidades

- `core`: centraliza configuracion de la aplicacion.
- `controller`: define endpoints HTTP y delega la logica.
- `services`: contiene casos de uso y reglas del sistema.
- `repositories`: encapsula consultas y operaciones de persistencia.
- `models`: define entidades SQLAlchemy.
- `dto`: define contratos de entrada y salida de la API.
- `enums`: centraliza codigos conocidos de catalogos y seguridad.
- `db`: configura la conexion, session y base declarativa.

## Organizacion por dominio

Los paquetes internos se agrupan por area:

- `catalog`: tablas de referencia y estados.
- `inventory`: items alquilables y copias fisicas.
- `rental`: clientes, rentas y detalles de renta.
- `security`: usuarios, roles, permisos y relacion rol-permiso.

## Base de datos

Las migraciones se manejan con Alembic.

La configuracion local nace desde `.env.example` y se copia a `.env`.

Docker Compose usa las variables de `.env` para crear el contenedor MySQL. La aplicacion y Alembic usan `DATABASE_URL`, tambien definida en `.env`, y la leen desde `app/core/config.py`.

Orden actual:

1. `0001_create_inventory_schema.py`
2. `0002_create_security_schema.py`
3. `0003_create_rental_schema.py`
4. `0004_seed_catalogs.py`

Los catalogos se cargan con seed inicial y la aplicacion debe referenciarlos por `code`, no por strings sueltos.
