from src.tile import Tile


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand: list[Tile] = []
        self.time_remaining_s: float = 3 * 60
        self.api = None

    def assign_bot(self, game, bot_class):
        self.api = bot_class()
        self.api.hook(game, self)