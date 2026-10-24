from functools import lru_cache
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from app.config import DATA_DIR

"""
Подключение к MCP-серверу (Model Context Protocol).
Протокол, по которому агент вызывает инструменты внешних серверов.
"""

@lru_cache(maxsize=1)
def get_mcp_client() -> MultiServerMCPClient:
    return MultiServerMCPClient({
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(DATA_DIR)],
            "transport": "stdio",
        }
    })

async def get_mcp_tools() -> list[BaseTool]:
    return await get_mcp_client().get_tools()

async def read_security_patterns_via_mcp() -> str:
    tools = await get_mcp_tools()
    read_tool = next((t for t in tools if t.name == "read_file"), None)
    if read_tool is None:
        raise RuntimeError(f"Нет read_file. Доступные: {[t.name for t in tools]}")
    result = await read_tool.ainvoke({"path": str(DATA_DIR / "security_patterns.txt")})
    if isinstance(result, list):
        return "\n".join(
            item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in result
        )
    return str(result)