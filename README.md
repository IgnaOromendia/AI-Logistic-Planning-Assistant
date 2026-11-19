### MCP

`logistics-mcp` es un servidor local del Model Context Protocol (MCP) que expone las herramientas de pedidos a clientes compatibles mediante `stdio`.

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

#### Herramientas

| Herramienta | Parámetros | Qué hace |
| --- | --- | --- |
| `get_order` | `order_id` | Consulta un pedido por ID. |
| `list_delayed_orders` | Ninguno | Consulta los pedidos con estado `delayed`. |
| `update_order_status` | `order_id`, `new_status` | Actualiza el pedido en `data/orders.json`. Acepta `in_transit`, `delivered` y `delayed`. |

#### Verificación

```bash
.venv/bin/python -m unittest discover -s tests -p test_logistics_mcp.py -v
```

La prueba inicia el servidor y verifica que el cliente descubre las tres herramientas.