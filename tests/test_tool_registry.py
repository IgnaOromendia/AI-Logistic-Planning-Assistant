import inspect
import unittest

from agent.tool_registry import TOOL_FUNCTIONS, TOOL_SCHEMAS
from tools import orders


class ToolRegistryTest(unittest.TestCase):
    def test_registers_order_schemas_and_functions(self):
        expected_functions = {
            "get_order": orders.get_order,
            "list_delayed_orders": orders.list_delayed_orders,
            "update_order_status": orders.update_order_status,
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
