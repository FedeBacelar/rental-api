# 3.5 Registrar copia fisica

Trata de registrar una copia fisica de una pelicula o videojuego.

## Endpoint

`POST /inventory/copies`

## Objetivo

Registrar una unidad fisica concreta de un item alquilable.

## Archivos disponibles

- `app/controller/inventory_controller.py`
- `app/dto/inventory/rental_copy_dto.py`
- `app/services/inventory_service.py`
- `app/repositories/inventory/rental_item_repository.py`
- `app/repositories/inventory/rental_copy_repository.py`
- `app/repositories/catalog/rental_copy_status_type_repository.py`

## Contrato esperado

El request debe permitir crear una copia fisica asociada a un item alquilable.

Datos esperados:

- `rental_item_id`
- `copy_number`
- `internal_code`

La response debe devolver la copia creada con sus datos principales.

Datos esperados en response:

- `id`
- `rental_item_id`
- `status_id`
- `copy_number`
- `internal_code`
- `is_active`

## Trabajo a realizar

Implementar el endpoint `POST /inventory/copies`.

El dev debe completar controller, DTO y service para:

- recibir un request de creacion de copia fisica
- validar que el item alquilable exista
- obtener el estado inicial `AVAILABLE`
- validar que no se repita `copy_number` para el mismo item
- validar que no se repita `internal_code`
- crear la copia usando `RentalCopyRepository`
- devolver la copia creada usando un DTO de response

## Descripcion tecnica

Una pelicula o videojuego representa el producto general.

La copia fisica representa la unidad real que se alquila.

Ejemplo:

```text
Item: Matrix
Copias:
- Matrix copia 1
- Matrix copia 2
- Matrix copia 3
```

La renta se hace sobre una copia fisica, no sobre el item general.

> **Concepto importante: item vs copia**
>
> El item alquilable representa el producto general.
>
> Ejemplo: `Matrix`.
>
> La copia fisica representa una unidad concreta de ese item.
>
> Ejemplo: `Matrix copia 1`.
>
> La renta se hace sobre copias fisicas, no sobre el item general.

> **Concepto importante: catalogos por code**
>
> No asumir que el estado disponible tiene id `1`.
>
> Buscar el estado usando el code `AVAILABLE`.
>
> Los ids pueden cambiar segun la base o el seed.

## Notas de implementacion

- El estado inicial normal de una copia nueva deberia ser `AVAILABLE`.
- No asumir ids numericos de catalogo.
- Usar el repository de estados de copia para obtener el estado correspondiente.
- No crear logica de SQL directamente en el controller.
