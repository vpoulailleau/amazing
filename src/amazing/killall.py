"""Kill running Amazing-related Python processes."""

import logging
from contextlib import suppress

import psutil

logger = logging.getLogger(__name__)

teams = ["player.player"]

for process in psutil.process_iter():
    with suppress(psutil.ZombieProcess, psutil.NoSuchProcess, psutil.AccessDenied):
        line = " ".join(process.cmdline()).lower()
        if "python" not in line and "uv run" not in line:
            continue
        if (
            "amazing." in line
            or ("sample_" in line and "_player" in line)
            or any(team in line for team in teams)
        ) and ("amazing.killall" not in line):
            logger.info("killing process: %s", line)
            process.kill()
