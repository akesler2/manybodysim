# many-body-sim

2D many-body particle simulation playground built with Python, NumPy, Matplotlib, and Streamlit.

Current focus is a modular architecture for experimenting with simulation logic and quickly visualizing results while debugging.

## Current features

- 2D particle simulation pipeline with numpy-backed state arrays
- **Nested runtime configuration** (`SimulatorConfig`): domain/run settings (`WorldConfig`), time stepping (`NumericsConfig`), particle initialization (`ParticleInitConfig`), and forces (`PhysicsConfig`), with convenience properties on `SimulatorConfig` for older call sites (`width`, `dt`, `boundaries`, etc.)
- **Boundary modes** (`reflective` / `none`) on `WorldConfig`, applied in the simulation engine when set to reflective
- **Optional YAML hierarchy**: `configs/base.yaml` plus optional scenario files; merged dicts are turned into `SimulatorConfig` via string registries for integrator, acceleration model, and boundaries
- Pluggable acceleration and integrator function wiring (Python callables on the dataclasses; YAML maps names to those callables in `config_loader.py`)
- Streamlit UI with:
  - right-side control panel
  - run/reset actions
  - frame slider + prev/next stepping
  - play/pause animated playback with FPS control
  - frame/time readout for debugging
  - display mode toggle (`Simulation only`, `Energy only`, `Both panels`)
  - panel width control to fit plots in smaller screens
- Kinetic energy analysis and plotting

## Project layout

```text
many-body-sim/
├── pyproject.toml
├── requirements.txt
├── configs/
│   ├── base.yaml               # Default hierarchical simulation YAML
│   └── scenarios/              # Optional overrides merged into base
├── ui/
│   └── app.py                  # Streamlit entrypoint
└── src/mbsim/
    ├── config.py               # SimulatorConfig + nested frozen dataclasses
    ├── config_loader.py        # YAML load/merge → SimulatorConfig
    ├── types.py                # Shared type aliases and protocols
    ├── simulation/
    │   ├── engine.py           # Per-step state advancement
    │   └── runner.py           # Simulation orchestration + Result output
    ├── state/
    │   ├── particles.py        # Initial particle generation
    │   └── universe.py         # Universe state container
    ├── forces/
    │   └── accel_fns.py        # Acceleration models
    ├── integrators/
    │   └── integrators.py      # Numerical integrators (Euler currently)
    ├── analysis/
    │   ├── metrics.py          # Derived metrics (e.g. kinetic energy)
    │   └── timeseries.py
    ├── viz/
    │   ├── scene2d.py          # Particle frame rendering
    │   ├── plots.py            # Diagnostic charts
    │   └── style.py
    └── ui/
        ├── controls.py         # Reusable UI controls
        ├── actions.py          # Action button helpers
        └── state.py            # Streamlit session state helpers
```

## Setup

1. Create and activate a virtual environment (if not already created).
2. Install dependencies:

```bash
./venv/bin/pip install -r requirements.txt
./venv/bin/pip install -e .
```

The editable install (`-e .`) makes `mbsim` importable from the `src/` layout.

## Configuration

**In code**, the single object passed into `run()` is a `SimulatorConfig` (`mbsim.config`). It groups:

| Section | Dataclass | Typical contents |
|--------|-----------|------------------|
| `world` | `WorldConfig` | `width`, `height`, `n_particles`, `t_end`, `boundaries` (`BoundaryMode`) |
| `numerics` | `NumericsConfig` | `dt`, `integrator` (callable) |
| `particle_init` | `ParticleInitConfig` | box size for spawning, `mass`, `v_mean`, `v_std`, `seed` |
| `physics` | `PhysicsConfig` | `accel_fn` (callable) |

Shared defaults used by the runner and UI live in `mbsim.config` (`default_particle_init`) and `mbsim.simulation.runner` (`default_sim_config`, a full `SimulatorConfig`). The Streamlit app calls `build_simulator_config(default_sim_config, …)` so widgets override those defaults for the current session.

**From YAML**, use `load_simulation_config(base_path, scenario_path=None, overrides=None)` (`mbsim.config_loader`). It deep-merges base and scenario dicts, then maps string keys to library objects:

- `numerics.integrator` → e.g. `euler`
- `physics.accel_model` → e.g. `none`
- `world.boundaries` → `reflective` or `none` (defaults to `reflective` if omitted)

Example:

```python
from pathlib import Path

from mbsim.config_loader import load_simulation_config
from mbsim.simulation.runner import run

# Paths are resolved normally; run with cwd = repo root, or pass an absolute Path.
sim_config = load_simulation_config(Path("configs/base.yaml"))
result = run(sim_config)
```

To add a new integrator or force name, register it in `config_loader.py` next to `INTEGRATOR_REGISTRY` / `ACCEL_REGISTRY` (and extend `BoundaryMode` / `BOUNDARY_REGISTRY` for new wall behaviors).

## Run the app

From the project root:

```bash
./venv/bin/streamlit run ui/app.py
```

## Linting (optional but recommended)

Example tooling:

```bash
./venv/bin/ruff check src ui
./venv/bin/basedpyright src ui
```

## Notes on current state

- This project is an active work in progress.
- `particle_init` still carries its own `width` / `height` for spawning; keeping them in sync with `world` when loading from YAML is handled in the loader; a single source of truth for the box may be consolidated later.
- Architecture is intentionally modular to support future additions:
  - additional force models
  - new integrators (Verlet/leapfrog/RK)
  - richer diagnostics
  - interactive controls/events (mouse/keyboard)
