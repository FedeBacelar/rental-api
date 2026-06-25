# 4.2 Consultar renta

Trata de consultar una renta creada.

Descripcion tecnica:

Metodo y ruta: GET /rentals/{rental_id}
Codigo de exito: 200 OK

Path params:
- rental_id: int

Response (RentalResponse, mismo contrato que devuelve crear renta en 4.1):
- id: int
- customer_id: int
- status_id: int
- status_code: str          (texto del estado: OPEN / PARTIALLY_RETURNED / OVERDUE /
                             PARTIALLY_OVERDUE / CLOSED / CANCELLED)
- rental_date: date
- expected_return_date: date
- total_amount: float

Validaciones:
- La renta debe existir (404 "La renta no existe" si no).

Logica:
- Buscar la renta por id y devolverla. Solo lectura, no cambia ningun estado.
- status_code se obtiene del rental_status_type asociado a status_id (campo code).

Decisiones de analisis:
- Se devuelve solo la cabecera de la renta. El desglose copia por copia va por
  el 4.4 (GET /rentals/{rental_id}/details), no embebido.
- Se agrego status_code (texto) ademas de status_id, para que en Swagger se entienda
  el estado sin tener que mapear el numero. Esto impacta tambien al RentalResponse de 4.1.
- "Fecha de creacion" se interpreta como rental_date (fecha de la renta). La tabla
  tiene ademas created_at (timestamp de insercion), no incluido por ahora.

Nota: total_amount queda en 0 hasta que se devuelven items (ver 4.5).