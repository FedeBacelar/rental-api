# 1.4 Listar estados de cliente

Trata de listar los estados posibles de un cliente.

## Endpoint

`GET /catalogs/customer-statuses`

## Objetivo

Devolver la lista de estados de cliente disponibles.

## Archivos disponibles

- `app/controller/catalog/catalog_controller.py`
- `app/dto/catalog/customer_status_dto.py`
- `app/services/catalog/catalog_service.py`
- `app/repositories/customer/customer_status_type_repository.py`

## Trabajo a realizar

Implementar el metodo `list_customer_statuses` dentro de `CatalogService`.

Desde el controller ya existe el endpoint que llama al service.

El dev debe completar el service para:

- crear o usar `CustomerStatusTypeRepository`
- obtener los estados de cliente activos
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la lista al controller

> **Concepto importante: estados como catalogo**
>
> Los estados de cliente no deberian escribirse a mano como texto libre.
>
> La base tiene un catalogo con valores conocidos como `ACTIVE`, `INACTIVE` y `BLOCKED`.
>
> Este endpoint ayuda a conocer esos valores desde Swagger.

## Descripcion tecnica

<sin definir>
