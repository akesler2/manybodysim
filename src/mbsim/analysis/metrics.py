"""Metric computations over simulation histories."""

from __future__ import annotations

import numpy as np

from mbsim.types import Mat2, Masses


def kinetic_energy_frame(velocities: Mat2, masses: Masses) -> float:
    """Return total kinetic energy for one frame."""
    speed_sq = np.sum(velocities * velocities, axis=1)
    return float(0.5 * np.sum(masses * speed_sq))


def kinetic_energy_timeseries(
    velocities_history: list[Mat2], masses: Masses
) -> np.ndarray:
    """Return kinetic energy per frame."""
    return np.array([kinetic_energy_frame(frame, masses) for frame in velocities_history])
