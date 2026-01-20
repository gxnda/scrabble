from pathlib import Path

from src.board import Board
from src.dictionary import Dictionary
from src.player import Player
from src.tile import BoardTile


class NotAWordException(Exception):
    pass

class Game:
    def __init__(self):
        self.board = Board()
        dict_path = Path(__file__).parent.parent / "dicts" / "sowpods.txt"
        self.dictionary = Dictionary(dict_path)
        self.players: list[Player] = []
        self.player_turn: int = 0

    def add_player(self, player: Player):
        self.players.append(player)

    def __increment_turn_counter(self):
        self.player_turn = (self.player_turn + 1) % len(self.players)

    @staticmethod
    def calculate_word_score(word_tiles: list[BoardTile]):
        total_score, total_mult = 0, 1
        for tile in word_tiles:
            score, mult = tile.calculate_score()
            total_score += score
            total_mult *= mult
        return total_score * total_mult

    def __find_connected(self, row, col, look_vertical: bool):
        tile = self.board.get(row, col)
        j = 0
        while not tile.is_empty():
            j -= 1
            try:
                tile = self.board.get(
                    row + (j if look_vertical else 0),
                    col + (j if not look_vertical else 0),
                )
            except ValueError:
                break
        wordtiles = []
        j += 1  # get back to the word
        tile = self.board.get(
            row + (j if look_vertical else 0),
            col + (j if not look_vertical else 0),
        )
        while not tile.is_empty():
            wordtiles.append(tile)
            j += 1
            try:
                tile = self.board.get(
                    row + (j if look_vertical else 0),
                    col + (j if not look_vertical else 0),
                )
            except ValueError:
                break
        return wordtiles

    def get_connecting_words(
        self, row: int, col: int, word: str, is_vertical: bool
    ) -> list[list[BoardTile]]:
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

    def _check_word_fits(
        self, start_row: int, start_col, word: str, is_vertical: bool
    ) -> int:
        """check if placement is empty or duplicate letter, returning the total overlaps"""
        total_overlaps = 0
        for i, char in enumerate(word):
            if is_vertical:
                board_tile = self.board.get(start_row + i, start_col)
            else:
                board_tile = self.board.get(start_row, start_col + i)

            if not board_tile.is_empty() and board_tile.letter != char:
                raise ValueError(
                    f"{word} has invalid placement at {start_row + i}, {start_col + i}"
                )
            if board_tile.letter == char:
                total_overlaps += 1
        return total_overlaps

    def place_word(self, start_row: int, start_col: int, word: str, is_vertical: bool):
        """
        Places a word on the board.
        Any overlap should be included.

        Ends the current players turn afterwards.
        """
        all_used_tiles = []
        # raises error if word does not fit / overlaps incorrectly
        try:
            total_overlaps = self._check_word_fits(
                start_row, start_col, word, is_vertical
            )
        except ValueError as e:
            raise e

        # check if bingo
        score = 0
        total_used_letters = len(word) - total_overlaps
        if total_used_letters == 7:  # hand size
            score += 50  # + 50 if bingo

        connecting_words = self.get_connecting_words(
            start_row, start_col, word, is_vertical
        )

        for connecting in connecting_words:
            parsed_connecting_word = "".join(char.letter for char in connecting)
            if parsed_connecting_word not in self.dictionary:
                raise NotAWordException(f"{connecting} is not in {self.dictionary}.")

            # score all words
            score += Game.calculate_word_score(connecting)
            for char in connecting:
                # use it up later
                if char not in all_used_tiles:
                    all_used_tiles.append(char)

        for char in all_used_tiles:
            char.use_up()
