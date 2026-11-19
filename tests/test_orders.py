import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from tools import orders


class UpdateOrderStatusTest(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(TemporaryDirectory())
        self.path = Path(directory) / "orders.json"
        self.original = {
            "orders": [
                {"id": 1, "status": "in_transit", "destination": "Córdoba"},
                {"id": 2, "status": "delayed"},
            ],
            "source": "test",
        }
        self.path.write_text(json.dumps(self.original), encoding="utf-8")
        self.enterContext(patch.object(orders, "ORDERS_PATH", self.path))

    def test_persists_status_and_preserves_other_data(self):
        expected_order = {**self.original["orders"][0], "status": "delivered"}

        self.assertEqual(orders.update_order_status(1, "delivered"), expected_order)
        self.assertEqual(orders.get_order(1), expected_order)
        self.assertEqual(
            json.loads(self.path.read_text(encoding="utf-8")),
            {**self.original, "orders": [expected_order, self.original["orders"][1]]},
        )

    def test_unknown_order_leaves_file_unchanged(self):
        original_content = self.path.read_bytes()

        result = orders.update_order_status(999, "delivered")

        self.assertEqual(result, orders.get_order(999))
        self.assertEqual(self.path.read_bytes(), original_content)

    def test_invalid_status_leaves_file_unchanged(self):
        original_content = self.path.read_bytes()

        result = orders.update_order_status(1, "invalid")

        self.assertEqual(result["error"], "STATUS_ERROR")
        self.assertEqual(self.path.read_bytes(), original_content)
