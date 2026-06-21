# 3.8 Consultar copia fisica

Trata de consultar una copia fisica existente.

## Endpoint

`GET /inventory/copies/{copy_id}`

## Objetivo

Consultar una copia fisica puntual.

## Archivos disponibles

- `app/controller/inventory/inventory_controller.py`
- `app/dto/inventory/rental_copy_dto.py`
- `app/services/inventory/inventory_service.py`
- `app/repositories/inventory/rental_copy_repository.py`

## Contrato esperado

El request recibe el `copy_id` por path.

La response debe devolver los datos principales de la copia.

Datos esperados:

- `id`
- `rental_item_id`
- `status_id`
- `copy_number`
- `internal_code`
- `is_active`

## Trabajo a realizar

Implementar el endpoint `GET /inventory/copies/{copy_id}`.

El dev debe completar controller, DTO y service para:

- recibir `copy_id` desde el path
- buscar la copia usando `RentalCopyRepository`
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la copia al controller

## Descripcion tecnica

Este endpoint sirve para verificar el estado de una copia puntual.

Es util despues de crear una copia, despues de crear una renta y despues de devolver un item.

Si la copia no existe, el endpoint deberia responder un error adecuado.

> **Concepto importante: verificar estado**
>
> Consultar una copia permite confirmar en que estado quedo despues de una operacion.
>
> Ejemplo: despues de crear una renta, la copia deberia quedar `RENTED`.
>
> Ejemplo: despues de devolver un item, la copia podria quedar `AVAILABLE`, `MAINTENANCE` o `DAMAGED`.

## Notas de implementacion

- No consultar la base directamente desde el controller.
- Resolver el caso de copia inexistente de forma clara.
- Mantener el DTO de salida consistente con los listados de copias.
