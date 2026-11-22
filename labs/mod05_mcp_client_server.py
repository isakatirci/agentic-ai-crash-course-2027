"""
Modül 5 Hands-On Lab: Model Context Protocol (MCP) Mimarisi
- JSON-RPC 2.0 tabanlı standart MCP Tool keşfi (tools/list) ve çağrısı (tools/call)
- MCP Server ve MCP Client soyutlaması (Thread-Safe)
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class MCPToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[[dict[str, Any]], dict[str, Any]]


class SimpleMCPServer:
    """JSON-RPC 2.0 mesajlarını işleyen minimal, Thread-Safe MCP Server."""

    def __init__(self, server_name: str) -> None:
        self.server_name = server_name
        self._lock = threading.RLock()
        self._tools: dict[str, MCPToolSpec] = {}

    def register_tool(self, spec: MCPToolSpec) -> None:
        with self._lock:
            self._tools[spec.name] = spec

    def handle_json_rpc(self, raw_request: str) -> str:
        req = json.loads(raw_request)
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "tools/list":
            with self._lock:
                tools_meta = [
                    {
                        "name": t.name,
                        "description": t.description,
                        "inputSchema": t.input_schema,
                    }
                    for t in self._tools.values()
                ]
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_meta}}, ensure_ascii=False)

        if method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            with self._lock:
                spec = self._tools.get(tool_name)
            if spec is None:
                return json.dumps(
                    {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Tool not found"}},
                    ensure_ascii=False,
                )
            output = spec.handler(arguments)
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": output}, ensure_ascii=False)

        return json.dumps(
            {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}},
            ensure_ascii=False,
        )


def check_inventory(args: dict[str, Any]) -> dict[str, Any]:
    sku = str(args.get("sku", ""))
    stock = {"SKU-LAPTOP-01": 12, "SKU-MOUSE-02": 0}
    return {"sku": sku, "in_stock": stock.get(sku, 0)}


def main() -> None:
    server = SimpleMCPServer("warehouse-mcp")
    server.register_tool(
        MCPToolSpec(
            name="check_inventory",
            description="Depo stok durumunu SKU koduna göre sorgular.",
            input_schema={"type": "object", "properties": {"sku": {"type": "string"}}, "required": ["sku"]},
            handler=check_inventory,
        )
    )

    # 1. MCP Client önce sunucuda hangi Tool'lar var diye keşif yapar (tools/list).
    list_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    print("MCP tools/list Yanıtı:", server.handle_json_rpc(list_req))

    # 2. MCP Client standart formatla Tool çağırır (tools/call).
    call_req = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "check_inventory", "arguments": {"sku": "SKU-LAPTOP-01"}},
        }
    )
    print("MCP tools/call Yanıtı:", server.handle_json_rpc(call_req))


if __name__ == "__main__":
    main()
