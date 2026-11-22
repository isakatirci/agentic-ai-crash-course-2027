"""
Modül 4 Hands-On Lab: RAG, Vector Database Mantığı ve Agentic RAG
- Chunking (metni parçalara bölme)
- Hafif Cosine Similarity tabanlı yerel Vector Store (Thread-Safe)
- Agentic RAG: İlk arama zayıfsa sorguyu yeniden yazıp (Query Rewrite) tekrar arama
"""

from __future__ import annotations

import math
import re
import threading
from collections import Counter
from dataclasses import dataclass

_TOKEN_RE = re.compile(r"[a-zA-ZçğıöşüÇĞİÖŞÜ0-9]+")


def text_to_vector(text: str) -> dict[str, float]:
    """Eğitim amaçlı hafif Term-Frequency vektörü. Gerçek sistemde Embedding API kullanılır."""
    tokens = [t.lower() for t in _TOKEN_RE.findall(text)]
    counts = Counter(tokens)
    norm = math.sqrt(sum(v * v for v in counts.values())) or 1.0
    return {k: v / norm for k, v in counts.items()}


def cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """İki normalize vektör arasındaki benzerlik skoru (0.0 - 1.0)."""
    if len(vec_a) > len(vec_b):
        vec_a, vec_b = vec_b, vec_a
    return sum(val * vec_b.get(key, 0.0) for key, val in vec_a.items())


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    chunk_id: str
    content: str
    vector: dict[str, float]


class ThreadSafeVectorStore:
    """Bellek içi (In-Memory) Thread-Safe Vector Store."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._chunks: list[DocumentChunk] = []

    def add_document(self, doc_id: str, text: str, chunk_size: int = 120) -> None:
        parts = [text[i : i + chunk_size].strip() for i in range(0, len(text), chunk_size)]
        new_chunks = [
            DocumentChunk(f"{doc_id}-{idx}", part, text_to_vector(part))
            for idx, part in enumerate(parts)
            if part
        ]
        with self._lock:
            self._chunks.extend(new_chunks)

    def search(self, query: str, top_k: int = 2) -> list[tuple[float, DocumentChunk]]:
        q_vec = text_to_vector(query)
        with self._lock:
            snapshot = list(self._chunks)
        scored = [(cosine_similarity(q_vec, chunk.vector), chunk) for chunk in snapshot]
        scored.sort(key=lambda item: item[0], reverse=True)
        return scored[:top_k]


def agentic_rag_search(store: ThreadSafeVectorStore, user_query: str, min_score: float = 0.25) -> str:
    """
    Agentic RAG Döngüsü:
    1. İlk sorguyu çalıştır.
    2. Benzerlik skoru eşiğin altındaysa sorguyu genişlet (Query Rewrite) ve tekrar ara.
    """
    results = store.search(user_query, top_k=1)
    if results and results[0][0] >= min_score:
        score, chunk = results[0]
        return f"[İlk Aramada Bulundu | Skor: {score:.2f}] -> {chunk.content}"

    # Query Rewrite (Sorgu İyileştirme)
    rewritten_query = f"{user_query} iade politikası süre gün kargo"
    retry_results = store.search(rewritten_query, top_k=1)
    if retry_results and retry_results[0][0] > 0.0:
        score, chunk = retry_results[0]
        return (
            f"[Agentic Query Rewrite Uygulandı | Yeni Skor: {score:.2f}] -> {chunk.content}"
        )
    return "İlgili bilgi veri tabanında bulunamadı."


def main() -> None:
    store = ThreadSafeVectorStore()
    store.add_document(
        "policy",
        "Müşteriler teslimattan itibaren 14 gün içinde ücretsiz kargo ile iade politikası kapsamında ürün iade edebilir.",
    )
    store.add_document(
        "support",
        "Teknik destek ekibi hafta içi 09:00 - 18:00 saatleri arasında canlı sohbet hizmeti verir.",
    )

    print("Sorgu 1 (Net):", agentic_rag_search(store, "iade politikası kaç gün?"))
    print("Sorgu 2 (Belirsiz):", agentic_rag_search(store, "beğenmezsem geri verebilir miyim?"))


if __name__ == "__main__":
    main()
