"""User interaction events (click/keyboard) mapped to simulation intents."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InteractionEvent:
    """Generic UI event to be consumed by simulation logic."""

    event_type: str
    x: float | None = None
    y: float | None = None
    payload: dict | None = None
