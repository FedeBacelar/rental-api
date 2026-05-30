# 3.7 Listar copias disponibles

Trata de listar copias fisicas disponibles para alquilar.

## Endpoint

`GET /inventory/copies/available`

## Objetivo

Devolver copias fisicas que se pueden seleccionar al crear una renta.

## Archivos disponibles

- `app/controller/inventory_controller.py`
- `app/dto/inventory/rental_copy_dto.py`
- `app/services/inventory_service.py`
- `app/repositories/inventory/rental_copy_repository.py`
- `app/repositories/catalog/rental_copy_status_type_repository.py`

## Contrato esperado

El request no necesita body.

Puede aceptar filtros opcionales mas adelante, por ejemplo:

- `rental_item_id`

La response debe devolver una lista de copias disponibles.

Datos esperados por copia:

- `id`
- `rental_item_id`
- `status_id`
- `copy_number`
- `internal_code`
- `is_active`

## Trabajo a realizar

Implementar el endpoint `GET /inventory/copies/available`.

El dev debe completar controller, DTO y service para:

- obtener el estado `AVAILABLE`
- consultar copias con ese estado usando `RentalCopyRepository`
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la lista al controller

## Descripcion tecnica

Este endpoint es necesario para crear una renta.

Una renta solo deberia poder seleccionar copias disponibles.

No se deberian ofrecer copias en estados como:

- `RENTED`
- `MAINTENANCE`
- `DAMAGED`
- `LOST`

> **Concepto importante: disponibilidad**
>
> No toda copia existente puede alquilarse.
>
> Para crear una renta solo sirven copias en estado `AVAILABLE`.
>
> Copias `RENTED`, `MAINTENANCE`, `DAMAGED` o `LOST` no deberian aparecer como seleccionables para alquilar.

> **Concepto importante: catalogos por code**
>
> No asumir ids numericos de estados.
>
> Resolver el estado disponible usando el code `AVAILABLE`.

## Notas de implementacion

- No asumir ids numericos de catalogo.
- Usar el code `AVAILABLE` para resolver el estado.
- Este endpoint puede devolver lista vacia si no hay copias disponibles.
