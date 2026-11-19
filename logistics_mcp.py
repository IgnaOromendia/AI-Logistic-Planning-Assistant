from mcp.server.fastmcp import FastMCP

from agent.tool_registry import TOOL_FUNCTIONS, TOOL_SCHEMAS

server = FastMCP("logistics-mcp")

for schema in TOOL_SCHEMAS:
    server.add_tool(
        TOOL_FUNCTIONS[schema["name"]],
        description=schema["description"],
    )

if __name__ == "__main__":
    server.run(transport="stdio")