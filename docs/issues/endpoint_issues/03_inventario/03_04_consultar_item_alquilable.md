# 3.4 Consultar item alquilable

Trata de consultar el detalle de un item alquilable existente.

## Endpoint

`GET /inventory/items/{item_id}`

## Objetivo

Consultar un item alquilable puntual.

## Archivos disponibles

- `app/controller/inventory_controller.py`
- `app/dto/inventory/rental_item_dto.py`
- `app/dto/inventory/movie_dto.py`
- `app/dto/inventory/videogame_dto.py`
- `app/services/inventory_service.py`
- `app/repositories/inventory/rental_item_repository.py`
- `app/repositories/inventory/movie_detail_repository.py`
- `app/repositories/inventory/videogame_detail_repository.py`

## Contrato esperado

El request recibe el `item_id` por path.

La response debe devolver el item con sus datos principales.

Si el item es una pelicula, deberia incluir datos de pelicula.

Si el item es un videojuego, deberia incluir datos de videojuego.

## Trabajo a realizar

Implementar el endpoint `GET /inventory/items/{item_id}`.

El dev debe completar controller, DTO y service para:

- recibir `item_id` desde el path
- buscar el item usando `RentalItemRepository`
- detectar si corresponde consultar `movie_details` o `videogame_details`
- devolver una respuesta clara para Swagger

## Descripcion tecnica

Este endpoint permite ver el detalle de un item antes de crear copias o antes de alquilarlo.

El service puede coordinar la consulta del item base y su detalle especifico.

Si el item no existe, el endpoint deberia responder un error adecuado.

> **Concepto importante: path param**
>
> Este endpoint recibe el identificador del item en la ruta.
>
> Ejemplo: `GET /inventory/items/10`.
>
> Se usa path param porque se esta consultando un recurso puntual.

> **Concepto importante: item base y detalle especifico**
>
> `rental_items` guarda los datos comunes.
>
> `movie_details` y `videogame_details` guardan los datos particulares segun el tipo.
>
> El service debe decidir que detalle consultar segun el tipo de item.

## Notas de implementacion

- No hacer consultas directas desde el controller.
- Centralizar la decision pelicula/videojuego en el service.
- Mantener el DTO de respuesta simple y entendible.
