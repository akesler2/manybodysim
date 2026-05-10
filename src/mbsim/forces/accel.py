# defines a helper function to compute acceleration from net force and mass

import numpy as np

from mbsim.types import AccelerationFn, ForceModelFn, Mat2, ScalarProperty


def acceleration(net_force: Mat2, m: ScalarProperty) -> Mat2:
    return net_force / m[:, np.newaxis]


def accel_from_forces(force_models: list[ForceModelFn]) -> AccelerationFn:
    """Combine force models into a single AccelerationFn (F_net / m for each particle)."""

    def accel(pos: Mat2, vel: Mat2, masses: ScalarProperty, t: float) -> Mat2:
        net_force = np.zeros_like(pos, dtype=float)
        for force_model in force_models:
            net_force += force_model(pos, vel, masses, t)
        return acceleration(net_force, masses)

    return accel
