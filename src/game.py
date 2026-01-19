from pathlib import Path

from src.board import Board
from src.dictionary import Dictionary
from src.player import Player
from src.tile import BoardTile


class Game:
    def __init__(self):
        self.board = Board()
        dict_path = Path(__file__).parent.parent / "dicts" / "sowpods.txt"
        self.dictionary = Dictionary(dict_path)
        self.players: list[Player] = []
        self.player_turn: int = 0

        self.last_placed_tile: BoardTile = BoardTile()

    def add_player(self, player: Player):
        self.players.append(player)

    def __increment_turn(self):
        self.player_turn = (self.player_turn + 1) % len(self.players)

