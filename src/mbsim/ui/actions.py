"""Button and action handlers for simulation lifecycle."""

from __future__ import annotations

import streamlit as st


def render_action_buttons(container=st) -> tuple[bool, bool]:
    """Render Run and Reset buttons; return (run_clicked, reset_clicked)."""
    run_clicked = container.button("Run simulation", use_container_width=True)
    reset_clicked = container.button("Reset", use_container_width=True)
    return run_clicked, reset_clicked
