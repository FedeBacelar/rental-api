# 1.1 Listar generos

Trata de listar los generos disponibles para registrar peliculas o videojuegos.

## Endpoint

`GET /catalogs/genres`

## Objetivo

Devolver la lista de generos disponibles.

## Archivos disponibles

- `app/controller/catalog/catalog_controller.py`
- `app/dto/catalog/genre_dto.py`
- `app/services/catalog/catalog_service.py`
- `app/repositories/catalog/genre_repository.py`

## Trabajo a realizar

Implementar el metodo `list_genres` dentro de `CatalogService`.

Desde el controller ya existe el endpoint que llama al service.

El dev debe completar el service para:

- crear o usar `GenreRepository`
- obtener los generos activos
- convertir la respuesta al DTO correspondiente con la estrategia que prefiera
- devolver la lista al controller

> **Concepto importante: catalogos**
>
> Los generos son datos base del sistema.
>
> En esta etapa no se crean desde la API: vienen cargados por el seed.
>
> Este endpoint solo debe leerlos y devolverlos.

## Descripcion tecnica

<sin definir>
