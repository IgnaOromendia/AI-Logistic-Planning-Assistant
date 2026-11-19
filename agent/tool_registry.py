import json
from pathlib import Path

from tools.orders import get_order, list_delayed_orders, update_order_status
from tools.policies import search_policies

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"

TOOL_FUNCTIONS = {
    "get_order": get_order,
    "list_delayed_orders": list_delayed_orders,
    "update_order_status": update_order_status,
    "search_policies": search_policies,
}

TOOL_SCHEMAS = [
    json.loads((TOOLS_DIR / f"{name}.json").read_text(encoding="utf-8"))
    for name in TOOL_FUNCTIONS
]
