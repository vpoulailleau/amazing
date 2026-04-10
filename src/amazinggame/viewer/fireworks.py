"""Firework shader wrapper used for player explosion effects."""

from importlib.resources import files
from pathlib import Path
from time import perf_counter

from arcade.experimental.shadertoy import Shadertoy

import amazinggame.viewer.resources
from amazinggame.viewer.constants import constants

ANIMATION_DURATION_SECONDS = 1.5


class Firework:
    """Manage one transient firework animation instance."""

    def __init__(self, position: tuple[float, float]) -> None:
        """Initialize shader state and start time for an explosion."""
        self.shadertoy = Shadertoy(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
            main_source=Path(
                str(files(amazinggame.viewer.resources) / "firework.glsl")
            ).read_text(encoding="utf-8"),
        )
        # uniform vec2 explosionPos;
        self.shadertoy.program["explosionPos"] = position
        self.shadertoy.program["explosionDurationSeconds"] = ANIMATION_DURATION_SECONDS
        self.start_time = perf_counter()

    def render(self) -> None:
        """Render the firework for the current frame."""
        self.shadertoy.render(time=perf_counter() - self.start_time)

    def finished(self) -> bool:
        """Return True when the firework duration has elapsed."""
        return perf_counter() - self.start_time > ANIMATION_DURATION_SECONDS
