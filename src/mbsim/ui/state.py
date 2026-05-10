"""Session state helpers for Streamlit UI."""

from __future__ import annotations

import streamlit as st


def init_ui_state() -> None:
    """Initialize required Streamlit session keys once."""
    st.session_state.setdefault("frame_idx", 0)
    st.session_state.setdefault("is_playing", False)
    st.session_state.setdefault("fps", 12)
    st.session_state.setdefault("sim_result", None)
    st.session_state.setdefault("mbsim_force_model", "none")
