# Performance improvements — TODO

Prioritized checklist for simulation and UI performance. Check items off as you implement them.

---

## Phase 1 — Fast wins (do first)

### [ ] Add `save_every` (history stride) in `run(...)`

- **What:** Only append/store every Nth timestep (e.g. `save_every=5` keeps 1/5 of frames).
- **Benefit:** Large reduction in memory and Python list growth; faster post-run playback when you do not need every physics step on disk.
- **Reasoning:** Full history is \(O(\text{steps} \times n \times 2)\) floats per array. Long `t_end` with small `dt` explodes storage and copy cost; most debugging only needs a coarser timeline.

### [ ] Make velocity history optional (`store_velocities`)

- **What:** Flag to skip recording `velocities_history` when the UI or analysis does not need it.
- **Benefit:** Cuts stored memory roughly in half for runs that only visualize positions.
- **Reasoning:** Kinetic energy and other metrics need velocities only if you compute them from history; if you derive energy during the run or subsample, you can avoid storing every velocity frame.

### [ ] Cache diagnostics in the UI (e.g. kinetic energy series)

- **What:** After `run(cfg)`, compute `kinetic_energy_timeseries` once and store in `st.session_state` keyed by result (or a run id); reuse on slider/playback reruns.
- **Benefit:** Fewer NumPy passes and less work on every Streamlit rerun.
- **Reasoning:** Streamlit reruns the script often; recomputing the same time series from full velocity history is wasted CPU.

### [ ] Lower default playback FPS (keep max high)

- **What:** Default `fps` in session state to a moderate value (e.g. 8–12); user can raise it.
- **Benefit:** Smoother perceived UI, less CPU contention with matplotlib redraws.
- **Reasoning:** Autoplay uses `sleep` + `rerun`; high FPS multiplies full-app reruns and figure creation cost.

---

## Phase 2 — Core data path

### [ ] Pre-allocate history arrays instead of list append

- **What:** Allocate `pos_hist` (and optionally `vel_hist`) with shape `(n_saved_frames, n, 2)` and index by frame; or one append per stride with known count.
- **Benefit:** Fewer allocations, better locality, predictable memory; faster than growing a Python list of arrays.
- **Reasoning:** List append + many `copy()` calls fragment memory and add interpreter overhead; pre-allocation matches fixed `steps` / `save_every`.

### [ ] Optional `float32` mode for state and history

- **What:** `dtype=np.float32` for positions, velocities, masses (configurable); document tradeoff vs `float64`.
- **Benefit:** Roughly half memory bandwidth and storage; often faster on large arrays.
- **Reasoning:** Many exploratory runs do not need double precision; errors accumulate from integrator choice and `dt` more than from float32 for moderate `n` and timescales.

### [ ] Guardrail: `max_frames` or auto-adjust `save_every`

- **What:** If `t_end / dt` exceeds a threshold, warn user and bump `save_every` (or cap stored frames) so memory stays bounded.
- **Benefit:** Prevents accidental OOM or multi-gigabyte sessions from one click in the UI.
- **Reasoning:** UX safety net when sliders allow huge step counts.

---

## Phase 3 — UI / rendering

### [ ] Ensure simulation does not rerun on frame-only changes

- **What:** After a successful `run`, only playback controls and plotting should rerun; do not call `run(cfg)` unless Run is clicked or params meaningfully change.
- **Benefit:** Large reduction in wall-clock time during scrubbing and play.
- **Reasoning:** Simulation is orders of magnitude more expensive than updating a matplotlib frame from cached arrays.

### [ ] “Preview render” mode for large `n`

- **What:** Smaller scatter markers, optional subsample of particles for display only (not physics).
- **Benefit:** Faster matplotlib to screen; still representative for layout debugging.
- **Reasoning:** Drawing thousands of markers with full styling every frame dominates when physics is cheap.

### [ ] Reduce redundant figure work where practical

- **What:** Only rebuild figures when `frame_idx` or display mode changes; avoid duplicate `st.pyplot` paths if Streamlit exposes stable patterns for your version.
- **Benefit:** Medium savings on busy reruns.
- **Reasoning:** Matplotlib figure creation and serialization to the browser is expensive relative to indexing one slice of an array.

---

## Phase 4 — Future many-body interactions

### [ ] Keep force API swappable (pairwise vs neighbor list)

- **What:** Single `AccelerationFn` signature; implementations behind it (naive pairs, grid, tree).
- **Benefit:** You can optimize hot path without rewriting integrator or UI.
- **Reasoning:** Naive \(O(N^2)\) becomes the bottleneck as soon as pairwise forces exist; architecture should allow swap without fork-lifting `engine.py`.

### [ ] Add a small benchmark script (`scripts/benchmark_step.py` or similar)

- **What:** Time one step or full run vs `n_particles` and `dt`; optional `--save-every`.
- **Benefit:** Data-driven decisions; catches regressions when you change integrator or boundaries.
- **Reasoning:** Performance tuning without measurement is guesswork.

### [ ] When adding interactions: neighbor list / cutoff or Barnes–Hut

- **What:** Spatial hashing or tree after naive implementation proves too slow.
- **Benefit:** Makes large `N` feasible where \(O(N^2)\) is not.
- **Reasoning:** Industry standard progression: correct slow reference → accelerated structure.

---

## Suggested implementation order (two sessions)

**Session A**

1. `save_every` + optional `store_velocities` in `runner.py` / `Result`
2. UI cache for kinetic energy (and any other per-result series)

**Session B**

1. Pre-allocated history buffers
2. `float32` option + frame-count guardrail
3. Preview render mode in `viz/scene2d.py` + UI toggle

---

## Notes

- Move this file outside the repo if you prefer it as personal notes only; paths above assume it lives at repo root for team visibility.
- Pair each checkbox with a short PR or commit message when done so history stays searchable.
