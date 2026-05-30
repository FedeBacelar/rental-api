# 1 - Objetivo

`RentalApi` es una API para gestionar el alquiler de peliculas y videojuegos.

El sistema permite administrar catalogos, inventario fisico, clientes, rentas y devoluciones. Tambien incluye una base de seguridad con usuarios, roles y permisos para futuras restricciones de acceso.

## Alcance principal

- Registrar peliculas y videojuegos alquilables.
- Registrar copias fisicas de cada item.
- Consultar copias disponibles para alquilar.
- Registrar clientes.
- Crear rentas con una o varias copias.
- Devolver items alquilados de forma parcial o completa.
- Calcular importes base, recargos por demora y costos de reposicion.

## Fuera de alcance por ahora

- Pagos reales.
- Facturacion.
- Reembolsos.
- Auditoria avanzada.
- Integracion con servicios externos.

## Flujo minimo esperado

1. Consultar catalogos necesarios.
2. Registrar un cliente.
3. Registrar una pelicula o videojuego.
4. Registrar una copia fisica.
5. Crear una renta.
6. Consultar la renta y sus detalles.
7. Devolver una copia alquilada.
