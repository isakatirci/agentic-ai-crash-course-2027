"""
Modül 6 Hands-On Lab: Planning & Multi-Agent Stateful Workflow (LangGraph Mantığı)
- Node (Düğüm) ve Edge (Geçiş) tabanlı deterministik graf motoru
- Immutable State kopyalaması ile %100 Thread-Safe yürütme
- Koşullu yönlendirme (Conditional Edge): Reviewer onaylamazsa Writer'a geri döner
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Callable


@dataclass(frozen=True, slots=True)
class WorkflowState:
    topic: str
    plan: tuple[str, ...] = ()
    draft: str = ""
    review_passed: bool = False
    revision_count: int = 0


def planner_node(state: WorkflowState) -> WorkflowState:
    """1. Ajan (Planner): Konuyu alt adımlara böler."""
    steps = (
        f"{state.topic} nedir?",
        "Neden Production ortamında kritik önem taşır?",
        "Basit bir uygulama örneği",
    )
    return replace(state, plan=steps)


def writer_node(state: WorkflowState) -> WorkflowState:
    """2. Ajan (Writer): Plana göre taslak metin üretir."""
    if state.revision_count == 0:
        # İlk taslakta bilerek kısa bırakıyoruz ki Reviewer geri çevirsin.
        draft = f"{state.topic} önemlidir."
    else:
        bullet_text = " | ".join(state.plan)
        draft = f"{state.topic} kapsamlı özet -> {bullet_text}. Örnek: State izole edilmelidir."
    return replace(state, draft=draft, revision_count=state.revision_count + 1)


def reviewer_node(state: WorkflowState) -> WorkflowState:
    """3. Ajan (Reviewer): Taslağın kalite kriterini kontrol eder."""
    passed = len(state.draft) >= 50 and "Örnek:" in state.draft
    return replace(state, review_passed=passed)


def run_stateful_graph(initial_state: WorkflowState, max_revisions: int = 3) -> WorkflowState:
    """LangGraph benzeri koşullu geçişli (Conditional Edge) yürütme motoru."""
    nodes: dict[str, Callable[[WorkflowState], WorkflowState]] = {
        "planner": planner_node,
        "writer": writer_node,
        "reviewer": reviewer_node,
    }

    current_node = "planner"
    state = initial_state

    while current_node != "END":
        print(f"[GRAPH] Çalıştırılan Node: {current_node}")
        state = nodes[current_node](state)

        # Edge (Geçiş) Kuralları
        if current_node == "planner":
            current_node = "writer"
        elif current_node == "writer":
            current_node = "reviewer"
        elif current_node == "reviewer":
            if state.review_passed or state.revision_count >= max_revisions:
                current_node = "END"
            else:
                print("[GRAPH] Reviewer reddetti -> Writer düğümüne geri dönülüyor.")
                current_node = "writer"

    return state


def main() -> None:
    final_state = run_stateful_graph(WorkflowState(topic="Agentic AI State Management"))
    print("\n--- SONUÇ ---")
    print("Onay Durumu:", final_state.review_passed)
    print("Revizyon Sayısı:", final_state.revision_count)
    print("Nihai Taslak:", final_state.draft)


if __name__ == "__main__":
    main()
