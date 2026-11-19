# Procedimiento general de entregas

Procedimiento ficticio para operaciones de última milla. Los horarios se expresan en la hora local del destino. Los días hábiles operativos van de lunes a viernes, excepto feriados del centro de distribución.

## Responsables

| Equipo | Responsabilidad |
| --- | --- |
| Depósito | Preparar, etiquetar y entregar los bultos al transportista. |
| Despacho | Planificar la ruta, confirmar la franja y seguir el recorrido. |
| Transportista | Custodiar los bultos y registrar el resultado de cada visita. |
| Atención al Cliente | Comunicar cambios, coordinar reprogramaciones y gestionar reclamos. |

## Flujo del pedido

1. **Preparar.** Depósito verifica el ID del pedido, el contenido, la cantidad de bultos y el estado del embalaje. Despacho confirma domicilio, referencias de acceso y contacto del destinatario. Cualquier diferencia se resuelve antes de cargar el pedido.
2. **Programar.** Despacho asigna ruta y transportista, y comunica fecha, franja horaria de cuatro horas e ID del pedido por el canal registrado.
3. **Despachar.** El transportista escanea los bultos al recibirlos. Despacho confirma la salida y actualiza el pedido a `in_transit`.
4. **Entregar.** El transportista verifica el código de recepción o el nombre de la persona autorizada. Registra hora, cantidad de bultos entregados y comprobante de recepción. Puede dejar el pedido en un lugar seguro únicamente cuando el destinatario lo autorizó por escrito y el punto es accesible y seguro. En ese caso, registra una foto del bulto en el lugar autorizado sin incluir personas ni documentos.
5. **Cerrar.** Despacho verifica que el comprobante corresponda al pedido y que se hayan entregado todos sus bultos. Actualiza el estado a `delivered` y envía la confirmación. Si se entregó solo una parte, deriva el faltante a Atención al Cliente y conserva el detalle de los bultos recibidos.

## Estados y excepciones

| Estado del pedido | Cuándo usarlo |
| --- | --- |
| `in_transit` | El pedido salió a reparto, incluida una salida con una nueva franja confirmada. |
| `delayed` | La franja comprometida corre riesgo confirmado de incumplimiento o ya venció con bultos pendientes. |
| `delivered` | Se verificó el comprobante de recepción de todos los bultos. |

- Si la franja corre riesgo de incumplirse, seguir el [procedimiento de demoras](delays.md).
- Si el transportista llegó al domicilio y no pudo entregar, seguir el [procedimiento de entregas fallidas](failed_deliveries.md).
- Si el destinatario informa un faltante, daño o desacuerdo con el comprobante, abrir un [reclamo](claims.md).
- Si el destinatario quiere devolver un pedido recibido, aplicar la [política de devoluciones](returns.md).

Las visitas fallidas, reprogramaciones, devoluciones y reclamos se documentan en el registro operativo con el ID del pedido y el historial de eventos. Para consultar o actualizar el estado del pedido se usan las herramientas descritas en el [README](../README.md).
