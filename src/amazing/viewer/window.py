import logging
from queue import Queue

import arcade
from amazing.viewer.animation import date, set_date
from amazing.viewer.constants import constants

input_queue: Queue = Queue()


class Window(arcade.Window):
    def __init__(self, addr: str, port: int) -> None:
        super().__init__(
            constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE
        )
        arcade.set_background_color(arcade.csscolor.BLACK)

    def setup(self) -> None:
        pass

    def on_draw(self):
        if not input_queue.empty():
            data = input_queue.get()
            date_server = data["time"]
            set_date(date_server)

        self.clear()


def gui_thread(addr: str, port: int) -> None:
    window = Window(addr, port)
    try:
        window.setup()
        arcade.run()
    except Exception:  # noqa: PIE786
        logging.exception("uncaught exception")
