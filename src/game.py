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
        offset = col if look_vertical else row
        for offset in range(offset-1, -1, -1):
            tile = self.board.get(
                row + (offset if look_vertical else 0),
                col + (offset if not look_vertical else 0),
            )

            if not tile.letter:
                break

        word = ""
        max_size = self.board.cols if look_vertical else self.board.rows
        for i in range(offset, max_size):
            tile = self.board.get(
                row + (i if look_vertical else 0),
                col + (i if not look_vertical else 0),
            )

            if not tile.letter:
                break

            word = word + tile.letter

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

        # TODO: Check parallel as well

        return words

    # Stuff for API

    def _check_word_placement(
        self, start_row: int, start_col, word: str, is_vertical: bool
    ):
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
        if not word in self.dictionary:
            raise ValueError(f"{word} is not a valid word")
