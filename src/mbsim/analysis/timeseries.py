"""Small helpers for creating analysis-ready series."""

from __future__ import annotations

import numpy as np


def time_axis(t_end: float, dt: float) -> np.ndarray:
    """Return evenly spaced sample times from 0 to t_end (exclusive)."""
    return np.arange(0.0, t_end, dt)
