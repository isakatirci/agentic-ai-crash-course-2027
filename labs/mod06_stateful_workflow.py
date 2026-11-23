"""
Modül 6 Hands-On Lab: Planning & Multi-Agent Stateful Workflow (LangGraph Mantığı)
- Node (Düğüm) ve Edge (Geçiş) tabanlı deterministik graf motoru
- Immutable State kopyalaması ile %100 Thread-Safe yürütme
- Koşullu yönlendirme (Conditional Edge): Reviewer onaylamazsa Writer'a geri döner
"""

from __future__ import annotations

# replace: frozen (değiştirilemez) bir dataclass'tan tek bir alanı güncellenmiş yeni kopya üretir.
from dataclasses import dataclass, replace
from typing import Callable


@dataclass(frozen=True, slots=True)
class WorkflowState:
    """Tüm düğümler (Nodes) arasında taşınan değiştirilemez (Immutable) iş akışı durumu."""

    topic: str
    plan: tuple[str, ...] = ()  # list yerine tuple kullanıyoruz çünkü tuple değiştirilemezdir!
    draft: str = ""
    review_passed: bool = False
    revision_count: int = 0


def planner_node(state: WorkflowState) -> WorkflowState:
    """1. Ajan (Planner): Büyük konuyu 3 net alt adıma böler."""
    steps = (
        f"{state.topic} nedir?",
        "Neden Production ortamında kritik önem taşır?",
        "Basit bir uygulama örneği",
    )
    # Mevcut state'i bozmuyoruz; yalnızca 'plan' alanı dolu yeni bir WorkflowState döndürüyoruz.
    return replace(state, plan=steps)


def writer_node(state: WorkflowState) -> WorkflowState:
    """2. Ajan (Writer): Plana göre taslak metin üretir."""
    if state.revision_count == 0:
        # İlk taslağı bilerek kısa bırakıyoruz ki Reviewer'ın reddedip geri gönderdiğini görelim.
        draft = f"{state.topic} önemlidir."
    else:
        # 2. turda (revizyonda) tüm plan maddelerini ve 'Örnek:' bölümünü ekleyerek düzeltiyoruz.
        bullet_text = " | ".join(state.plan)
        draft = f"{state.topic} kapsamlı özet -> {bullet_text}. Örnek: State izole edilmelidir."
    return replace(state, draft=draft, revision_count=state.revision_count + 1)


def reviewer_node(state: WorkflowState) -> WorkflowState:
    """3. Ajan (Reviewer): Taslağın kalite kriterlerine uyup uymadığını denetler."""
    # Kalite kuralı: Taslak en az 50 karakter olmalı VE içinde "Örnek:" kelimesi geçmeli.
    passed = len(state.draft) >= 50 and "Örnek:" in state.draft
    return replace(state, review_passed=passed)


def run_stateful_graph(initial_state: WorkflowState, max_revisions: int = 3) -> WorkflowState:
    """LangGraph benzeri koşullu geçişli (Conditional Edge) yürütme motoru."""
    # Graf üzerindeki tüm düğümleri (Nodes) isim -> fonksiyon sözlüğü olarak tanımlıyoruz.
    nodes: dict[str, Callable[[WorkflowState], WorkflowState]] = {
        "planner": planner_node,
        "writer": writer_node,
        "reviewer": reviewer_node,
    }

    current_node = "planner"  # Akış her zaman 'planner' düğümünden başlar.
    state = initial_state

    # "END" düğümüne ulaşana kadar grafı adım adım yürütüyoruz.
    while current_node != "END":
        print(f"[GRAPH] Çalıştırılan Node: {current_node}")
        # Aktif düğümün fonksiyonunu çağırıp güncellenmiş yeni State'i alıyoruz.
        state = nodes[current_node](state)

        # Edge (Geçiş) Kuralları: Bir sonraki düğüm hangisi olacak?
        if current_node == "planner":
            current_node = "writer"
        elif current_node == "writer":
            current_node = "reviewer"
        elif current_node == "reviewer":
            # Conditional Edge: Onaylandıysa veya revizyon hakkı bittiyse bitir; yoksa Writer'a dön!
            if state.review_passed or state.revision_count >= max_revisions:
                current_node = "END"
            else:
                print("[GRAPH] Reviewer reddetti -> Writer düğümüne geri dönülüyor.")
                current_node = "writer"

    return state


def main() -> None:
    # Başlangıç konusunu verip grafı başlatıyoruz. (topic metnini değiştirip tekrar çalıştırabilirsiniz!)
    final_state = run_stateful_graph(WorkflowState(topic="Agentic AI State Management"))
    print("\n--- SONUÇ ---")
    print("Onay Durumu:", final_state.review_passed)
    print("Revizyon Sayısı:", final_state.revision_count)
    print("Nihai Taslak:", final_state.draft)


if __name__ == "__main__":
    main()
