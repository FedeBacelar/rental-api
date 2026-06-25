# RentalApi

API base para el trabajo practico de sistema de alquiler de peliculas y videojuegos.

El proyecto utiliza FastAPI, SQLAlchemy, Alembic, MySQL y Docker Compose.

## Requisitos

- Python 3.11 o superior
- Docker Desktop

Docker Desktop se usa para levantar la base MySQL del proyecto de forma local y sin instalar MySQL directamente en la PC.

Si no se cuenta con Docker Desktop, se puede usar una instalacion local de MySQL como alternativa. En ese caso, hay que crear la base de datos manualmente y ajustar la configuracion de conexion de la API.

## Como levantar el proyecto

Ejecutar los comandos desde la carpeta raiz del proyecto, donde se encuentra `docker-compose.yml`.

1. Crear el archivo de configuracion local:

El proyecto incluye `.env.example` como plantilla. Para trabajar localmente, copiamos esa plantilla a `.env`.

```powershell
Copy-Item .env.example .env
```

El archivo `.env` queda fuera del repo y contiene la configuracion local de conexion.

2. Levantar los servicios con Docker Compose:

Usamos Docker para ejecutar MySQL dentro de un contenedor. Docker Compose lee el archivo `docker-compose.yml` y crea ese contenedor con la configuracion del proyecto.

```powershell
docker compose up -d
```

La opcion `-d` deja el contenedor ejecutandose en segundo plano.

3. Crear el entorno virtual:

Un entorno virtual es una carpeta local donde Python instala las dependencias de este proyecto sin mezclarlas con las de otros proyectos o con la instalacion global de Python.

```powershell
python -m venv .venv
```

4. Instalar dependencias:

El archivo `requirements.txt` contiene las librerias Python que necesita el proyecto, por ejemplo FastAPI, SQLAlchemy, Alembic y el conector de MySQL. Con `pip` las instalamos dentro del entorno virtual.

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

5. Levantar la API:

Utilizamos `uvicorn` como servidor ASGI para ejecutar la aplicacion FastAPI en entorno local.

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Al iniciar, la aplicacion ejecuta las migraciones de Alembic para crear o actualizar la estructura de base de datos.

## URLs utiles

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Documentacion

- `docs/README.md`: indice de documentacion escrita.
- `docs/assets/documentacion.html`: mapa vivo del proyecto para consultar como levantarlo, entender la arquitectura y resolver dudas frecuentes.

## Gestion del proyecto

El seguimiento operativo de tareas e issues vive en Linear:

- `https://linear.app/federicobacelar/project/rentalapi-888ed6c0e001`

## Base de datos

La base MySQL se publica localmente en:

```text
localhost:3506
```

Credenciales configuradas para desarrollo:

```text
database: rental_api
user: appuser
password: apppass
```

## Configuracion

La configuracion principal del proyecto se encuentra en estos archivos:

- `.env.example`: plantilla con las variables necesarias para levantar el proyecto.
- `.env`: configuracion local real; no se sube al repo.
- `docker-compose.yml`: define el servicio de MySQL y toma sus valores desde `.env`.
- `app/core/config.py`: centraliza la lectura de variables de entorno para que la aplicacion use una unica configuracion.
- `alembic.ini`: configuracion general de Alembic.
- `alembic/env.py`: conecta Alembic con `app/core/config.py` y los models de la aplicacion.

Si se usa Docker Compose, los valores de `.env.example` ya vienen preparados para trabajar juntos.

Si se usa una base MySQL instalada localmente, se deben modificar los datos de conexion en `.env`.

### Worker de vencimientos

La API incluye un worker simple que marca rentas vencidas.

Comportamiento:

- Al iniciar la API, ejecuta una pasada si `OVERDUE_WORKER_RUN_ON_STARTUP=1`.
- Luego corre una vez por dia en el horario definido por `OVERDUE_WORKER_DAILY_TIME`.
- Por defecto corre a las `00:00`.

Variables disponibles:

```text
OVERDUE_WORKER_ENABLED=1
OVERDUE_WORKER_RUN_ON_STARTUP=1
OVERDUE_WORKER_DAILY_TIME=00:00
```

El worker cambia rentas `OPEN` vencidas a `OVERDUE` y sus detalles `RENTED` a `OVERDUE`. Las copias siguen `RENTED` hasta que se devuelvan.

## Problemas comunes

Si Alembic informa que no encuentra una revision vieja, normalmente significa que el volumen local de MySQL quedo con migraciones de una version anterior del proyecto.

Para reiniciar la base local desde cero:

```powershell
docker compose down -v
docker compose up -d
```

Ese comando elimina los datos locales del contenedor. Usarlo solo cuando no haya informacion importante que conservar.
