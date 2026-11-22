"""
Modül 1 Hands-On Lab: LLM Engineering Temelleri
- Tokenization tahminleyici (precompiled regex ile yüksek performans)
- Context Window bütçe kontrolü
- Structured Outputs (JSON Schema doğrulama)
- %100 Thread-Safe tasarım (immutable dataclass & zero global mutable state)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

# Regex desenini uygulama başında bir kez derliyoruz (High Efficiency).
_WORD_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


@dataclass(frozen=True, slots=True)
class LLMRequestConfig:
    """Değiştirilemez (Immutable) LLM yapılandırması. Thread-Safe'tir."""

    model: str = "gpt-4o-mini"
    temperature: float = 0.0  # Deterministik çıktı için 0.0
    max_context_tokens: int = 4096
    system_prompt: str = (
        "Sen bir destek bileti (Support Ticket) sınıflandırma uzmanısın. "
        "Yalnızca geçerli JSON döndür."
    )


@dataclass(frozen=True, slots=True)
class TicketClassification:
    """Structured Output sözleşmesi (Schema)."""

    category: str
    priority: str
    summary: str


def estimate_tokens(text: str) -> int:
    """Basit ve hızlı bir Token sayısı tahminleyicisi."""
    parts = _WORD_PATTERN.findall(text)
    # Türkçe ve karma metinlerde ortalama 1.3 token/parça güvenli bir yaklaşımdır.
    return max(1, int(len(parts) * 1.3))


def validate_ticket_schema(raw_json: str) -> TicketClassification:
    """LLM çıktısını katı kurallarla doğrular (Schema Validation)."""
    data: dict[str, Any] = json.loads(raw_json)
    allowed_categories = {"billing", "technical", "account"}
    allowed_priorities = {"low", "medium", "high"}

    category = str(data.get("category", "")).lower()
    priority = str(data.get("priority", "")).lower()
    summary = str(data.get("summary", "")).strip()

    if category not in allowed_categories:
        raise ValueError(f"Geçersiz category: {category}")
    if priority not in allowed_priorities:
        raise ValueError(f"Geçersiz priority: {priority}")
    if not summary:
        raise ValueError("summary alanı boş olamaz.")

    return TicketClassification(category=category, priority=priority, summary=summary)


def mock_structured_llm_call(user_message: str, config: LLMRequestConfig) -> str:
    """
    Harici API anahtarı olmadan Structured Outputs akışını test etmek için
    yerel deterministik simülatör. Gerçek projede burada OpenAI SDK çağrılır.
    """
    total_tokens = estimate_tokens(config.system_prompt) + estimate_tokens(user_message)
    if total_tokens > config.max_context_tokens:
        raise OverflowError(
            f"Context Window aşıldı! ({total_tokens} > {config.max_context_tokens})"
        )

    lowered = user_message.lower()
    if "fatura" in lowered or "ödeme" in lowered:
        payload = {
            "category": "billing",
            "priority": "high",
            "summary": "Kullanıcı ödeme veya fatura sorunu bildiriyor.",
        }
    elif "şifre" in lowered or "giriş" in lowered:
        payload = {
            "category": "account",
            "priority": "medium",
            "summary": "Kullanıcı hesap erişim problemi yaşıyor.",
        }
    else:
        payload = {
            "category": "technical",
            "priority": "low",
            "summary": "Genel teknik destek talebi.",
        }

    return json.dumps(payload, ensure_ascii=False)


def main() -> None:
    config = LLMRequestConfig(temperature=0.0)
    user_ticket = "Kredi kartımdan bu ay iki kez fatura çekilmiş, acil kontrol eder misiniz?"

    raw_output = mock_structured_llm_call(user_ticket, config)
    validated = validate_ticket_schema(raw_output)

    print("Ham JSON Çıktısı:", raw_output)
    print("Doğrulanmış Nesne:", validated)
    print("Tahmini Token Sayısı:", estimate_tokens(user_ticket))


if __name__ == "__main__":
    main()
