"""Reusable Streamlit controls for simulation parameters."""

from __future__ import annotations

import streamlit as st

from mbsim.config import (
    ParticleInitConfig,
    NumericsConfig,
    PhysicsConfig,
    SimulatorConfig,
    WorldConfig,
)


def build_simulator_config(defaults: SimulatorConfig, container=st.sidebar) -> SimulatorConfig:
    """Render basic controls and return an updated SimulatorConfig."""
    width = container.number_input("Width", value=float(defaults.width), min_value=1.0)
    height = container.number_input("Height", value=float(defaults.height), min_value=1.0)
    t_end = container.number_input("Simulation duration", value=float(defaults.t_end), min_value=0.1)
    dt = container.number_input("Time step", value=float(defaults.dt), min_value=1e-4)
    n_particles = container.slider("Particles", min_value=1, max_value=100, value=int(defaults.n_particles))
    v_mean = container.number_input(
        "v_mean", value=float(defaults.particle_init.v_mean), min_value=0.0, step=0.1
    )
    v_std = container.number_input(
        "v_std", value=float(defaults.particle_init.v_std), min_value=0.0, step=0.1
    )

    particle_init = ParticleInitConfig(
        width=width,
        height=height,
        mass=defaults.particle_init.mass,
        v_mean=v_mean,
        v_std=v_std,
        seed=defaults.particle_init.seed,
    )

    return SimulatorConfig(
        world=WorldConfig(
            width=width,
            height=height,
            n_particles=n_particles,
            t_end=t_end,
            boundaries=defaults.world.boundaries,
        ),
        numerics=NumericsConfig(dt=dt, integrator=defaults.integrator),
        particle_init=particle_init,
        physics=PhysicsConfig(accel_fn=defaults.accel_fn),
    )
