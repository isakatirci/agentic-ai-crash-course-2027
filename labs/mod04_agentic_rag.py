"""
Modül 4 Hands-On Lab: RAG, Vector Database Mantığı ve Agentic RAG
- Chunking (metni parçalara bölme)
- Hafif Cosine Similarity tabanlı yerel Vector Store (Thread-Safe)
- Agentic RAG: İlk arama zayıfsa sorguyu yeniden yazıp (Query Rewrite) tekrar arama
"""

from __future__ import annotations

import math  # Karekök (sqrt) ile vektör uzunluğunu normalize etmek için.
import re
import threading
from collections import Counter  # Her kelimenin metinde kaç kez geçtiğini hızlıca sayar.
from dataclasses import dataclass

# Türkçe karakterleri de kapsayan kelime ayırıcı Regex (1 kez derlenir).
_TOKEN_RE = re.compile(r"[a-zA-ZçğıöşüÇĞİÖŞÜ0-9]+")


def text_to_vector(text: str) -> dict[str, float]:
    """Eğitim amaçlı hafif Term-Frequency vektörü. Gerçek sistemde Embedding API kullanılır."""
    # 1. Metindeki tüm kelimeleri küçük harfe çevirip listeye alıyoruz.
    tokens = [t.lower() for t in _TOKEN_RE.findall(text)]
    # 2. Hangi kelime kaç kez geçmiş sayıyoruz (ör. {"iade": 2, "gün": 1}).
    counts = Counter(tokens)
    # 3. Vektörü 1 birim uzunluğa normalize ediyoruz (Cosine Similarity hesabı için).
    norm = math.sqrt(sum(v * v for v in counts.values())) or 1.0
    return {k: v / norm for k, v in counts.items()}


def cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """İki normalize vektör arasındaki benzerlik skoru (0.0 = alakasız, 1.0 = birebir aynı)."""
    # Performans optimizasyonu: Her zaman daha az elemanı olan sözlükte döngü kurarız.
    if len(vec_a) > len(vec_b):
        vec_a, vec_b = vec_b, vec_a
    # Ortak kelimelerin ağırlıklarını çarpıp topluyoruz (Dot Product).
    return sum(val * vec_b.get(key, 0.0) for key, val in vec_a.items())


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    """Veritabanında saklanan tek bir metin parçası (Chunk) ve onun sayısal vektörü."""

    chunk_id: str
    content: str
    vector: dict[str, float]


class ThreadSafeVectorStore:
    """Bellek içi (In-Memory) Thread-Safe Vector Store."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._chunks: list[DocumentChunk] = []

    def add_document(self, doc_id: str, text: str, chunk_size: int = 120) -> None:
        """Uzun metni chunk_size karakterlik parçalara böler (Chunking) ve vektörleştirir."""
        parts = [text[i : i + chunk_size].strip() for i in range(0, len(text), chunk_size)]
        new_chunks = [
            DocumentChunk(f"{doc_id}-{idx}", part, text_to_vector(part))
            for idx, part in enumerate(parts)
            if part
        ]
        # Kilit yalnızca listeye yeni parçaları eklerken tutulur.
        with self._lock:
            self._chunks.extend(new_chunks)

    def search(self, query: str, top_k: int = 2) -> list[tuple[float, DocumentChunk]]:
        """Sorguyu vektöre çevirir ve en yüksek benzerlik skoruna sahip top_k parçayı döndürür."""
        q_vec = text_to_vector(query)
        with self._lock:
            snapshot = list(self._chunks)  # Güvenli kopya üzerinde arama yapıyoruz.
        scored = [(cosine_similarity(q_vec, chunk.vector), chunk) for chunk in snapshot]
        # En yüksek skordan en düşüğe doğru sıralıyoruz.
        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[:top_k]


def agentic_rag_search(store: ThreadSafeVectorStore, user_query: str, min_score: float = 0.25) -> str:
    """
    Agentic RAG Döngüsü:
    1. İlk sorguyu çalıştır.
    2. Benzerlik skoru eşiğin altındaysa sorguyu genişlet (Query Rewrite) ve tekrar ara.
    """
    # Adım 1: Kullanıcının ham sorusuyla ilk aramayı yap.
    results = store.search(user_query, top_k=1)
    if results and results[0][0] >= min_score:
        score, chunk = results[0]
        return f"[İlk Aramada Bulundu | Skor: {score:.2f}] -> {chunk.content}"

    # Adım 2: Skor zayıfsa (ör. kullanıcı teknik terim bilmiyorsa) sorguyu zenginleştir.
    rewritten_query = f"{user_query} iade politikası süre gün kargo"
    retry_results = store.search(rewritten_query, top_k=1)
    if retry_results and retry_results[0][0] > 0.0:
        score, chunk = retry_results[0]
        return (
            f"[Agentic Query Rewrite Uygulandı | Yeni Skor: {score:.2f}] -> {chunk.content}"
        )
    return "İlgili bilgi veri tabanında bulunamadı."


def main() -> None:
    # 1. Yerel Vector Store oluştur ve iki şirket dokümanı yükle.
    store = ThreadSafeVectorStore()
    store.add_document(
        "policy",
        "Müşteriler teslimattan itibaren 14 gün içinde ücretsiz kargo ile iade politikası kapsamında ürün iade edebilir.",
    )
    store.add_document(
        "support",
        "Teknik destek ekibi hafta içi 09:00 - 18:00 saatleri arasında canlı sohbet hizmeti verir.",
    )

    # 2. Net soru ilk seferde bulunur; belirsiz soru ise Query Rewrite ile kurtarılır.
    print("Sorgu 1 (Net):", agentic_rag_search(store, "iade politikası kaç gün?"))
    print("Sorgu 2 (Belirsiz):", agentic_rag_search(store, "beğenmezsem geri verebilir miyim?"))


if __name__ == "__main__":
    main()
