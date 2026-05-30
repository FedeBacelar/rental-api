# 3.1 Registrar pelicula

Trata de registrar una pelicula como item alquilable.

## Endpoint

`POST /inventory/movies`

## Objetivo

Registrar una pelicula en el inventario para que luego pueda tener copias fisicas y ser alquilada.

## Archivos disponibles

- `app/controller/inventory_controller.py`
- `app/dto/inventory/movie_dto.py`
- `app/services/inventory_service.py`
- `app/repositories/inventory/rental_item_repository.py`
- `app/repositories/inventory/movie_detail_repository.py`
- `app/repositories/catalog/rental_item_type_repository.py`
- `app/repositories/catalog/genre_repository.py`

## Contrato esperado

El request debe permitir cargar datos comunes del item alquilable y datos especificos de pelicula.

Datos comunes:

- `genre_id`
- `title`
- `description`
- `age_rating`
- `base_daily_price`
- `late_fee_per_day`
- `replacement_cost`

Datos especificos de pelicula:

- `duration_minutes`
- `director`
- `original_language`

La response debe devolver la pelicula registrada con sus datos principales.

## Trabajo a realizar

Implementar el endpoint `POST /inventory/movies`.

El dev debe completar controller, DTO y service para:

- recibir un request de creacion de pelicula
- validar que el genero exista
- obtener el tipo de item `MOVIE`
- crear el registro base en `rental_items`
- crear el registro especifico en `movie_details`
- devolver la pelicula creada usando un DTO de response

## Descripcion tecnica

Este endpoint representa un contrato simple para Swagger.

Aunque internamente la base usa dos tablas, el usuario de la API no deberia crear primero un `rental_item` y despues un `movie_detail`.

El service debe coordinar ambas creaciones:

1. Buscar el tipo de item `MOVIE` usando `RentalItemTypeRepository`.
2. Validar el genero usando `GenreRepository`.
3. Crear `RentalItem` usando `RentalItemRepository`.
4. Crear `MovieDetail` usando `MovieDetailRepository`.
5. Devolver una respuesta unificada.

> **Concepto importante: transaccion**
>
> Esta operacion deberia ser transaccional.
>
> Eso significa que todas las acciones internas deben confirmarse juntas:
>
> - crear `rental_items`
> - crear `movie_details`
>
> Si una parte falla, se debe deshacer todo.
>
> Ejemplo: si se crea el `rental_item`, pero falla la creacion de `movie_detail`, no deberia quedar una pelicula incompleta en la base.
>
> Esto evita inconsistencias.
>
> Concepto relacionado: **atomicidad**.

## Notas de implementacion

- El controller recibe la request HTTP.
- El DTO define que datos entran y que datos salen.
- El service contiene la logica del caso de uso.
- Los repositories se usan para consultar o guardar en base de datos.
- No crear logica de SQL directamente en el controller.


