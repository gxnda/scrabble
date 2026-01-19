from pathlib import Path
from typing import Optional

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

        self.last_placed_tile: Optional[BoardTile] = None

    def add_player(self, player: Player):
        self.players.append(player)

    def __increment_turn_counter(self):
        self.player_turn = (self.player_turn + 1) % len(self.players)

    def end_turn(self):
        self.last_placed_tile = None
        self.__increment_turn_counter()

    def __find_connected(self, row, col, look_vertical: bool):
        tile = self.board.get(row, col)
        j = 0
        while tile.letter:
            j -= 1
            try:
                tile = self.board.get(
                    row + (j if look_vertical else 0),
                    col + (j if not look_vertical else 0),
                )
            except ValueError:
                break
        word = ""
        j += 1  # get back to the word
        while tile.letter:
            word += tile.letter
            j += 1
            try:
                tile = self.board.get(
                    row + (j if look_vertical else 0),
                    col + (j if not look_vertical else 0),
                )
            except ValueError:
                break
        return word

    def get_connecting_words(
        self, row: int, col: int, word: str, is_vertical: bool
    ) -> list[str]:
        """
        Gets all words connecting to a given word if it was placed on the board.
        It does not care if the word is valid.
        """
        words = []
        # First it checks all words in the perpendicular direction for each char
        for i in range(len(word)):
            # goes left until no word
            words.append(
                self.__find_connected(
                    row + (i if is_vertical else 0),
                    col + (i if not is_vertical else 0),
                    not is_vertical,
                )
            )

        words.append(self.__find_connected(row, col, is_vertical))

        return words

    # Stuff for API

    def _check_word_fits(self, start_row: int, start_col, word: str, is_vertical: bool):
        """check if placement is empty or duplicate letter"""
        for i, char in enumerate(word):
            if is_vertical:
                board_tile = self.board.get(start_row + i, start_col)
            else:
                board_tile = self.board.get(start_row, start_col + i)

            if not board_tile.is_empty() or board_tile.letter != char:
                raise ValueError(
                    f"{word} has invalid placement at {start_row + i}, {start_col + i}"
                )

    def place_word(self, start_row: int, start_col: int, word: str, is_vertical: bool):
        """
        Places a word on the board.
        Any overlap should be included.

        Ends the current players turn afterwards.
        """
        connecting_words = self.get_connecting_words(
            start_row, start_col, word, is_vertical
        )
        for connecting in connecting_words:
            if connecting not in self.dictionary:
                raise ValueError(f"{connecting} is not in {self.dictionary}.")
