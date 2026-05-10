# uses config and engine to run the simulation.


import numpy as np
from mbsim.config_loader import make_accel_fn
from mbsim.integrators.integrators import step_euler
from mbsim.simulation.engine import advance_universe
from mbsim.state.particles import random_particle_gen
from mbsim.state.universe import Universe
from mbsim.config import (
    PhysicalConstantsConfig,
    default_particle_init,
    NumericsConfig,
    PhysicsConfig,
    SimulatorConfig,
    WorldConfig,
)
from mbsim.types import ParticleGeneratorFn, Mat2


_default_pc = PhysicalConstantsConfig()

default_sim_config = SimulatorConfig(
    world=WorldConfig(width=100, height=100, n_particles=2, t_end=10.0),
    numerics=NumericsConfig(dt=0.01, integrator=step_euler),
    particle_init=default_particle_init,
    physics=PhysicsConfig(accel_fn=make_accel_fn("none", _default_pc)),
    physical_constants=_default_pc,
)


def initial_universe(particle_gen: ParticleGeneratorFn, sim_config):
    # Constructs an initial universe from chosen ParticleGeneratorFn and sim_config
    particles = particle_gen(sim_config.n_particles, sim_config.particle_init)
    return Universe(particles, sim_config.width, sim_config.height)


class Result:
    # Result of run() \
    # Stores times, positions_history, velocities_history and the final universe
    # To be used by later UI, Viz, and Analysis modules 
    
    def __init__(self, times, universe):
        self.times = times
        self.positions_history = []
        self.velocities_history = []
        self.final_universe = universe

    def get_times(self):
        return self.times

    def get_positions_history(self):
        return self.positions_history

    def get_velocities_history(self):
        return self.velocities_history

    def get_final_universe(self):
        return self.final_universe

    def append_positions(self, pos: Mat2):
        self.positions_history.append(pos)

    def append_velocities(self, vel: Mat2):
        self.velocities_history.append(vel)


def run(sim_config):
    # calls initial_universe to construct initial conditions
    # loops steps through times using advance universe
    # returns a result object
    universe = initial_universe(random_particle_gen, sim_config)

    times = np.arange(0.0, sim_config.t_end, sim_config.dt)
    sim_result = Result(times, universe)

    for t in times:
        universe = advance_universe(
            universe,
            sim_config.accel_fn,
            sim_config.integrator,
            t,
            sim_config.dt,
            sim_config.boundaries,
        )
        sim_result.append_positions(universe.positions.copy())
        sim_result.append_velocities(universe.velocities.copy())

    sim_result.final_universe = universe

    return sim_result


