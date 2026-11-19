import asyncio
import sys
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = Path(__file__).resolve().parents[1] / "logistics_mcp.py"


class LogisticsMCPTest(unittest.IsolatedAsyncioTestCase):
    async def test_client_discovers_all_three_order_tools(self):
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
            ["get_order", "list_delayed_orders", "update_order_status"],
        )
