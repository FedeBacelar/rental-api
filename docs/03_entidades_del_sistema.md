# 3 - Entidades del sistema

El dominio se divide en catalogos, inventario, rentas y seguridad.

## Catalogos

Los catalogos guardan valores de referencia usados por el sistema.

- `rental_item_types`: tipos de item alquilable (`MOVIE`, `VIDEOGAME`).
- `genres`: generos de peliculas o videojuegos.
- `platforms`: plataformas para videojuegos.
- `rental_copy_status_types`: estados de copias fisicas.
- `customer_status_types`: estados de clientes.
- `rental_status_types`: estados de rentas.
- `rental_detail_status_types`: estados de cada item alquilado.
- `user_status_types`: estados de usuarios.

## Inventario

- `rental_items`: representa una pelicula o videojuego alquilable.
- `movie_details`: datos especificos de una pelicula.
- `videogame_details`: datos especificos de un videojuego.
- `rental_copies`: copias fisicas disponibles, alquiladas, perdidas o danadas.

La entidad central del inventario es `rental_items`. Las tablas `movie_details` y `videogame_details` completan informacion segun el tipo de item.

## Clientes

- `customers`: personas que pueden realizar rentas.

El cliente tiene datos basicos como nombre, documento, email, telefono, direccion y estado. El documento es unico.

## Rentas

- `rentals`: cabecera de una operacion de alquiler.
- `rental_details`: detalle de cada copia fisica incluida en una renta.

Una renta puede tener varios detalles. Cada detalle guarda snapshot de precios al momento de alquilar, dias alquilados, demoras, recargos y estado operativo.

## Seguridad

- `users`: usuarios que operan el sistema.
- `roles`: roles disponibles.
- `permissions`: permisos disponibles.
- `role_permissions`: relacion entre roles y permisos.

La seguridad queda preparada para crecer. Los permisos concretos se definen cuando el sistema necesite restringir acciones reales.

## Decisiones de dominio

- Una renta puede devolverse parcialmente.
- El detalle de renta es la verdad operativa fina.
- Una renta se cierra cuando todos sus detalles quedan resueltos.
- Un detalle queda resuelto cuando esta devuelto, perdido o cancelado.
- Los precios se copian al detalle para conservar el valor usado en la operacion.
