"""Player state and command handling."""

import logging
from typing import TYPE_CHECKING, NoReturn

from amazing.game.constants import MAX_BLOCKED_COUNTER

if TYPE_CHECKING:
    from amazing.game.game import Game

logger = logging.getLogger(__name__)

type PlayerState = dict[str, str | bool | int]


def _raise_unknown_command(command_str: str) -> NoReturn:
    message = f"Unknown command: {command_str}"
    raise ValueError(message)


class Player:
    """Represents one player connected to the game server."""

    def __init__(self, name: str, game: Game) -> None:
        """Initialize player state for a new game participant."""
        self.name = name
        self.blocked_counter = 0
        self.game = game
        self.score = 0

    @property
    def blocked(self) -> bool:
        """Return whether the player is blocked after repeated invalid commands."""
        return self.blocked_counter > MAX_BLOCKED_COUNTER

    def manage_command(self, command_str: str) -> str:
        """Validate and dispatch a player command.

        Returns:
            The command result returned to the client.
        """
        if self.blocked:
            return "BLOCKED"
        command = command_str.split()
        try:
            for command_type in ("MOVE", "FIRE", "RADAR"):
                if command[0] == command_type:
                    return getattr(self, command_type.lower())(command[1:])
            _raise_unknown_command(command_str)
        except ValueError as e:
            logger.warning("Problem for %s: %s", self.name, e)
            self.blocked_counter += 1
            if self.blocked:
                return "BLOCKED"
            return "KO"

    def update(self, delta_time: float) -> None:
        """Update runtime player state for one frame."""
        _ = delta_time
        if self.blocked:
            return

    def state(self) -> PlayerState:
        """Return a serializable view of the player state.

        Returns:
            A dictionary with the public player fields.
        """
        return {
            "name": self.name,
            "blocked": self.blocked,
            "score": self.score,
        }
