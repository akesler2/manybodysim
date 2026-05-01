# many-body-sim

2D many-body particle simulation playground built with Python, NumPy, Matplotlib, and Streamlit.

Current focus is a modular architecture for experimenting with simulation logic and quickly visualizing results while debugging.

## Current features

- 2D particle simulation pipeline with numpy-backed state arrays
- Configurable simulation parameters (`width`, `height`, `n_particles`, `dt`, `t_end`)
- Pluggable acceleration and integrator function wiring
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
├── ui/
│   └── app.py                  # Streamlit entrypoint
└── src/mbsim/
    ├── config.py               # Generator + simulator config dataclasses
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
- Architecture is intentionally modular to support future additions:
  - additional force models
  - new integrators (Verlet/leapfrog/RK)
  - richer diagnostics
  - interactive controls/events (mouse/keyboard)
