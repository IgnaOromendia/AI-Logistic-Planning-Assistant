### MCP

`logistics-mcp` es un servidor MCP local que permite que un cliente compatible con `stdio` descubra e invoque las herramientas de pedidos y de búsqueda de políticas.

#### Instalación

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

#### Conexión

Configurá el cliente MCP para que lance este comando usando las rutas absolutas de tu copia del repositorio:

```bash
/ruta/al/repo/.venv/bin/python /ruta/al/repo/logistics_mcp.py
```

#### Tools

| Tool | Parámetros | Qué hace |
| --- | --- | --- |
| `get_order` | `order_id` | Consulta un pedido por ID. |
| `list_delayed_orders` | Ninguno | Consulta los pedidos con estado `delayed`. |
| `update_order_status` | `order_id`, `new_status` | Actualiza el pedido en `data/orders.json`. Acepta `in_transit`, `delivered` y `delayed`. |
| `search_policies` | `query` | Busca en las políticas internas y devuelve hasta tres fragmentos ordenados por relevancia. |

#### Verificación

```bash
.venv/bin/python -m unittest discover -s tests -p test_logistics_mcp.py -v
```

La prueba inicia el servidor y verifica que el cliente descubre las herramientas.

### RAG

La empresa logística cuenta con documentación interna que describe cómo actuar frente a distintas situaciones.
Se desarrolló un sistema RAG (Retrieval-Augmented Generation) para que pueda responder preguntas utilizando esa documentación. 

Se implementó a traves de:
- `index`: Lee los documentos, lo fragmenta y genera un embedding.
- `search`: Recibe una pregunta, la convierte en embedding y busca los fragmentos que tengan mayor similitud.
- `generate`: Genera el prompt para el LLM.

Antes de usar `search_policies`, generá el índice desde la raíz del repositorio. Volvé a generarlo cuando cambien los archivos de `policies/`.

```bash
.venv/bin/python -m rag.index
```

Desde un LLM conectado al servidor MCP, llamá a `search_policies` con estos argumentos.

```json
{"query": "¿Qué hago si el destinatario está ausente?"}
```

La respuesta incluye una lista `results`. Cada fragmento contiene el archivo de origen (`source`), el texto de la política (`text`) y el puntaje de similitud (`score`). El LLM puede usar esos fragmentos para responder y citar sus fuentes.
