# 3.3 Listar items alquilables

Trata de listar peliculas y videojuegos cargados en el inventario.

## Endpoint

`GET /inventory/items`

## Objetivo

Devolver los items alquilables cargados en el sistema.

## Archivos disponibles

- `app/controller/inventory/inventory_controller.py`
- `app/dto/inventory/rental_item_dto.py`
- `app/services/inventory/inventory_service.py`
- `app/repositories/inventory/rental_item_repository.py`

## Contrato esperado

El request no necesita body.

La response debe devolver una lista de items alquilables con sus datos principales.

Datos esperados por item:

- `id`
- `item_type_id`
- `genre_id`
- `title`
- `description`
- `age_rating`
- `base_daily_price`
- `late_fee_per_day`
- `replacement_cost`
- `is_active`

## Trabajo a realizar

Implementar el endpoint `GET /inventory/items`.

El dev debe completar controller, DTO y service para:

- llamar al service desde el controller
- obtener los items activos usando `RentalItemRepository`
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la lista al controller

## Descripcion tecnica

Este endpoint sirve para consultar el inventario general antes de seleccionar una copia fisica.

La lista puede incluir peliculas y videojuegos.

No hace falta devolver todos los datos especificos de pelicula/videojuego en este listado. Puede ser una respuesta resumida.

> **Concepto importante: listado resumido**
>
> Un listado no siempre necesita devolver todo el detalle de cada registro.
>
> Para una pantalla o consulta general, puede alcanzar con mostrar datos principales del item.
>
> El detalle completo queda para `GET /inventory/items/{item_id}`.

## Notas de implementacion

- Mantener el controller simple.
- La consulta de base debe vivir en repository.
- La transformacion a DTO debe resolverse en service.
