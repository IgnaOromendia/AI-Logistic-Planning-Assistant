# Qué hacer cuando una entrega falla

Un intento fallido ocurre cuando el transportista llega al domicilio y no puede entregar. Si la ruta se interrumpe antes de llegar, seguir el [procedimiento de demoras](delays.md).

## Durante la visita

1. Verificar el número, el acceso y las referencias del domicilio. Si hay una condición insegura, retirarse y avisar a Despacho de inmediato.
2. Si el destinatario no responde, llamar al contacto autorizado y esperar hasta cinco minutos desde el primer aviso, siempre que sea seguro permanecer en el lugar. Si el destinatario rechaza el pedido, registrar el motivo que indique.
3. Registrar hora, resultado, gestiones de contacto y cantidad de bultos pendientes. Documentar cualquier daño visible y conservar la custodia de los bultos.
4. Informar a Despacho antes de seguir la ruta. Si aún se puede completar la entrega en la franja original, Despacho mantiene el seguimiento del recorrido. Si se confirma que la franja se incumplirá o esta ya venció, Despacho actualiza el pedido a `delayed` y Atención al Cliente avisa dentro de los 30 minutos siguientes.

## Decisión según el resultado

| Motivo | Acción |
| --- | --- |
| Ausencia o falta de una persona autorizada | Atención al Cliente ofrece una segunda visita, normalmente el siguiente día hábil, y confirma la nueva franja con el destinatario. |
| Domicilio incompleto, incorrecto o sin acceso | Atención al Cliente verifica los datos y confirma una franja antes de que Despacho asigne otro recorrido. |
| Rechazo del pedido | Despacho coordina el retorno a depósito. Si el rechazo se debe a daño o artículos incorrectos, Atención al Cliente abre un [reclamo](claims.md). |
| Riesgo para el transportista | El supervisor revisa la incidencia y define si es viable otra visita o un punto de entrega alternativo. |

## Segundo intento y retorno

Se permiten hasta dos intentos por pedido. Cuando el pedido sale a reparto con la nueva franja confirmada, Despacho actualiza su estado a `in_transit`. Si falla el segundo intento o el destinatario no confirma una reprogramación dentro de dos días hábiles desde el primer contacto, Despacho ordena el retorno. Depósito escanea cada bulto al recibirlo y registra cualquier diferencia. Atención al Cliente comunica el resultado y la alternativa aplicable, como retiro en un punto habilitado o resolución del pedido según el motivo del retorno.

El cierre del intento se registra por separado del estado del pedido. Si el segundo intento tiene éxito, Despacho verifica el comprobante y actualiza el pedido a `delivered` cuando se hayan recibido todos los bultos. Si vuelve a depósito, Despacho registra la recepción y Atención al Cliente registra el resultado comunicado.
