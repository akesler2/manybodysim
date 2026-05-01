
from __future__ import annotations
from mbsim.types import AccelerationFn, Integrator, Mat2
from mbsim.geometry.boundary import reflective_boundary

def advance_universe(universe, accel: AccelerationFn, integrator: Integrator, 
t: float, dt: float) -> tuple[Mat2, Mat2]:
    """passes the pos, vel and masses from universe and the acceleratinonFn to 
    integrator and returns the new positions and velocities"""

    pos = universe.positions
    vel = universe.velocities
    masses = universe.masses

    # Integrate the positions and velocities over time step dt
    pos, vel = integrator(pos,vel, masses, t, dt, accel)

    # Check particles against boundaries, and then update positions and velocities based on boundary rules
    pos, vel = reflective_boundary(pos, vel, universe.width, universe.height)
    
    # Update the universe with the new positions and velocities
    universe.update(pos, vel)

    return universe