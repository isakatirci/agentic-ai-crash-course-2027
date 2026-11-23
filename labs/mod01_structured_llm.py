"""
Modül 1 Hands-On Lab: LLM Engineering Temelleri
- Tokenization tahminleyici (precompiled regex ile yüksek performans)
- Context Window bütçe kontrolü
- Structured Outputs (JSON Schema doğrulama)
- %100 Thread-Safe tasarım (immutable dataclass & zero global mutable state)
"""

# Tip ipuçlarını (Type Hints) daha esnek kullanmamızı sağlar.
from __future__ import annotations

import json  # Metin halindeki JSON verisini Python sözlüğüne (dict) çevirir.
import re    # Düzenli ifadeler (Regex) ile metni parçalara ayırmak için kullanılır.
from dataclasses import dataclass  # Az kodla temiz veri sınıfları (Class) oluşturur.
from typing import Any

# Regex desenini fonksiyonun dışında 1 kez derliyoruz (High Efficiency).
# Böylece her çağrıda bilgisayar aynı deseni tekrar hesaplamaz.
_WORD_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


# frozen=True -> Nesne oluşturulduktan sonra değiştirilemez (Immutable & Thread-Safe).
# slots=True  -> Python'ın gereksiz bellek (RAM) harcamasını engeller.
@dataclass(frozen=True, slots=True)
class LLMRequestConfig:
    """Değiştirilemez (Immutable) LLM yapılandırması. Thread-Safe'tir."""

    model: str = "gpt-4o-mini"
    temperature: float = 0.0  # 0.0 = En tutarlı, sürprizsiz (Deterministik) çıktı.
    max_context_tokens: int = 4096  # Modelin tek seferde alabileceği üst Token sınırı.
    system_prompt: str = (
        "Sen bir destek bileti (Support Ticket) sınıflandırma uzmanısın. "
        "Yalnızca geçerli JSON döndür."
    )


@dataclass(frozen=True, slots=True)
class TicketClassification:
    """Structured Output sözleşmesi (Schema): Modelden beklediğimiz 3 zorunlu alan."""

    category: str
    priority: str
    summary: str


def estimate_tokens(text: str) -> int:
    """Basit ve hızlı bir Token sayısı tahminleyicisi."""
    # Metni kelimelere ve noktalama işaretlerine böler (liste döner).
    parts = _WORD_PATTERN.findall(text)
    # Türkçe eklemeli bir dil olduğu için parça sayısını 1.3 ile çarpıp güvenli tahmin alırız.
    return max(1, int(len(parts) * 1.3))


def validate_ticket_schema(raw_json: str) -> TicketClassification:
    """LLM çıktısını katı kurallarla doğrular (Schema Validation)."""
    # 1. JSON metnini Python sözlüğüne (dict) çeviriyoruz; bozuksa hata fırlatır.
    data: dict[str, Any] = json.loads(raw_json)

    # 2. Yalnızca izin verdiğimiz değerleri küme (set) olarak tanımlıyoruz (hızlı arama).
    allowed_categories = {"billing", "technical", "account"}
    allowed_priorities = {"low", "medium", "high"}

    # 3. Alanları güvenli şekilde okuyup küçük harfe çeviriyoruz (data.get hata vermez).
    category = str(data.get("category", "")).lower()
    priority = str(data.get("priority", "")).lower()
    summary = str(data.get("summary", "")).strip()

    # 4. İzin dışı bir değer geldiyse veritabanına yazmadan önce işlemi durduruyoruz.
    if category not in allowed_categories:
        raise ValueError(f"Geçersiz category: {category}")
    if priority not in allowed_priorities:
        raise ValueError(f"Geçersiz priority: {priority}")
    if not summary:
        raise ValueError("summary alanı boş olamaz.")

    # 5. Tüm kontroller geçti; artık güvenli ve tip korumalı nesnemizi döndürebiliriz.
    return TicketClassification(category=category, priority=priority, summary=summary)


def mock_structured_llm_call(user_message: str, config: LLMRequestConfig) -> str:
    """
    Harici API anahtarı olmadan Structured Outputs akışını test etmek için
    yerel deterministik simülatör. Gerçek projede burada OpenAI SDK çağrılır.
    """
    # API'ye gitmeden önce toplam Token bütçesini (System + User) kontrol ediyoruz.
    total_tokens = estimate_tokens(config.system_prompt) + estimate_tokens(user_message)
    if total_tokens > config.max_context_tokens:
        raise OverflowError(
            f"Context Window aşıldı! ({total_tokens} > {config.max_context_tokens})"
        )

    # Mesajı küçük harfe çevirip anahtar kelimelere göre örnek JSON hazırlıyoruz.
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

    # Python sözlüğünü Türkçe karakterleri koruyarak (ensure_ascii=False) JSON metnine çevirir.
    return json.dumps(payload, ensure_ascii=False)


def main() -> None:
    # 1. Ayar nesnesini oluşturuyoruz (Temperature=0.0).
    config = LLMRequestConfig(temperature=0.0)
    # 2. Denemek için örnek bir kullanıcı destek mesajı yazıyoruz. (Değiştirip tekrar deneyebilirsiniz!)
    user_ticket = "Kredi kartımdan bu ay iki kez fatura çekilmiş, acil kontrol eder misiniz?"

    # 3. Simüle edilmiş LLM'den ham JSON alıp şema doğrulamasından geçiriyoruz.
    raw_output = mock_structured_llm_call(user_ticket, config)
    validated = validate_ticket_schema(raw_output)

    print("Ham JSON Çıktısı:", raw_output)
    print("Doğrulanmış Nesne:", validated)
    print("Tahmini Token Sayısı:", estimate_tokens(user_ticket))


# Bu dosya doğrudan terminalden çalıştırıldığında main() fonksiyonunu başlatır.
if __name__ == "__main__":
    main()
