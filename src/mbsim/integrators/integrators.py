# Basic Euler's method integrator for solving equations of motion
from __future__ import annotations

from mbsim.types import AccelerationFn, Mat2, Masses


def step_euler(
    positions: Mat2,
    velocities: Mat2,
    masses: Masses,
    t: float,
    dt: float,
    accel_fn: AccelerationFn,
) -> tuple[Mat2, Mat2]:
    new_positions = positions + velocities * dt
    new_velocities = velocities + accel_fn(positions, velocities, masses, t) * dt
    return new_positions, new_velocities
