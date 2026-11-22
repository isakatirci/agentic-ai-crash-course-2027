"""
Modül 2 Hands-On Lab: Tool Use, Function Calling ve Güvenli Agent Loop
- Thread-Safe ToolRegistry (RLock korumalı)
- Max-Steps koruması (Sonsuz döngü önleme)
- Hata yakalama ve güvenli Tool çağrısı
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    name: str
    description: str
    handler: Callable[..., dict[str, Any]]


class ThreadSafeToolRegistry:
    """Birden fazla Thread aynı anda erişse bile güvenli kalan Tool kayıt defteri."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        with self._lock:
            self._tools[tool.name] = tool

    def execute(self, name: str, **kwargs: Any) -> dict[str, Any]:
        with self._lock:
            tool = self._tools.get(name)
        if tool is None:
            return {"ok": False, "error": f"Bilinmeyen tool: {name}"}
        try:
            # Tool çalışırken lock'u tutmuyoruz; böylece eşzamanlılık (Concurrency) engellenmez.
            result = tool.handler(**kwargs)
            return {"ok": True, "data": result}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}


def get_order_status(order_id: str) -> dict[str, Any]:
    """Örnek dış servis aracı (Tool): Sipariş durumunu sorgular."""
    fake_db = {
        "ORD-101": {"status": "Kargoda", "eta_days": 2},
        "ORD-202": {"status": "Teslim Edildi", "eta_days": 0},
    }
    if order_id not in fake_db:
        raise KeyError(f"Sipariş bulunamadı: {order_id}")
    return fake_db[order_id]


def calculate_shipping_discount(order_total: float) -> dict[str, Any]:
    """Örnek hesaplama aracı (Tool): Kargo indirimini kesin matematikle hesaplar."""
    free_shipping = order_total >= 500.0
    return {"free_shipping": free_shipping, "shipping_fee": 0.0 if free_shipping else 49.90}


def run_agent_loop(user_query: str, registry: ThreadSafeToolRegistry, max_steps: int = 3) -> str:
    """Basitleştirilmiş Think -> Act -> Observe Agent Loop."""
    observations: list[str] = []

    for step in range(1, max_steps + 1):
        # 1. THINK: Hangi Tool çağrılmalı?
        if "ORD-" in user_query and not observations:
            order_id = next(word.strip(".,?!") for word in user_query.split() if word.startswith("ORD-"))
            # 2. ACT: Tool'u çağır
            tool_result = registry.execute("get_order_status", order_id=order_id)
            # 3. OBSERVE: Sonucu kaydet
            observations.append(f"Adım {step} [get_order_status]: {tool_result}")
            if tool_result["ok"]:
                info = tool_result["data"]
                return (
                    f"Siparişiniz ({order_id}) şu an '{info['status']}' durumunda. "
                    f"Tahmini teslimat: {info['eta_days']} gün."
                )
            return f"Sipariş sorgulanamadı: {tool_result['error']}"

        if "kargo" in user_query.lower():
            tool_result = registry.execute("calculate_shipping_discount", order_total=650.0)
            return f"Kargo hesaplaması tamamlandı: {tool_result['data']}"

    return "Maksimum adım sayısına (max_steps) ulaşıldı; işlem güvenli şekilde durduruldu."


def main() -> None:
    registry = ThreadSafeToolRegistry()
    registry.register(ToolDefinition("get_order_status", "Sipariş durumunu getirir", get_order_status))
    registry.register(
        ToolDefinition("calculate_shipping_discount", "Kargo ücretini hesaplar", calculate_shipping_discount)
    )

    print(run_agent_loop("Merhaba, ORD-101 numaralı siparişim nerede?", registry))
    print(run_agent_loop("650 TL alışverişte kargo ücreti ne kadar?", registry))


if __name__ == "__main__":
    main()
