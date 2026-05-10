from __future__ import annotations

from dataclasses import dataclass, fields, replace
from enum import StrEnum
from typing import Any, Mapping

from mbsim.types import AccelerationFn, Integrator


class BoundaryMode(StrEnum):
    """How particles interact with the domain edge."""

    REFLECTIVE = "reflective"
    NONE = "none"


@dataclass(frozen=True)
class WorldConfig:
    """Simulation domain, boundaries, and top-level run settings."""

    width: float
    height: float
    n_particles: int
    t_end: float
    boundaries: BoundaryMode = BoundaryMode.REFLECTIVE


@dataclass(frozen=True)
class ParticleInitConfig:
    """Initial particle state generation settings."""

    width: float
    height: float
    mass: float
    v_mean: float
    v_std: float
    seed: int | None = None


@dataclass(frozen=True)
class NumericsConfig:
    """Numerical integration settings."""

    dt: float
    integrator: Integrator


@dataclass(frozen=True)
class PhysicalConstantsConfig:
    """Universal / model constants used by force laws (SI unless noted in YAML comments).

    Override any subset in YAML under ``physical_constants``. Unknown keys are rejected.
    """

    gravitational_constant: float = 6.67430e-11  # G [m^3 kg^-1 s^-2]
    coulomb_constant: float = 8.9875517923e9  # k_e [N m^2 C^-2]
    earth_mass: float = 5.972e24  # kg
    earth_radius: float = 6.371e6  # m
    earth_gravity: float = 9.80665  # m s^-2 (uniform field magnitude)
    # ``uniform_accel`` force model: uniform acceleration ``a`` with ``F_i = m_i * a``.
    # Default ``a = (0, -earth_gravity)``. Override components (SI m s^-2) for direction/magnitude.
    uniform_accel_x: float = 0.0
    uniform_accel_y: float | None = None  # None → ``-earth_gravity``
    # ``uniform_force`` model: identical force on every particle ``F_i = (fx, fy)`` (SI N).
    uniform_force_fx: float = 0.0
    uniform_force_fy: float = 0.0


def physical_constants_from_mapping(data: Mapping[str, Any] | None) -> PhysicalConstantsConfig:
    """Merge YAML (or dict) overrides onto defaults."""
    base = PhysicalConstantsConfig()
    if not data:
        return base
    data = _normalize_legacy_physical_constant_keys(dict(data))
    valid = {f.name for f in fields(PhysicalConstantsConfig)}
    overrides: dict[str, Any] = {}
    for key, raw in data.items():
        if key not in valid:
            raise ValueError(
                f"Unknown physical_constants key '{key}'. Valid: {', '.join(sorted(valid))}"
            )
        if raw is None:
            overrides[key] = None
        else:
            overrides[key] = float(raw)
    return replace(base, **overrides)


def _normalize_legacy_physical_constant_keys(data: dict[str, Any]) -> dict[str, Any]:
    """Map deprecated YAML keys to current names (new keys win if both are present)."""
    if "constant_force_accel_x" in data and "uniform_accel_x" not in data:
        data["uniform_accel_x"] = data.pop("constant_force_accel_x")
    if "constant_force_accel_y" in data and "uniform_accel_y" not in data:
        data["uniform_accel_y"] = data.pop("constant_force_accel_y")
    return data


@dataclass(frozen=True)
class PhysicsConfig:
    """Physics model settings."""

    accel_fn: AccelerationFn


@dataclass(frozen=True)
class SimulatorConfig:
    """Canonical runtime simulation config used by runner/engine."""

    world: WorldConfig
    numerics: NumericsConfig
    particle_init: ParticleInitConfig
    physics: PhysicsConfig
    physical_constants: PhysicalConstantsConfig = PhysicalConstantsConfig()

    # Backward-compatible convenience properties for existing call sites.
    @property
    def width(self) -> float:
        return self.world.width

    @property
    def height(self) -> float:
        return self.world.height

    @property
    def n_particles(self) -> int:
        return self.world.n_particles

    @property
    def t_end(self) -> float:
        return self.world.t_end

    @property
    def boundaries(self) -> BoundaryMode:
        return self.world.boundaries

    @property
    def dt(self) -> float:
        return self.numerics.dt

    @property
    def integrator(self) -> Integrator:
        return self.numerics.integrator

    @property
    def accel_fn(self) -> AccelerationFn:
        return self.physics.accel_fn


default_particle_init = ParticleInitConfig(
    width=100.0,
    height=100.0,
    mass=1.0,
    v_mean=10.0,
    v_std=10.0,
    seed=42,
)
