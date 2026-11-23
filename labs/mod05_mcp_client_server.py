"""
Modül 5 Hands-On Lab: Model Context Protocol (MCP) Mimarisi
- JSON-RPC 2.0 tabanlı standart MCP Tool keşfi (tools/list) ve çağrısı (tools/call)
- MCP Server ve MCP Client soyutlaması (Thread-Safe)
"""

from __future__ import annotations

import json  # JSON-RPC 2.0 isteklerini okuyup yanıt üretmek için.
import threading
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class MCPToolSpec:
    """MCP Server üzerinde dış dünyaya açılan tek bir aracın standart tanımı."""

    name: str                                         # Aracın benzersiz adı
    description: str                                  # LLM'in okuyacağı görev açıklaması
    input_schema: dict[str, Any]                      # Aracın beklediği parametrelerin JSON şeması
    handler: Callable[[dict[str, Any]], dict[str, Any]]  # Gerçek işi yapan Python fonksiyonu


class SimpleMCPServer:
    """JSON-RPC 2.0 mesajlarını işleyen minimal, Thread-Safe MCP Server."""

    def __init__(self, server_name: str) -> None:
        self.server_name = server_name
        self._lock = threading.RLock()  # Eşzamanlı araç kaydı ve okumasını korur.
        self._tools: dict[str, MCPToolSpec] = {}

    def register_tool(self, spec: MCPToolSpec) -> None:
        """Sunucuya yeni bir MCP aracı (Tool) kaydeder."""
        with self._lock:
            self._tools[spec.name] = spec

    def handle_json_rpc(self, raw_request: str) -> str:
        """Gelen standart JSON-RPC 2.0 mesajını okur, ilgili MCP metodunu çalıştırır."""
        # 1. İstemciden (MCP Client) gelen JSON metnini Python sözlüğüne çeviriyoruz.
        req = json.loads(raw_request)
        req_id = req.get("id")          # Hangi isteğe yanıt verdiğimizi eşleştiren kimlik.
        method = req.get("method")      # "tools/list" veya "tools/call"
        params = req.get("params", {})  # Çağrı parametreleri (yoksa boş sözlük).

        # 2. KEŞİF (Tool Discovery): İstemci "Hangi araçların var?" diye soruyor.
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

        # 3. ÇALIŞTIRMA (Tool Execution): İstemci belirli bir aracı argümanlarıyla çağırıyor.
        if method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            with self._lock:
                spec = self._tools.get(tool_name)
            if spec is None:
                # Standart JSON-RPC -32601 hata kodu: "Method/Tool bulunamadı".
                return json.dumps(
                    {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Tool not found"}},
                    ensure_ascii=False,
                )
            # Aracı kilit dışında çalıştırıp sonucu standart JSON-RPC formatında döndürüyoruz.
            output = spec.handler(arguments)
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": output}, ensure_ascii=False)

        # Desteklenmeyen bir metot adı geldiyse standart hata döndür.
        return json.dumps(
            {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}},
            ensure_ascii=False,
        )


def check_inventory(args: dict[str, Any]) -> dict[str, Any]:
    """Örnek arka uç (Backend) fonksiyonu: Verilen ürün kodunun (SKU) stoğunu döndürür."""
    sku = str(args.get("sku", ""))
    stock = {"SKU-LAPTOP-01": 12, "SKU-MOUSE-02": 0}
    return {"sku": sku, "in_stock": stock.get(sku, 0)}


def main() -> None:
    # 1. Bir MCP Server ayağa kaldırıp depo stok aracını kaydediyoruz.
    server = SimpleMCPServer("warehouse-mcp")
    server.register_tool(
        MCPToolSpec(
            name="check_inventory",
            description="Depo stok durumunu SKU koduna göre sorgular.",
            input_schema={"type": "object", "properties": {"sku": {"type": "string"}}, "required": ["sku"]},
            handler=check_inventory,
        )
    )

    # 2. MCP Client önce sunucuda hangi Tool'lar var diye keşif yapar (tools/list).
    list_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    print("MCP tools/list Yanıtı:", server.handle_json_rpc(list_req))

    # 3. MCP Client standart formatla Tool çağırır (tools/call). (SKU-MOUSE-02 ile de deneyin!)
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
