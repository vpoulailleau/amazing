"""Core game state and command orchestration."""

import logging
from time import perf_counter

from amazing.game import Maze, generate_maze
from amazing.game.constants import MAX_NB_PLAYERS, MAZE_DIMENSION
from amazing.game.player import Player, PlayerState

logger = logging.getLogger(__name__)


class Game:
    """Runtime container for players, timers, and commands."""

    def __init__(self) -> None:
        """Initialize game timers and player storage."""
        self.start_time = perf_counter()
        self.last_update_time = self.start_time
        self.cumulated_time = 0.0
        self.players: list[Player] = []
        self.maze: Maze = None  # ty: ignore[invalid-assignment]

    @property
    def finished(self) -> bool:
        """Return whether the game has a winner."""
        return any(
            int(player.position[0]) == MAZE_DIMENSION - 1
            and int(player.position[1]) == MAZE_DIMENSION - 1
            for player in self.players
        )

    def start(self) -> None:
        """Reset timers when a game starts."""
        self.maze = generate_maze(MAZE_DIMENSION, MAZE_DIMENSION)
        self.start_time = perf_counter()
        self.last_update_time = self.start_time

    def manage_command(self, player_id: int, command: str) -> str:
        """Dispatch a command to the matching player.

        Returns:
            The status returned by the player command handler.
        """
        if player_id >= len(self.players):
            logger.error("Unknown player ID: %d", player_id)
            return "BLOCKED"
        return self.players[player_id].manage_command(command)

    def add_player(self, player_name: str) -> None:
        """Add a player when the server still has room."""
        if len(self.players) >= MAX_NB_PLAYERS:
            return
        player = Player(player_name, self)
        self.players.append(player)

    def update(self) -> None:
        """Advance timers and update every active player."""
        delta_time = perf_counter() - self.last_update_time
        for player in self.players:
            player.update(delta_time)
        self.last_update_time += delta_time
        self.cumulated_time += delta_time
        logger.debug("Cumulated time: %.3f", self.cumulated_time)

    def state(self) -> dict[str, float | list[PlayerState]]:
        """Return a serializable snapshot of the game state.

        Returns:
            A dictionary containing elapsed time and serialized players.
        """
        players: list[PlayerState] = [player.state() for player in self.players]
        data: dict[str, float | list[PlayerState]] = {
            "time": self.cumulated_time,
            "players": players,
        }
        return data
