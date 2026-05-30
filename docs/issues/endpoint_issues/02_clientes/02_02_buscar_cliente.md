# 2.2 Buscar cliente

Trata de buscar un cliente existente para seleccionarlo o consultarlo.

## Endpoint

`GET /customers/search?query={texto}`

## Objetivo

Buscar clientes existentes para seleccionar uno antes de crear una renta.

## Archivos disponibles

- `app/controller/customer_controller.py`
- `app/dto/customer/customer_dto.py`
- `app/services/customer_service.py`
- `app/repositories/rental/customer_repository.py`

## Trabajo a realizar

Implementar el metodo `search_customers` dentro de `CustomerService`.

Desde el controller ya existe el endpoint que llama al service.

El dev debe completar el service para:

- recibir el texto de busqueda
- buscar clientes existentes usando `CustomerRepository`
- agregar metodos nuevos al repository si hace falta
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la lista al controller

> **Concepto importante: query param**
>
> Este endpoint recibe el texto de busqueda por query string.
>
> Ejemplo: `GET /customers/search?query=juan`.
>
> Se usa query param porque no estamos creando ni modificando datos, solo filtrando una consulta.

## Descripcion tecnica

<sin definir>
