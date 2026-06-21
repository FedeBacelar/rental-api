# 1.2 Listar plataformas

Trata de listar las plataformas disponibles para registrar videojuegos.

## Endpoint

`GET /catalogs/platforms`

## Objetivo

Devolver la lista de plataformas disponibles.

## Archivos disponibles

- `app/controller/catalog/catalog_controller.py`
- `app/dto/catalog/platform_dto.py`
- `app/services/catalog/catalog_service.py`
- `app/repositories/catalog/platform_repository.py`

## Trabajo a realizar

Implementar el metodo `list_platforms` dentro de `CatalogService`.

Desde el controller ya existe el endpoint que llama al service.

El dev debe completar el service para:

- crear o usar `PlatformRepository`
- obtener las plataformas activas
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la lista al controller

> **Concepto importante: catalogos**
>
> Las plataformas son datos base para registrar videojuegos.
>
> En esta etapa no se crean desde la API: vienen cargadas por el seed.
>
> Este endpoint solo debe leerlas y devolverlas.

## Descripcion tecnica

<sin definir>
