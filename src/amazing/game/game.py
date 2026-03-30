import logging
from time import perf_counter

from amazing.game.constants import MAX_NB_PLAYERS
from amazing.game.player import Player


class Game:
    def __init__(self) -> None:
        self.start_time = perf_counter()
        self.last_update_time = self.start_time
        self.cumulated_time = 0
        self.players: list[Player] = []

    @property
    def finished(self) -> bool:
        return False  # TODO

    def start(self) -> None:
        self.start_time = perf_counter()
        self.last_update_time = self.start_time

    def manage_command(self, player_id: int, command: str) -> str:
        if player_id >= len(self.players):
            logging.error("Unknown player ID: %d", player_id)
            return "BLOCKED"
        return self.players[player_id].manage_command(command)

    def add_player(self, player_name: str) -> None:
        if len(self.players) >= MAX_NB_PLAYERS:
            return
        player = Player(player_name, self)
        self.players.append(player)

    def update(self) -> None:
        delta_time = perf_counter() - self.last_update_time
        for player in self.players:
            player.update(delta_time)
        self.last_update_time += delta_time
        self.cumulated_time += delta_time
        logging.error(self.cumulated_time)

    def state(self) -> dict:
        data = {
            "time": self.cumulated_time,
            "players": [player.state() for player in self.players],
        }
        for team, player in enumerate(data["players"]):
            player["team"] = team
        return data
