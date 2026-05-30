# 2.3 Listar clientes activos

Trata de listar los clientes activos disponibles para operar.

## Endpoint

`GET /customers/active`

## Objetivo

Devolver la lista de clientes activos.

## Archivos disponibles

- `app/controller/customer_controller.py`
- `app/dto/customer/customer_dto.py`
- `app/services/customer_service.py`
- `app/repositories/rental/customer_repository.py`

## Trabajo a realizar

Implementar el metodo `list_active_customers` dentro de `CustomerService`.

Desde el controller ya existe el endpoint que llama al service.

El dev debe completar el service para:

- usar `CustomerRepository`
- obtener los clientes activos
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la lista al controller

> **Concepto importante: listado operativo**
>
> Este endpoint deberia devolver clientes que pueden seleccionarse para operar.
>
> No es lo mismo listar todos los clientes historicos que listar clientes activos.
>
> Para crear una renta, normalmente se necesita seleccionar un cliente activo.

## Descripcion tecnica

<sin definir>
