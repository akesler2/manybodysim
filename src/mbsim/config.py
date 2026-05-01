from dataclasses import dataclass
from enum import StrEnum

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
