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
from mbsim.config_loader import FORCE_MODEL_REGISTRY, make_accel_fn


def _force_model_labels() -> dict[str, str]:
    """Human-readable labels; marks deprecated registry aliases."""
    labels = {k: k.replace("_", " ") for k in FORCE_MODEL_REGISTRY}
    if "constant" in labels:
        labels["constant"] = "constant (alias → uniform_accel)"
    return labels


def build_simulator_config(defaults: SimulatorConfig, container=st.sidebar) -> SimulatorConfig:
    """Render basic controls and return an updated SimulatorConfig."""
    force_keys = tuple(sorted(FORCE_MODEL_REGISTRY.keys()))
    labels = _force_model_labels()
    cur = st.session_state.get("mbsim_force_model", "none")
    if cur not in force_keys:
        st.session_state["mbsim_force_model"] = "none"

    force_model = container.selectbox(
        "Force model",
        options=list(force_keys),
        format_func=lambda k: labels.get(k, k),
        key="mbsim_force_model",
        help="Registry keys from FORCE_MODEL_REGISTRY (see config_loader.py). "
        "Tune strengths via physical_constants on SimulatorConfig / YAML.",
    )

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

    accel_fn = make_accel_fn(force_model, defaults.physical_constants)

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
        physics=PhysicsConfig(accel_fn=accel_fn),
        physical_constants=defaults.physical_constants,
    )
