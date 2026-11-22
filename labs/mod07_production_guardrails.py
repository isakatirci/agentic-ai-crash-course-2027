"""
Modül 7 Hands-On Lab: Production-Ready Engineering
- Structured Observability Trace (LangSmith mantığı)
- Retry + Exponential Backoff + Fallback mekanizması
- Otomatik Evaluation (Deterministic Assert Checks)
- Thread-Safe Trace Collector
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, slots=True)
class TraceEvent:
    span_name: str
    duration_ms: float
    status: str
    detail: str


class ThreadSafeTracer:
    """Production Observability için Thread-Safe izleme (Tracing) toplayıcısı."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._events: list[TraceEvent] = []

    def record(self, event: TraceEvent) -> None:
        with self._lock:
            self._events.append(event)

    def snapshot(self) -> list[TraceEvent]:
        with self._lock:
            return list(self._events)


def call_with_retry_and_fallback(
    primary_fn: Callable[[], str],
    fallback_fn: Callable[[], str],
    tracer: ThreadSafeTracer,
    max_retries: int = 2,
) -> str:
    """Geçici API hatalarında Retry yapar; başarısız olursa Fallback modele geçer."""
    for attempt in range(1, max_retries + 2):
        start = time.perf_counter()
        try:
            result = primary_fn()
            elapsed = (time.perf_counter() - start) * 1000
            tracer.record(TraceEvent("primary_llm", elapsed, "OK", f"attempt={attempt}"))
            return result
        except RuntimeError as exc:
            elapsed = (time.perf_counter() - start) * 1000
            tracer.record(TraceEvent("primary_llm", elapsed, "ERROR", f"attempt={attempt}: {exc}"))
            if attempt <= max_retries:
                time.sleep(0.05 * attempt)  # Kısa Exponential Backoff

    start = time.perf_counter()
    fallback_result = fallback_fn()
    elapsed = (time.perf_counter() - start) * 1000
    tracer.record(TraceEvent("fallback_llm", elapsed, "OK", "fallback_triggered"))
    return fallback_result


def evaluate_response(response: str, required_keywords: tuple[str, ...]) -> dict[str, object]:
    """Basit otomatik Evaluation: Cevap gerekli bilgileri içeriyor mu?"""
    lowered = response.lower()
    missing = [kw for kw in required_keywords if kw.lower() not in lowered]
    return {"passed": len(missing) == 0, "missing_keywords": missing}


def main() -> None:
    tracer = ThreadSafeTracer()
    attempts = {"count": 0}

    def unstable_primary() -> str:
        attempts["count"] += 1
        raise RuntimeError("429 Rate Limit Exceeded")

    def reliable_fallback() -> str:
        return "İade süresi 14 gündür ve kargo ücretsizdir."

    answer = call_with_retry_and_fallback(unstable_primary, reliable_fallback, tracer, max_retries=2)
    eval_report = evaluate_response(answer, required_keywords=("14 gün", "ücretsiz"))

    print("Nihai Cevap:", answer)
    print("Evaluation Raporu:", eval_report)
    print("\n--- OBSERVABILITY TRACE ---")
    for ev in tracer.snapshot():
        print(f"  [{ev.status}] {ev.span_name} ({ev.duration_ms:.2f} ms) -> {ev.detail}")


if __name__ == "__main__":
    main()
