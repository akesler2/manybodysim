# defines force models which are then used to compute accelerations

import numpy as np

from mbsim.config import PhysicalConstantsConfig
from mbsim.types import ForceModelFn, Mat2, ScalarProperty


def no_force(pos: Mat2, vel: Mat2, m: ScalarProperty, t: float) -> Mat2:
    n = pos.shape[0]
    return np.zeros((n, 2), dtype=float)


def uniform_acceleration(pc: PhysicalConstantsConfig) -> ForceModelFn:
    """Uniform acceleration field: ``F_i = m_i * a`` (same ``a`` for every particle).

    Default ``a = (0, -earth_gravity)``. Set ``uniform_accel_x`` / ``uniform_accel_y`` on
    ``PhysicalConstantsConfig`` for SI acceleration components (m s^-2).
    ``uniform_accel_y`` omitted or null uses ``-earth_gravity``.
    """

    ax = float(pc.uniform_accel_x)
    ay = (
        float(pc.uniform_accel_y)
        if pc.uniform_accel_y is not None
        else -float(pc.earth_gravity)
    )
    accel_vec = np.array([ax, ay], dtype=float)

    def force(pos: Mat2, vel: Mat2, masses: ScalarProperty, t: float) -> Mat2:
        return masses[:, np.newaxis] * accel_vec

    return force


def uniform_force(pc: PhysicalConstantsConfig) -> ForceModelFn:
    """Same force vector on every particle: ``F_i = (fx, fy)`` (not scaled by mass)."""

    fx = float(pc.uniform_force_fx)
    fy = float(pc.uniform_force_fy)
    fvec = np.array([fx, fy], dtype=float)

    def force(pos: Mat2, vel: Mat2, masses: ScalarProperty, t: float) -> Mat2:
        n = pos.shape[0]
        return np.broadcast_to(fvec, (n, 2)).copy()

    return force
