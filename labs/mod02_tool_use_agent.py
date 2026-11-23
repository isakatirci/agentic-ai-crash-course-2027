"""
Modül 2 Hands-On Lab: Tool Use, Function Calling ve Güvenli Agent Loop
- Thread-Safe ToolRegistry (RLock korumalı)
- Max-Steps koruması (Sonsuz döngü önleme)
- Hata yakalama ve güvenli Tool çağrısı
"""

from __future__ import annotations

import threading  # Birden fazla kullanıcı aynı anda eriştiğinde kilit (Lock) koymak için.
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    """Bir aracın (Tool) kimlik kartı: adı, açıklaması ve çalıştırılacak Python fonksiyonu."""

    name: str
    description: str
    handler: Callable[..., dict[str, Any]]  # Çağrılabilir Python fonksiyonu referansı.


class ThreadSafeToolRegistry:
    """Birden fazla Thread aynı anda erişse bile güvenli kalan Tool kayıt defteri."""

    def __init__(self) -> None:
        # RLock (Reentrant Lock): Aynı anda sadece 1 Thread'in sözlüğü değiştirmesine izin verir.
        self._lock = threading.RLock()
        self._tools: dict[str, ToolDefinition] = {}  # Kayıtlı araçları tutan sözlük.

    def register(self, tool: ToolDefinition) -> None:
        # "with self._lock:" bloğu bitince kilit otomatik açılır (hata olsa bile).
        with self._lock:
            self._tools[tool.name] = tool

    def execute(self, name: str, **kwargs: Any) -> dict[str, Any]:
        # **kwargs: Fonksiyona gönderilen isimlendirilmiş parametreleri (ör. order_id="ORD-101") toplar.
        with self._lock:
            tool = self._tools.get(name)
        if tool is None:
            return {"ok": False, "error": f"Bilinmeyen tool: {name}"}
        try:
            # KRİTİK: Aracı çalıştırırken kilidi tutmuyoruz! Böylece diğer kullanıcılar beklemez.
            result = tool.handler(**kwargs)
            return {"ok": True, "data": result}
        except Exception as exc:
            # Araç hata verse bile tüm Agent çökmez; hata mesajı düzenli bir sözlük olarak döner.
            return {"ok": False, "error": str(exc)}


def get_order_status(order_id: str) -> dict[str, Any]:
    """Örnek dış servis aracı (Tool): Sipariş durumunu sorgular."""
    # Gerçek projede burada SQL veritabanına veya REST API'ye istek atılır.
    fake_db = {
        "ORD-101": {"status": "Kargoda", "eta_days": 2},
        "ORD-202": {"status": "Teslim Edildi", "eta_days": 0},
    }
    if order_id not in fake_db:
        raise KeyError(f"Sipariş bulunamadı: {order_id}")
    return fake_db[order_id]


def calculate_shipping_discount(order_total: float) -> dict[str, Any]:
    """Örnek hesaplama aracı (Tool): Kargo indirimini kesin matematikle hesaplar."""
    # LLM matematikte yanılabilir; kesin kuralları her zaman Python Tool'u hesaplar.
    free_shipping = order_total >= 500.0
    return {"free_shipping": free_shipping, "shipping_fee": 0.0 if free_shipping else 49.90}


def run_agent_loop(user_query: str, registry: ThreadSafeToolRegistry, max_steps: int = 3) -> str:
    """Basitleştirilmiş Think -> Act -> Observe Agent Loop."""
    observations: list[str] = []  # Agent'ın önceki adımlarda gördüğü araç sonuçları.

    # max_steps sınırı sayesinde Agent asla sonsuz döngüye girip bütçenizi yakmaz.
    for step in range(1, max_steps + 1):
        # 1. THINK: Kullanıcı sorusunda "ORD-" geçiyorsa sipariş aracını seç.
        if "ORD-" in user_query and not observations:
            # Cümle içindeki "ORD-101" kodunu noktalama işaretlerinden temizleyip ayıklıyoruz.
            order_id = next(word.strip(".,?!") for word in user_query.split() if word.startswith("ORD-"))
            # 2. ACT: Seçilen aracı güvenli kayıt defteri (Registry) üzerinden çalıştır.
            tool_result = registry.execute("get_order_status", order_id=order_id)
            # 3. OBSERVE: Gelen sonucu gözlem listesine kaydet ve kullanıcıya anlaşılır cevap üret.
            observations.append(f"Adım {step} [get_order_status]: {tool_result}")
            if tool_result["ok"]:
                info = tool_result["data"]
                return (
                    f"Siparişiniz ({order_id}) şu an '{info['status']}' durumunda. "
                    f"Tahmini teslimat: {info['eta_days']} gün."
                )
            return f"Sipariş sorgulanamadı: {tool_result['error']}"

        # Kullanıcı kargo soruyorsa kargo hesaplama aracını çağır.
        if "kargo" in user_query.lower():
            tool_result = registry.execute("calculate_shipping_discount", order_total=650.0)
            return f"Kargo hesaplaması tamamlandı: {tool_result['data']}"

    return "Maksimum adım sayısına (max_steps) ulaşıldı; işlem güvenli şekilde durduruldu."


def main() -> None:
    # 1. Araç kayıt defterini oluştur ve iki farklı Tool kaydet.
    registry = ThreadSafeToolRegistry()
    registry.register(ToolDefinition("get_order_status", "Sipariş durumunu getirir", get_order_status))
    registry.register(
        ToolDefinition("calculate_shipping_discount", "Kargo ücretini hesaplar", calculate_shipping_discount)
    )

    # 2. Farklı sorularla Agent Loop'u test et. (ORD-999 yazarak hata yönetimini de deneyebilirsiniz!)
    print(run_agent_loop("Merhaba, ORD-101 numaralı siparişim nerede?", registry))
    print(run_agent_loop("650 TL alışverişte kargo ücreti ne kadar?", registry))


if __name__ == "__main__":
    main()
