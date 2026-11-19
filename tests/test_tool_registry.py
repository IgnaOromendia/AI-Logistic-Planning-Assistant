import inspect
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from agent.tool_registry import TOOL_FUNCTIONS, TOOL_SCHEMAS
from tools import orders, policies


class ToolRegistryTest(unittest.TestCase):
    def test_registers_logistics_schemas_and_functions(self):
        expected_functions = {
            "get_order": orders.get_order,
            "list_delayed_orders": orders.list_delayed_orders,
            "update_order_status": orders.update_order_status,
            "search_policies": policies.search_policies,
        }

        self.assertEqual(TOOL_FUNCTIONS, expected_functions)
        self.assertCountEqual(
            [schema["name"] for schema in TOOL_SCHEMAS], expected_functions,
        )

    def test_schemas_describe_function_arguments(self):
        json_types = {int: "integer", str: "string"}

        for schema in TOOL_SCHEMAS:
            with self.subTest(tool=schema["name"]):
                parameters = schema["parameters"]
                arguments = inspect.signature(TOOL_FUNCTIONS[schema["name"]]).parameters
                self.assertEqual(parameters["type"], "object")
                self.assertCountEqual(parameters["required"], arguments)
                self.assertEqual(
                    {name: prop["type"] for name, prop in parameters["properties"].items()},
                    {name: json_types[arg.annotation] for name, arg in arguments.items()},
                )

    def test_search_policies_returns_ranked_rag_fragments(self):
        query = "¿Qué hago si el destinatario está ausente?"
        fragments = [
            {"source": "failed_deliveries.md", "text": "Registrá el intento.", "score": 0.9},
            {"source": "deliveries.md", "text": "Contactá al destinatario.", "score": 0.7},
        ]

        with patch("rag.search.search", return_value=fragments) as search:
            result = TOOL_FUNCTIONS["search_policies"](f"  {query}  ")

        search.assert_called_once_with(query)
        self.assertEqual(result, {"results": fragments})

    def test_search_policies_rejects_blank_query_without_searching(self):
        with patch("rag.search.search") as search:
            with self.assertRaisesRegex(ValueError, "consulta"):
                TOOL_FUNCTIONS["search_policies"](" \n ")

        search.assert_not_called()

    def test_search_policies_reports_how_to_build_missing_index(self):
        with TemporaryDirectory() as directory, patch("rag.search.STORAGE", Path(directory)):
            with self.assertRaisesRegex(FileNotFoundError, "python -m rag.index"):
                TOOL_FUNCTIONS["search_policies"]("entregas")
