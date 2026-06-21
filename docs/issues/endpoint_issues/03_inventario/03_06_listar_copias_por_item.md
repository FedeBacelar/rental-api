# 3.6 Listar copias por item

Trata de listar las copias fisicas asociadas a un item alquilable.

## Endpoint

`GET /inventory/items/{item_id}/copies`

## Objetivo

Devolver las copias fisicas registradas para un item alquilable.

## Archivos disponibles

- `app/controller/inventory/inventory_controller.py`
- `app/dto/inventory/rental_copy_dto.py`
- `app/services/inventory/inventory_service.py`
- `app/repositories/inventory/rental_item_repository.py`
- `app/repositories/inventory/rental_copy_repository.py`

## Contrato esperado

El request recibe el `item_id` por path.

La response debe devolver una lista de copias fisicas asociadas al item.

Datos esperados por copia:

- `id`
- `rental_item_id`
- `status_id`
- `copy_number`
- `internal_code`
- `is_active`

## Trabajo a realizar

Implementar el endpoint `GET /inventory/items/{item_id}/copies`.

El dev debe completar controller, DTO y service para:

- recibir `item_id` desde el path
- validar que el item exista
- consultar las copias usando `RentalCopyRepository`
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la lista al controller

## Descripcion tecnica

Este endpoint permite ver cuantas copias tiene un item y en que estado se encuentran.

Es util para revisar inventario y para entender por que una copia puede o no estar disponible para alquilar.

> **Concepto importante: relacion uno a muchos**
>
> Un item alquilable puede tener muchas copias fisicas.
>
> Ejemplo: una pelicula puede tener copia 1, copia 2 y copia 3.
>
> Por eso este endpoint lista varias copias a partir de un solo `item_id`.

## Notas de implementacion

- No filtrar solo disponibles en este endpoint.
- Este endpoint debe listar todas las copias del item, activas o segun la regla que se defina.
- La consulta especifica de disponibles vive en el issue `3.7`.
