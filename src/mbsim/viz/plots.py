"""Matplotlib plots for analysis outputs."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np


def plot_kinetic_energy(
    times: np.ndarray, kinetic_energy: np.ndarray, fig_width: float = 6.0, fig_height: float = 3.0
) -> Figure:
    """Return a line plot of kinetic energy over time."""
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.plot(times, kinetic_energy, linewidth=1.5)
    ax.set_title("Kinetic Energy")
    ax.set_xlabel("time")
    ax.set_ylabel("energy")
    ax.grid(True, alpha=0.3)
    return fig
