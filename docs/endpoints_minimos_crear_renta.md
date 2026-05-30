# Objetivo: Rentar y devolver desde Swagger

Escenario inicial:

- Base de datos vacia.
- Catalogos ya sedeados.
- Sin clientes cargados.
- Sin peliculas cargadas.
- Sin videojuegos cargados.
- Sin copias fisicas cargadas.
- Sin rentas cargadas.

## 1. Consultar datos base

Endpoints:

- 1.1 Listar generos.
- 1.2 Listar plataformas.
- 1.3 Listar estados de copia.
- 1.4 Listar estados de cliente.

Uso:

- Obtener ids/codes necesarios para completar requests desde Swagger.
- No crear catalogos manualmente.

## 2. Clientes

Endpoints:

- 2.1 Registrar cliente.
- 2.2 Buscar cliente.
- 2.3 Listar clientes activos.

Uso:

- Crear un cliente.
- Buscarlo para obtener el `customer_id`.
- Usarlo al crear la renta.

## 3. Inventario

Endpoints:

- 3.1 Registrar pelicula.
- 3.2 Registrar videojuego.
- 3.3 Listar items alquilables.
- 3.4 Consultar item alquilable.
- 3.5 Registrar copia fisica.
- 3.6 Listar copias por item.
- 3.7 Listar copias disponibles.
- 3.8 Consultar copia fisica.

Uso:

- Registrar una pelicula o videojuego en un solo request.
- Crear copias fisicas de ese item.
- Obtener el `rental_copy_id` de una copia disponible.

Nota tecnica:

- El endpoint `registrar pelicula` puede crear internamente `rental_items` y `movie_details`.
- El endpoint `registrar videojuego` puede crear internamente `rental_items` y `videogame_details`.
- El contrato HTTP deberia ser simple para quien usa Swagger.

## 4. Rentas

Endpoints:

- 4.1 Crear renta.
- 4.2 Consultar renta.
- 4.3 Listar rentas por cliente.
- 4.4 Consultar detalles de renta.
- 4.5 Devolver item.

Uso:

- Crear una renta seleccionando cliente y copias disponibles.
- Consultar la renta creada.
- Obtener el `rental_detail_id`.
- Devolver el item alquilado.

## 5. Flujo minimo completo

```text
1. Listar generos.
2. Listar plataformas si se va a crear un videojuego.
3. Registrar cliente.
4. Buscar cliente o listar clientes activos.
5. Registrar pelicula o registrar videojuego.
6. Registrar copia fisica para ese item.
7. Listar copias disponibles.
8. Crear renta con customer_id y rental_copy_id.
9. Consultar renta.
10. Consultar detalles de renta.
11. Devolver item usando rental_detail_id.
12. Consultar renta nuevamente.
13. Consultar copia fisica nuevamente.
```

## Contratos indispensables

Catalogos:

- Listar generos.
- Listar plataformas.
- Listar estados de copia.
- Listar estados de cliente.

Clientes:

- Registrar cliente.
- Buscar cliente.
- Listar clientes activos.

Inventario:

- Registrar pelicula.
- Registrar videojuego.
- Listar items alquilables.
- Consultar item alquilable.
- Registrar copia fisica.
- Listar copias por item.
- Listar copias disponibles.
- Consultar copia fisica.

Rentas:

- Crear renta.
- Consultar renta.
- Listar rentas por cliente.
- Consultar detalles de renta.
- Devolver item.
