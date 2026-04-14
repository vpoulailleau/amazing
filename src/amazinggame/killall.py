"""Kill running Amazinggame-related Python processes."""

from contextlib import suppress

import psutil

launch_commands = [
    "python",
    "uv run",
    "uvx",
    "viewer",
    "server",
]
selectors = ["player.player", "sample_player", "server", "viewer"]


def main() -> None:
    """Main entrypoint for killing running Amazinggame-related Python processes."""
    for process in psutil.process_iter():
        with suppress(psutil.ZombieProcess, psutil.NoSuchProcess, psutil.AccessDenied):
            line = " ".join(process.cmdline()).lower()
            if not any(cmd in line for cmd in launch_commands):
                continue
            print("testing", line)  # noqa: T201
            if any(selector in line for selector in selectors) and (
                "killall" not in line
            ):
                print("    killing process:", line)  # noqa: T201
                process.kill()


if __name__ == "__main__":
    main()
