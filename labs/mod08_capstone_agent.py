"""
Modül 8 Hands-On Lab: Capstone Mini-Project (End-to-End Customer Support Agent)
Tüm modüllerin tek bir Thread-Safe sistemde birleşimi:
- Memory & Session State (Modül 3)
- Agentic RAG Bilgi Bankası (Modül 4)
- Tool Use (Sipariş Sorgulama) (Modül 2)
- Observability Trace & Evaluation (Modül 7)
"""

from __future__ import annotations

import threading
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class TraceSpan:
    session_id: str
    step: str
    latency_ms: float
    outcome: str


@dataclass(slots=True)
class SupportSession:
    session_id: str
    history: deque[str] = field(default_factory=lambda: deque(maxlen=5))


class ProductionSupportAgent:
    """Eşzamanlı (Concurrent) müşteri isteklerini güvenle işleyen Capstone Agent."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._sessions: dict[str, SupportSession] = {}
        self._traces: list[TraceSpan] = []
        self._knowledge_base = {
            "iade": "Teslimattan itibaren 14 gün içinde ücretsiz iade hakkınız vardır.",
            "garanti": "Tüm elektronik ürünlerde 24 ay resmi distribütör garantisi bulunur.",
        }
        self._orders = {
            "ORD-500": "Hazırlanıyor (Tahmini kargo: Yarın)",
            "ORD-501": "Kargoda (Takip No: TR998877)",
        }

    def _get_session(self, session_id: str) -> SupportSession:
        with self._lock:
            sess = self._sessions.get(session_id)
            if sess is None:
                sess = SupportSession(session_id=session_id)
                self._sessions[session_id] = sess
            return sess

    def _record_trace(self, span: TraceSpan) -> None:
        with self._lock:
            self._traces.append(span)

    def handle_request(self, session_id: str, user_message: str) -> str:
        start = time.perf_counter()
        session = self._get_session(session_id)

        with self._lock:
            session.history.append(f"USER: {user_message}")

        lowered = user_message.lower()
        # 1. Tool Use Routing (Sipariş sorgusu)
        if "ord-" in lowered:
            order_id = next(
                tok.strip(".,?!").upper() for tok in user_message.split() if tok.lower().startswith("ord-")
            )
            status = self._orders.get(order_id, "Sipariş bulunamadı.")
            reply = f"[Tool:OrderLookup] {order_id} durumu -> {status}"
            step_name = "tool_order_lookup"
        # 2. RAG Routing (Politika bilgisi)
        elif "iade" in lowered or "geri" in lowered:
            reply = f"[RAG:Policy] {self._knowledge_base['iade']}"
            step_name = "rag_policy_search"
        elif "garanti" in lowered:
            reply = f"[RAG:Policy] {self._knowledge_base['garanti']}"
            step_name = "rag_policy_search"
        else:
            reply = "[Fallback] Talebinizi netleştirebilir misiniz? Sipariş (ORD-XXX), iade veya garanti sorabilirsiniz."
            step_name = "fallback_clarify"

        with self._lock:
            session.history.append(f"AGENT: {reply}")

        latency = (time.perf_counter() - start) * 1000
        self._record_trace(TraceSpan(session_id, step_name, latency, "SUCCESS"))
        return reply

    def get_traces(self) -> list[TraceSpan]:
        with self._lock:
            return list(self._traces)


def main() -> None:
    agent = ProductionSupportAgent()
    requests = [
        ("sess-1", "ORD-500 siparişim ne durumda?"),
        ("sess-2", "Ürünü beğenmezsem iade süresi kaç gün?"),
        ("sess-3", "Kulaklıkların garanti süresi ne kadar?"),
        ("sess-1", "Teşekkürler, peki ORD-501 nerede?"),
    ]

    # Thread-Safety testi: 4 isteği aynı anda paralel ThreadPoolExecutor ile çalıştırıyoruz.
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(agent.handle_request, sid, msg) for sid, msg in requests]
        for (sid, msg), fut in zip(requests, futures):
            print(f"[{sid}] Soru: {msg}")
            print(f"[{sid}] Yanıt: {fut.result()}\n")

    print("--- CAPSTONE OBSERVABILITY TRACES ---")
    for span in agent.get_traces():
        print(f"  {span.session_id} | {span.step} | {span.latency_ms:.3f} ms | {span.outcome}")


if __name__ == "__main__":
    main()
