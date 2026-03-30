import logging

from amazing.game.constants import MAX_BLOCKED_COUNTER


class Player:
    def __init__(self, name: str, game) -> None:
        self.name = name
        self.blocked_counter = 0
        self.game = game
        self.score = 0

    @property
    def blocked(self):
        return self.blocked_counter > MAX_BLOCKED_COUNTER

    def manage_command(self, command_str: str) -> str:
        if self.blocked:
            return "BLOCKED"
        command = command_str.split()
        try:
            for command_type in ("MOVE", "FIRE", "RADAR"):
                if command[0] == command_type:
                    return getattr(self, command_type.lower())(command[1:])
            raise ValueError(f"Unknown command: {command_str}")
        except ValueError as e:
            logging.warning("Problem for %s: %s", self.name, str(e))
            self.blocked_counter += 1
            if self.blocked:
                return "BLOCKED"
            return "KO"

    def update(self, delta_time: float) -> None:
        if self.blocked:
            return
        # TODO update parameters

    def state(self) -> dict:
        return {
            "name": self.name,
            "blocked": self.blocked,
            "score": self.score,
        }
