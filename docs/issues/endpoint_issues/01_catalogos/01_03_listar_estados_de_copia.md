# 1.3 Listar estados de copia

Trata de listar los estados posibles de una copia fisica.

## Endpoint

`GET /catalogs/rental-copy-statuses`

## Objetivo

Devolver la lista de estados de copia disponibles.

## Archivos disponibles

- `app/controller/catalog/catalog_controller.py`
- `app/dto/catalog/rental_copy_status_dto.py`
- `app/services/catalog/catalog_service.py`
- `app/repositories/inventory/rental_copy_status_type_repository.py`

## Trabajo a realizar

Implementar el metodo `list_rental_copy_statuses` dentro de `CatalogService`.

Desde el controller ya existe el endpoint que llama al service.

El dev debe completar el service para:

- crear o usar `RentalCopyStatusTypeRepository`
- obtener los estados de copia activos
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la lista al controller

> **Concepto importante: estados como catalogo**
>
> Los estados de copia no deberian escribirse a mano como texto libre.
>
> La base tiene un catalogo con valores conocidos como `AVAILABLE`, `RENTED`, `MAINTENANCE`, `DAMAGED` y `LOST`.
>
> Este endpoint ayuda a conocer esos valores desde Swagger.

## Descripcion tecnica

<sin definir>
