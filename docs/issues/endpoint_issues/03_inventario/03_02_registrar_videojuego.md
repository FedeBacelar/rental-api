# 3.2 Registrar videojuego

Trata de registrar un videojuego como item alquilable.

## Endpoint

`POST /inventory/videogames`

## Objetivo

Registrar un videojuego en el inventario para que luego pueda tener copias fisicas y ser alquilado.

## Archivos disponibles

- `app/controller/inventory/inventory_controller.py`
- `app/dto/inventory/videogame_dto.py`
- `app/services/inventory/inventory_service.py`
- `app/repositories/inventory/rental_item_repository.py`
- `app/repositories/inventory/videogame_detail_repository.py`
- `app/repositories/inventory/rental_item_type_repository.py`
- `app/repositories/catalog/genre_repository.py`
- `app/repositories/catalog/platform_repository.py`

## Contrato esperado

El request debe permitir cargar datos comunes del item alquilable y datos especificos de videojuego.

Datos comunes:

- `genre_id`
- `title`
- `description`
- `age_rating`
- `base_daily_price`
- `late_fee_per_day`
- `replacement_cost`

Datos especificos de videojuego:

- `platform_id`
- `publisher`
- `multiplayer`

La response debe devolver el videojuego registrado con sus datos principales.

## Trabajo a realizar

Implementar el endpoint `POST /inventory/videogames`.

El dev debe completar controller, DTO y service para:

- recibir un request de creacion de videojuego
- validar que el genero exista
- validar que la plataforma exista
- obtener el tipo de item `VIDEOGAME`
- crear el registro base en `rental_items`
- crear el registro especifico en `videogame_details`
- devolver el videojuego creado usando un DTO de response

## Descripcion tecnica

Este endpoint representa un contrato simple para Swagger.

Aunque internamente la base usa dos tablas, el usuario de la API no deberia crear primero un `rental_item` y despues un `videogame_detail`.

El service debe coordinar ambas creaciones:

1. Buscar el tipo de item `VIDEOGAME` usando `RentalItemTypeRepository`.
2. Validar el genero usando `GenreRepository`.
3. Validar la plataforma usando `PlatformRepository`.
4. Crear `RentalItem` usando `RentalItemRepository`.
5. Crear `VideogameDetail` usando `VideogameDetailRepository`.
6. Devolver una respuesta unificada.

> **Concepto importante: transaccion**
>
> Esta operacion deberia ser transaccional.
>
> Eso significa que todas las acciones internas deben confirmarse juntas:
>
> - crear `rental_items`
> - crear `videogame_details`
>
> Si una parte falla, se debe deshacer todo.
>
> Ejemplo: si se crea el `rental_item`, pero falla la creacion de `videogame_detail`, no deberia quedar un videojuego incompleto en la base.
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
