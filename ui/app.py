"""Streamlit entrypoint for interactive simulation playback."""

from __future__ import annotations

import time

import streamlit as st

from mbsim.analysis.metrics import kinetic_energy_timeseries
from mbsim.simulation.runner import default_sim_config, run
from mbsim.ui.actions import render_action_buttons
from mbsim.ui.controls import build_simulator_config
from mbsim.ui.state import init_ui_state
from mbsim.viz.plots import plot_kinetic_energy
from mbsim.viz.scene2d import draw_particle_frame


def main() -> None:
    # Page-level layout config. Change `layout` to "centered" for a narrower app.
    st.set_page_config(page_title="Many-Body Sim", layout="wide")
    st.markdown("### Many-Body Simulation (2D)")

    # Session bootstrap.
    init_ui_state()

    # Main layout: content on left, controls on right.
    # Streamlit's built-in sidebar is always left, so this right column acts as a
    # "right side panel" that is easier to customize.
    content_col, control_col = st.columns([4.5, 1.5], gap="small")

    with control_col:
        st.markdown("#### Controls")
        sim_config = build_simulator_config(default_sim_config, container=st)
        st.markdown("#### Actions")
        run_clicked, reset_clicked = render_action_buttons(container=st)
        panel_width = st.slider(
            "Panel width",
            min_value=0.5,
            max_value=1.0,
            value=0.60,
            step=0.05,
            help="Shrinks or expands the rendered panel within the page width.",
        )
        display_mode = st.radio(
            "Display mode",
            options=("Both panels", "Simulation only", "Energy only"),
            index=1,
        )

    # Reset clears cached results and returns playback to frame 0.
    if reset_clicked:
        st.session_state.sim_result = None
        st.session_state.frame_idx = 0
        st.session_state.is_playing = False

    # Run executes the simulation with current controls and stores result in session state.
    if run_clicked:
        st.session_state.sim_result = run(sim_config)
        st.session_state.frame_idx = 0
        st.session_state.is_playing = False

    # Early-return placeholder layout shown before first run.
    result = st.session_state.sim_result
    if result is None:
        st.info("Adjust settings, then click Run simulation.")
        return

    # Compact playback controls and plots live in content column.
    with content_col:
        max_frame = max(0, len(result.positions_history) - 1)
        play_col, prev_col, next_col, frame_col = st.columns([1.2, 1, 1, 7], gap="small")
        with play_col:
            play_label = "Pause" if st.session_state.is_playing else "Play"
            if st.button(play_label, width="stretch"):
                # Toggle playback. If already on the final frame, Play restarts from frame 0.
                if (not st.session_state.is_playing) and st.session_state.frame_idx >= max_frame:
                    st.session_state.frame_idx = 0
                st.session_state.is_playing = not st.session_state.is_playing
        with prev_col:
            if st.button("Prev", width="stretch"):
                st.session_state.is_playing = False
                st.session_state.frame_idx = max(0, st.session_state.frame_idx - 1)
        with next_col:
            if st.button("Next", width="stretch"):
                st.session_state.is_playing = False
                st.session_state.frame_idx = min(max_frame, st.session_state.frame_idx + 1)
        with frame_col:
            st.session_state.frame_idx = st.slider(
                "Frame", min_value=0, max_value=max_frame, value=st.session_state.frame_idx
            )
        frame = st.session_state.frame_idx

        # Compact playback status readout for debugging.
        current_time = float(result.times[frame]) if len(result.times) > frame else 0.0
        st.caption(f"Frame {frame + 1}/{max_frame + 1}  |  t = {current_time:.3f}s")

        # Analysis section: compute derived series for diagnostics panel(s).
        kinetic = kinetic_energy_timeseries(
            result.velocities_history, result.final_universe.masses
        )

        # Figure construction section.
        if display_mode in ("Both panels", "Simulation only"):
            scene_fig = draw_particle_frame(
                result.positions_history[frame],
                width=sim_config.width,
                height=sim_config.height,
                fig_width=6.2,
            )
        if display_mode in ("Both panels", "Energy only"):
            energy_fig = plot_kinetic_energy(
                result.times,
                kinetic,
                fig_width=6.2,
                fig_height=3.0,
            )

        # Final render layout for content area.
        # `panel_width` controls margins around the rendered panel(s) without
        # changing matplotlib plot coordinates or visual scale.
        side_margin = max((1.0 - panel_width) / 2.0, 0.01)
        left_pad, panel_slot, right_pad = st.columns(
            [side_margin, panel_width, side_margin], gap="small"
        )

        # Unused spacer columns intentionally keep plot panel narrower.
        _ = left_pad, right_pad

        with panel_slot:
            if display_mode == "Both panels":
                sim_col, energy_col = st.columns(2, gap="small")
                with sim_col:
                    st.pyplot(scene_fig, clear_figure=True, width="stretch")
                with energy_col:
                    st.pyplot(energy_fig, clear_figure=True, width="stretch")
            elif display_mode == "Simulation only":
                st.pyplot(scene_fig, clear_figure=True, width="stretch")
            else:
                st.pyplot(energy_fig, clear_figure=True, width="stretch")

    with control_col:
        st.markdown("#### Playback")
        st.session_state.fps = st.slider(
            "FPS",
            min_value=1,
            max_value=60,
            value=int(st.session_state.fps),
            step=1,
            help="Playback frame rate for Play mode.",
        )

    # Autoplay tick: advance one frame per rerun and stop at the final frame.
    if st.session_state.is_playing:
        if st.session_state.frame_idx < max_frame:
            time.sleep(1.0 / max(int(st.session_state.fps), 1))
            st.session_state.frame_idx += 1
            st.rerun()
        else:
            st.session_state.is_playing = False


if __name__ == "__main__":
    main()