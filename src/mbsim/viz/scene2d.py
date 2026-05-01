"""2D particle scene rendering helpers."""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from mbsim.types import Mat2

from .style import BACKGROUND_COLOR, PARTICLE_COLOR


def draw_particle_frame(
    positions: Mat2,
    width: float,
    height: float,
    title: str = "Many-Body Simulation",
    fig_width: float = 8.0,
) -> Figure:
    """Render a single 2D frame and return a matplotlib figure."""
    fig_height = fig_width * (height / width) if width > 0 else fig_width
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.scatter(positions[:, 0], positions[:, 1], s=12, c=PARTICLE_COLOR)
    ax.set_xlim(0.0, width)
    ax.set_ylim(0.0, height)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return fig
