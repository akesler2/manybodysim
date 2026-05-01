from dataclasses import dataclass

from mbsim.types import AccelerationFn, Integrator


@dataclass(frozen=True)
class GeneratorConfig:
    width: float
    height: float
    mass: float
    v_mean: float
    v_std: float
    seed: int | None = None


@dataclass(frozen=True)
class SimulatorConfig:
   # Global simulation parameters
    width: float
    height: float
    t_end: float
    dt: float

    # Number of particles to generate on initialization
    n_particles: int

    # Nested particle generation config
    generator: GeneratorConfig

    # Integration parameters
    integrator: Integrator
    accel_fn: AccelerationFn
    


cfg = GeneratorConfig(
    width = 100.0,
    height = 100.0,
    mass = 1.0,
    v_mean = 10.0,
    v_std = 10.0,
    seed = 42
    )

