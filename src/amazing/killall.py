"""Kill running Amazing-related Python processes."""

from contextlib import suppress

import psutil

teams = ["player.player"]

for process in psutil.process_iter():
    with suppress(psutil.ZombieProcess, psutil.NoSuchProcess, psutil.AccessDenied):
        line = " ".join(process.cmdline()).lower()
        if "python" not in line and "uv run" not in line:
            continue
        print("testing", line)  # noqa: T201
        if (
            "amazing." in line
            or ("sample_" in line and "_player" in line)
            or any(team in line for team in teams)
        ) and ("amazing.killall" not in line):
            print("    killing process:", line)  # noqa: T201
            process.kill()
