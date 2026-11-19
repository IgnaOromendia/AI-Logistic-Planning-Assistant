# Gestión de pedidos demorados

Despacho gestiona una demora cuando una incidencia confirmada pone en riesgo la franja comprometida o cuando la franja termina con bultos pendientes. Si ya hubo una visita al domicilio y la entrega no pudo concretarse, registrar el intento según el [procedimiento de entregas fallidas](failed_deliveries.md).

## Detección y respuesta

1. Despacho compara la hora estimada de llegada con el fin de la franja. Revisa el último escaneo y confirma con el transportista qué bultos están pendientes y dónde están.
2. Si se confirma la demora, actualiza el pedido a `delayed` y registra la franja original, la causa, la última ubicación conocida, la nueva estimación si está disponible y el responsable del seguimiento.
3. Atención al Cliente avisa al destinatario dentro de los 30 minutos posteriores a la confirmación. Informa qué pedido se demoró, si hay una nueva hora estimada y cuándo enviará la próxima actualización. Si todavía no hay estimación, acuerda con Despacho una hora para el próximo aviso.
4. Despacho revisa el caso cada dos horas durante la operación hasta confirmar una nueva hora o franja. Atención al Cliente comunica cada cambio de compromiso y deja asentados los intentos de contacto.

## Resolución y escalamiento

| Situación | Acción |
| --- | --- |
| El pedido puede entregarse en el mismo recorrido | Despacho actualiza la hora estimada. El pedido sigue en `delayed` hasta que se verifique la entrega completa. |
| El recorrido ya no permite entregar | Despacho propone una nueva franja. El pedido vuelve a `in_transit` cuando la franja se confirma y el pedido sale nuevamente a reparto. |
| Pasaron dos horas sin una ubicación confirmada | Despacho escala al supervisor de operaciones y Atención al Cliente abre un [reclamo por posible extravío](claims.md). |
| La entrega supera en un día hábil el compromiso original | El supervisor revisa la causa y define prioridad de reparto, cambio de transportista o una alternativa que Atención al Cliente pueda ofrecer. |

Despacho cierra el seguimiento al verificar la entrega completa o al transferir el caso a un reclamo que se haga cargo de la resolución. En ambos casos registra la hora, el resultado y el aviso enviado. Los pedidos entregados se actualizan a `delivered` según el [procedimiento general](deliveries.md).
