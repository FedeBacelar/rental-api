# 2.1 Registrar cliente

Trata de crear un cliente nuevo en el sistema.

## Endpoint

`POST /customers`

## Objetivo

Registrar un cliente para poder asociarlo luego a una renta.

## Archivos disponibles

- `app/controller/customer_controller.py`
- `app/dto/customer/customer_dto.py`
- `app/services/customer_service.py`
- `app/repositories/rental/customer_repository.py`
- `app/repositories/catalog/customer_status_type_repository.py`

## Trabajo a realizar

Implementar el metodo `create_customer` dentro de `CustomerService`.

Desde el controller ya existe el endpoint que llama al service.

El dev debe completar el service para:

- validar que no exista otro cliente con el mismo documento
- obtener el estado inicial del cliente
- crear el cliente usando `CustomerRepository`
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver el cliente creado al controller

> **Concepto importante: validacion previa**
>
> Antes de crear un cliente, validar que no exista otro con el mismo documento.
>
> Esto evita duplicados y mantiene la base consistente.
>
> La validacion debe vivir en el service, usando el repository para consultar la base.

> **Concepto importante: estado inicial**
>
> Un cliente nuevo deberia crearse con estado inicial `ACTIVE`.
>
> No asumir que `ACTIVE` tiene un id fijo. Buscar el estado por `code`.

## Descripcion tecnica

<sin definir>
