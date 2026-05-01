"""Shared types for the 2D numpy-based simulation core.

These aliases and protocols define a single contract across forces,
integrators, and simulation orchestration modules.
"""

from __future__ import annotations

from typing import Callable, Protocol, TypeAlias, TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
if TYPE_CHECKING:
    from mbsim.config import ParticleInitConfig

# Generic floating numpy array type used throughout the package.
FloatArray: TypeAlias = NDArray[np.floating]

# Shape intent (enforced by convention and runtime checks where needed):
# - Vec2: (2,)
# - Mat2: (n, 2)
# - Masses: (n,)
Vec2: TypeAlias = FloatArray
Mat2: TypeAlias = FloatArray
Masses: TypeAlias = FloatArray

# Acceleration function contract for array-based simulation.
# Input: positions, velocities, masses, current time
# Output: accelerations with shape (n, 2)
AccelerationFn: TypeAlias = Callable[[Mat2, Mat2, Masses, float], Mat2]

# Particle generator function contract for array-based simulation.
# Input: number of particles, might requite additional inputs
# Output: positions and velocities with shape (n, 2), and masses with shape (n,)
ParticleGeneratorFn: TypeAlias = Callable[
    [int, "ParticleInitConfig"], tuple[Mat2, Mat2, Masses]
]

class Integrator(Protocol):
    """Protocol for pluggable time integrators."""

    def step(
        self,
        positions: Mat2,
        velocities: Mat2,
        masses: Masses,
        t: float,
        dt: float,
        accel_fn: AccelerationFn,
    ) -> tuple[Mat2, Mat2]:
        """Advance one timestep and return (positions, velocities)."""

