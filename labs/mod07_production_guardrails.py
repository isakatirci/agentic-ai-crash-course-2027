"""
Modül 7 Hands-On Lab: Production-Ready Engineering
- Structured Observability Trace (LangSmith mantığı)
- Retry + Exponential Backoff + Fallback mekanizması
- Otomatik Evaluation (Deterministic Assert Checks)
- Thread-Safe Trace Collector
"""

from __future__ import annotations

import threading
import time  # Milisaniye hassasiyetinde süre ölçmek (perf_counter) ve beklemek (sleep) için.
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, slots=True)
class TraceEvent:
    """Uçağın kara kutusundaki tek bir kayıt satırı (Span): Ne çalıştı, kaç ms sürdü?"""

    span_name: str
    duration_ms: float
    status: str   # "OK" veya "ERROR"
    detail: str


class ThreadSafeTracer:
    """Production Observability için Thread-Safe izleme (Tracing) toplayıcısı."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._events: list[TraceEvent] = []

    def record(self, event: TraceEvent) -> None:
        """Yeni bir izleme kaydını güvenli biçimde listeye ekler."""
        with self._lock:
            self._events.append(event)

    def snapshot(self) -> list[TraceEvent]:
        """Kayıtların güvenli bir kopyasını döndürür."""
        with self._lock:
            return list(self._events)


def call_with_retry_and_fallback(
    primary_fn: Callable[[], str],
    fallback_fn: Callable[[], str],
    tracer: ThreadSafeTracer,
    max_retries: int = 2,
) -> str:
    """Geçici API hatalarında Retry yapar; başarısız olursa Fallback modele geçer."""
    # 1 ilk deneme + max_retries tekrar denemesi = toplam max_retries + 1 tur.
    for attempt in range(1, max_retries + 2):
        start = time.perf_counter()  # Yüksek hassasiyetli kronometreyi başlat.
        try:
            result = primary_fn()
            elapsed = (time.perf_counter() - start) * 1000  # Saniyeyi milisaniyeye çevir.
            tracer.record(TraceEvent("primary_llm", elapsed, "OK", f"attempt={attempt}"))
            return result
        except RuntimeError as exc:
            # Hata alındığında süreyi ve hata mesajını kara kutuya (Tracer) yazıyoruz.
            elapsed = (time.perf_counter() - start) * 1000
            tracer.record(TraceEvent("primary_llm", elapsed, "ERROR", f"attempt={attempt}: {exc}"))
            if attempt <= max_retries:
                # Exponential Backoff: Sunucuyu boğmamak için her denemede biraz daha fazla bekle.
                time.sleep(0.05 * attempt)

    # Birincil model tüm denemelerde başarısız oldu -> Yedek (Fallback) devreye giriyor!
    start = time.perf_counter()
    fallback_result = fallback_fn()
    elapsed = (time.perf_counter() - start) * 1000
    tracer.record(TraceEvent("fallback_llm", elapsed, "OK", "fallback_triggered"))
    return fallback_result


def evaluate_response(response: str, required_keywords: tuple[str, ...]) -> dict[str, object]:
    """Basit otomatik Evaluation: Dönen cevap zorunlu bilgileri eksiksiz içeriyor mu?"""
    lowered = response.lower()
    # Eksik kalan anahtar kelimeleri tek satırda (List Comprehension) buluyoruz.
    missing = [kw for kw in required_keywords if kw.lower() not in lowered]
    return {"passed": len(missing) == 0, "missing_keywords": missing}


def main() -> None:
    tracer = ThreadSafeTracer()
    attempts = {"count": 0}

    def unstable_primary() -> str:
        # Canlı ortamdaki geçici API hız sınırı (429 Rate Limit) hatasını simüle ediyoruz.
        attempts["count"] += 1
        raise RuntimeError("429 Rate Limit Exceeded")

    def reliable_fallback() -> str:
        # Birincil model çöktüğünde kullanıcıyı yarı yolda bırakmayan yedek yanıt.
        return "İade süresi 14 gündür ve kargo ücretsizdir."

    # 1. Retry + Fallback korumasıyla çağrıyı çalıştır.
    answer = call_with_retry_and_fallback(unstable_primary, reliable_fallback, tracer, max_retries=2)
    # 2. Üretilen cevabı otomatik Evaluation testinden geçir.
    eval_report = evaluate_response(answer, required_keywords=("14 gün", "ücretsiz"))

    print("Nihai Cevap:", answer)
    print("Evaluation Raporu:", eval_report)
    print("\n--- OBSERVABILITY TRACE ---")
    for ev in tracer.snapshot():
        print(f"  [{ev.status}] {ev.span_name} ({ev.duration_ms:.2f} ms) -> {ev.detail}")


if __name__ == "__main__":
    main()
