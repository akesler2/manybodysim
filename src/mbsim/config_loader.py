"""YAML-backed hierarchical config loading for simulations."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import yaml

from mbsim.config import (
    BoundaryMode,
    ParticleInitConfig,
    NumericsConfig,
    PhysicalConstantsConfig,
    PhysicsConfig,
    SimulatorConfig,
    WorldConfig,
    physical_constants_from_mapping,
)
from mbsim.forces.accel import accel_from_forces
from mbsim.forces.force_models import no_force, uniform_acceleration, uniform_force
from mbsim.integrators.integrators import step_euler
from mbsim.types import AccelerationFn, ForceModelFn

INTEGRATOR_REGISTRY = {
    "euler": step_euler,
}

# Maps YAML ``physics.force_model`` names to factories that build a ``ForceModelFn``
# given merged ``PhysicalConstantsConfig`` (so models can read G, g, etc.).
ForceModelFactory = Callable[[PhysicalConstantsConfig], ForceModelFn]

FORCE_MODEL_REGISTRY: dict[str, ForceModelFactory] = {
    "none": lambda _pc: no_force,
    "uniform_accel": uniform_acceleration,
    "uniform_force": uniform_force,
    # Deprecated alias (same as uniform_accel)
    "constant": uniform_acceleration,
}


def make_accel_fn(force_name: str, physical_constants: PhysicalConstantsConfig) -> AccelerationFn:
    """Resolve registry name + constants into the integrator's acceleration callable."""
    key = force_name.lower()
    if key not in FORCE_MODEL_REGISTRY:
        valid = ", ".join(sorted(FORCE_MODEL_REGISTRY))
        raise ValueError(f"Unknown physics.force_model '{force_name}'. Valid: {valid}")
    model_fn = FORCE_MODEL_REGISTRY[key](physical_constants)
    return accel_from_forces([model_fn])

BOUNDARY_REGISTRY: dict[str, BoundaryMode] = {
    "reflective": BoundaryMode.REFLECTIVE,
    "none": BoundaryMode.NONE,
}


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file into a dict."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config at {p} must be a mapping/object at root.")
    return data


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge override into base (override wins)."""
    merged: dict[str, Any] = dict(base)
    for key, override_val in override.items():
        base_val = merged.get(key)
        if isinstance(base_val, dict) and isinstance(override_val, dict):
            merged[key] = deep_merge(base_val, override_val)
        else:
            merged[key] = override_val
    return merged


def _required_section(data: dict[str, Any], name: str) -> dict[str, Any]:
    section = data.get(name)
    if not isinstance(section, dict):
        raise ValueError(f"Missing required config section: '{name}'.")
    return section


def simulation_config_from_dict(data: dict[str, Any]) -> SimulatorConfig:
    """Build validated SimulatorConfig from merged hierarchical dict."""
    world = _required_section(data, "world")
    particle_init_data = _required_section(data, "particle_init")
    numerics = _required_section(data, "numerics")
    physics = _required_section(data, "physics")

    width = float(world["width"])
    height = float(world["height"])
    n_particles = int(world["n_particles"])
    t_end = float(world["t_end"])
    dt = float(numerics["dt"])

    if width <= 0 or height <= 0:
        raise ValueError("world.width and world.height must be > 0.")
    if n_particles < 1:
        raise ValueError("world.n_particles must be >= 1.")
    if t_end <= 0:
        raise ValueError("world.t_end must be > 0.")
    if dt <= 0:
        raise ValueError("numerics.dt must be > 0.")

    integrator_name = str(numerics["integrator"]).lower()
    force_raw = physics.get("force_model", physics.get("accel_model"))
    if force_raw is None:
        raise ValueError("physics must include 'force_model' (or legacy 'accel_model').")
    force_name = str(force_raw).lower()
    boundary_raw = world.get("boundaries", "reflective")
    boundary_name = str(boundary_raw).lower()

    if integrator_name not in INTEGRATOR_REGISTRY:
        valid = ", ".join(sorted(INTEGRATOR_REGISTRY))
        raise ValueError(f"Unknown numerics.integrator '{integrator_name}'. Valid: {valid}")
    if force_name not in FORCE_MODEL_REGISTRY:
        valid = ", ".join(sorted(FORCE_MODEL_REGISTRY))
        raise ValueError(f"Unknown physics.force_model '{force_name}'. Valid: {valid}")
    if boundary_name not in BOUNDARY_REGISTRY:
        valid = ", ".join(sorted(BOUNDARY_REGISTRY))
        raise ValueError(f"Unknown world.boundaries '{boundary_name}'. Valid: {valid}")

    v_std = float(particle_init_data["v_std"])
    if v_std < 0:
        raise ValueError("particle_init.v_std must be >= 0.")

    particle_init = ParticleInitConfig(
        width=width,
        height=height,
        mass=float(particle_init_data["mass"]),
        v_mean=float(particle_init_data["v_mean"]),
        v_std=v_std,
        seed=int(particle_init_data["seed"]) if particle_init_data.get("seed") is not None else None,
    )

    pc_raw = data.get("physical_constants")
    if pc_raw is not None and not isinstance(pc_raw, dict):
        raise ValueError("physical_constants must be a mapping/object when provided.")
    physical_constants = physical_constants_from_mapping(pc_raw)

    return SimulatorConfig(
        world=WorldConfig(
            width=width,
            height=height,
            n_particles=n_particles,
            t_end=t_end,
            boundaries=BOUNDARY_REGISTRY[boundary_name],
        ),
        numerics=NumericsConfig(dt=dt, integrator=INTEGRATOR_REGISTRY[integrator_name]),
        particle_init=particle_init,
        physics=PhysicsConfig(accel_fn=make_accel_fn(force_name, physical_constants)),
        physical_constants=physical_constants,
    )


def load_simulation_config(
    base_path: str | Path,
    scenario_path: str | Path | None = None,
    overrides: dict[str, Any] | None = None,
) -> SimulatorConfig:
    """Load base + optional scenario + optional overrides into SimulatorConfig."""
    merged = load_yaml(base_path)
    if scenario_path is not None:
        merged = deep_merge(merged, load_yaml(scenario_path))
    if overrides:
        merged = deep_merge(merged, overrides)
    return simulation_config_from_dict(merged)
