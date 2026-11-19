import asyncio
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.memory import create_connected_server_and_client_session

from logistics_mcp import server as logistics_server


SERVER_PATH = Path(__file__).resolve().parents[1] / "logistics_mcp.py"


class LogisticsMCPTest(unittest.IsolatedAsyncioTestCase):
    async def test_client_discovers_order_and_policy_tools(self):
        server = StdioServerParameters(
            command=sys.executable,
            args=[str(SERVER_PATH)],
        )

        async with asyncio.timeout(10):
            async with stdio_client(server) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    await session.initialize()
                    tools = (await session.list_tools()).tools

        self.assertCountEqual(
            [tool.name for tool in tools],
            ["get_order", "list_delayed_orders", "update_order_status", "search_policies"],
        )
        policy_tool = next(tool for tool in tools if tool.name == "search_policies")
        self.assertEqual(policy_tool.inputSchema["required"], ["query"])
        self.assertEqual(policy_tool.inputSchema["properties"]["query"]["type"], "string")

    async def test_client_receives_structured_policy_fragments(self):
        fragments = [
            {"source": "failed_deliveries.md", "text": "Registrá el intento.", "score": 0.9}
        ]

        with patch("rag.search.search", return_value=fragments):
            async with create_connected_server_and_client_session(logistics_server) as session:
                result = await session.call_tool("search_policies", {"query": "destinatario ausente"})

        self.assertFalse(result.isError)
        self.assertEqual(result.structuredContent, {"results": fragments})
