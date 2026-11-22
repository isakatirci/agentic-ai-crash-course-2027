"""
Modül 3 Hands-On Lab: Agent Memory & State Management
- Bounded Short-Term Memory (deque(maxlen=N) ile bellek sızıntısı önlenir)
- Session bazlı izole State Store (Thread-Safe RLock)
- Long-Term Memory (kalıcı kullanıcı tercihleri)
"""

from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str


@dataclass(slots=True)
class SessionState:
    session_id: str
    short_term: deque[Message] = field(default_factory=lambda: deque(maxlen=6))
    long_term_facts: dict[str, str] = field(default_factory=dict)


class ThreadSafeMemoryManager:
    """Her kullanıcı oturumu (Session) için izole ve Thread-Safe bellek yöneticisi."""

    def __init__(self, max_short_term_messages: int = 6) -> None:
        self._lock = threading.RLock()
        self._max_messages = max_short_term_messages
        self._sessions: dict[str, SessionState] = {}

    def _get_or_create(self, session_id: str) -> SessionState:
        state = self._sessions.get(session_id)
        if state is None:
            state = SessionState(
                session_id=session_id,
                short_term=deque(maxlen=self._max_messages),
            )
            self._sessions[session_id] = state
        return state

    def add_message(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            state = self._get_or_create(session_id)
            state.short_term.append(Message(role=role, content=content))

    def save_long_term_fact(self, session_id: str, key: str, value: str) -> None:
        with self._lock:
            state = self._get_or_create(session_id)
            state.long_term_facts[key] = value

    def build_context_snapshot(self, session_id: str) -> dict[str, object]:
        """Dışarıya kopya (snapshot) döndürür; böylece dış kod iç state'i bozamaz."""
        with self._lock:
            state = self._get_or_create(session_id)
            return {
                "session_id": state.session_id,
                "long_term_facts": dict(state.long_term_facts),
                "recent_messages": list(state.short_term),
            }


def main() -> None:
    memory = ThreadSafeMemoryManager(max_short_term_messages=4)
    session = "user-junior-01"

    memory.save_long_term_fact(session, "preferred_language", "Python")
    memory.save_long_term_fact(session, "experience_level", "Junior")

    for i in range(1, 7):
        memory.add_message(session, "user", f"Soru {i}: Agent Memory nasıl çalışır?")

    snapshot = memory.build_context_snapshot(session)
    print("Long-Term Facts:", snapshot["long_term_facts"])
    print(f"Short-Term Mesaj Sayısı (maxlen=4): {len(snapshot['recent_messages'])}")
    for msg in snapshot["recent_messages"]:
        print(f"  - [{msg.role}] {msg.content}")


if __name__ == "__main__":
    main()
