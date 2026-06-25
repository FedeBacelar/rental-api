# Reglas de estados y worker de vencimientos

Este documento define las reglas minimas del flujo de rentas para mantener el comportamiento consistente entre endpoints y jobs.

## Estados de copias fisicas

Estados principales:

- `AVAILABLE`: la copia esta disponible para alquilar.
- `RENTED`: la copia esta alquilada y todavia no fue devuelta.
- `MAINTENANCE`: la copia no se puede alquilar temporalmente.
- `DAMAGED`: la copia volvio danada o no esta apta para alquilar.
- `LOST`: la copia fue declarada perdida.

Transiciones esperadas para el MVP:

- `AVAILABLE` -> `RENTED`: al crear una renta.
- `RENTED` -> `AVAILABLE`: al devolver normalmente.
- `RENTED` -> `DAMAGED`: al devolver danada.
- `RENTED` -> `LOST`: al declarar perdida.

El worker de vencimientos no cambia estados de copias. Una copia vencida sigue estando `RENTED` hasta que se devuelva o se declare perdida/danada.

## Estados de rentas

Estados principales:

- `OPEN`: renta activa dentro del plazo esperado.
- `OVERDUE`: renta activa con fecha esperada de devolucion vencida.
- `PARTIALLY_RETURNED`: renta con algunas copias devueltas y otras pendientes.
- `PARTIALLY_OVERDUE`: renta parcialmente devuelta con items pendientes vencidos.
- `CLOSED`: renta completamente resuelta.
- `CANCELLED`: renta cancelada.

Transiciones esperadas para el MVP:

- `OPEN` -> `OVERDUE`: cuando paso la fecha esperada de devolucion.
- `OPEN` -> `PARTIALLY_RETURNED`: cuando se devuelve parte de una renta con multiples copias.
- `OPEN` -> `CLOSED`: cuando se devuelven todas las copias a tiempo.
- `OVERDUE` -> `CLOSED`: cuando se resuelve una renta vencida.
- `OVERDUE` -> `PARTIALLY_RETURNED`: cuando se devuelve parte de una renta vencida.

## Estados de detalles de renta

Estados principales:

- `RENTED`: detalle activo dentro del plazo esperado.
- `OVERDUE`: detalle activo vencido.
- `RETURNED`: detalle devuelto.
- `LOST`: detalle declarado perdido.
- `CANCELLED`: detalle cancelado.

Transiciones esperadas para el MVP:

- `RENTED` -> `OVERDUE`: cuando paso la fecha esperada de devolucion.
- `RENTED` -> `RETURNED`: devolucion normal dentro del plazo.
- `OVERDUE` -> `RETURNED`: devolucion tardia con mora.
- `RENTED` -> `LOST`: perdida dentro del plazo.
- `OVERDUE` -> `LOST`: perdida luego del vencimiento.

## Worker de vencimientos

El worker de vencimientos mantiene sincronizados los estados cuando pasa la fecha esperada de devolucion.

Regla aplicada:

- Busca rentas `OPEN` con `expected_return_date < hoy`.
- Cambia esas rentas a `OVERDUE`.
- Busca rentas `PARTIALLY_RETURNED` con `expected_return_date < hoy`.
- Cambia esas rentas a `PARTIALLY_OVERDUE`.
- Cambia sus detalles `RENTED` a `OVERDUE`.
- No modifica las copias fisicas: siguen `RENTED`.
- No calcula importes ni mora. Los importes finales se calculan al devolver el item.

El worker corre:

- Una vez al iniciar la API, si esta habilitado.
- Una vez por dia en el horario configurado.

Variables de entorno:

```text
OVERDUE_WORKER_ENABLED=1
OVERDUE_WORKER_RUN_ON_STARTUP=1
OVERDUE_WORKER_DAILY_TIME=00:00
```

Detalle:

- `OVERDUE_WORKER_ENABLED`: habilita o deshabilita el worker.
- `OVERDUE_WORKER_RUN_ON_STARTUP`: ejecuta una pasada al iniciar la API.
- `OVERDUE_WORKER_DAILY_TIME`: horario diario en formato `HH:MM`.

Para desarrollo local, el valor por defecto es correr al iniciar y todos los dias a las `00:00`.
