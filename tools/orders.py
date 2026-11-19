import json
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Lock


ORDERS_PATH = Path(__file__).resolve().parents[1] / "data" / "orders.json"
_orders_write_lock = Lock()


def _load_orders_document() -> dict:
    with ORDERS_PATH.open(encoding="utf-8") as orders_file:
        return json.load(orders_file)


def _save_orders_document(document: dict) -> None:
    with TemporaryDirectory(dir=ORDERS_PATH.parent) as directory:
        temporary_path = Path(directory) / ORDERS_PATH.name
        with temporary_path.open("w", encoding="utf-8") as orders_file:
            json.dump(document, orders_file, ensure_ascii=False, indent=4)
            orders_file.write("\n")
        temporary_path.replace(ORDERS_PATH)


def get_order(order_id: int) -> dict:
    orders = _load_orders_document()["orders"]

    for order in orders:
        if order["id"] == order_id:
            return order

    return {
        "error": "ORDER_NOT_FOUND",
        "message": f"No existe el pedido {order_id}",
    }

def list_delayed_orders() -> dict:
    orders = _load_orders_document()["orders"]

    response = {}

    for order in orders:
        if order["status"] == "delayed":
            response.update(order)

    return response

def update_order_status(order_id: int, new_status: str) -> dict:
    if new_status not in ("in_transit", "delivered", "delayed"):
        return {
            "error": "STATUS_ERROR",
            "message": f"El status {new_status} no forma parte del sistema",
        }

    with _orders_write_lock:
        document = _load_orders_document()
        for order in document["orders"]:
            if order["id"] == order_id:
                order["status"] = new_status
                _save_orders_document(document)
                return order

    return {
        "error": "ORDER_NOT_FOUND",
        "message": f"No existe el pedido {order_id}",
    }
