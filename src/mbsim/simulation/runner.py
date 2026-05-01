# uses config and engine to run the simulation.


import numpy as np
from mbsim.forces.accel_fns import no_accel
from mbsim.integrators.integrators import step_euler
from mbsim.simulation.engine import advance_universe
from mbsim.state.particles import random_particle_gen
from mbsim.state.universe import Universe
from mbsim.config import cfg, SimulatorConfig
from mbsim.types import ParticleGeneratorFn, Mat2



sim_cfg = SimulatorConfig(
    width = 100,
    height = 100,
    t_end = 10.0,
    dt = .01,
    n_particles = 2,
    generator = cfg,
    integrator = step_euler,
    accel_fn = no_accel,
)


def initial_universe(particle_gen: ParticleGeneratorFn, sim_cfg):
    # Constructs an initial universe from chosen ParticleGeneratorFn and sim_cfg
    particles = particle_gen(sim_cfg.n_particles, sim_cfg.generator)
    return Universe(particles, sim_cfg.width, sim_cfg.height)


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


def run(sim_cfg):
    # calls initial_universe to construct initial conditions
    # loops steps through times using advance universe
    # returns a result object
    universe = initial_universe(random_particle_gen,sim_cfg)

    times = np.arange(0.0, sim_cfg.t_end, sim_cfg.dt)
    sim_result = Result(times, universe)

    for t in times:
        universe =  advance_universe(universe, sim_cfg.accel_fn, sim_cfg.integrator, t, sim_cfg.dt)
        sim_result.append_positions(universe.positions.copy())
        sim_result.append_velocities(universe.velocities.copy())

    sim_result.final_universe = universe

    return sim_result


