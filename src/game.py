import random
from pathlib import Path

from src.board import Board
from src.dictionary import Dictionary
from src.player import Player
from src.tile import BoardTile, TileBag


class NotAWordException(Exception):
    pass


class Game:
    HAND_SIZE = 7

    def __init__(self, players=None):
        if not players:
            players = []
        self.board = Board()
        self.tile_bag = TileBag()
        dict_path = Path(__file__).parent.parent / "dicts" / "sowpods.txt"
        self.dictionary = Dictionary(dict_path)
        self.players: list[Player] = players
        self.current_player: Player | None = None
        self.player_turn: int = 0

        # isinstance() allows subclasses.
        # if len(players) == 0 or not all(isinstance(p, Player) for p in players):
        #     raise ValueError(
        #         "Players must be a non empty list of Player objects.")

    def start(self):
        self.player_turn = random.randint(0, len(self.players) - 1)
        print("Drawing hands...")
        for _ in self.players:
            assert self.current_player
            self.current_player.hand.extend(self.tile_bag.draw_n(Game.HAND_SIZE))
            self.__increment_turn_counter()

        while not self.is_game_over():
            self.turn_cycle()

    def turn_cycle(self):
        """Main turn cycle of the game"""
        assert self.current_player
        print(f"{self.current_player.name}'s turn")
        self.board.display()
        if self.current_player.api:
            self.current_player.api.on_turn()
        else:
            raise NotImplementedError("human player!")

        self.refill_hand(self.current_player)

    def refill_hand(self, player: Player):
        """
        Refills a given players hand
        """
        if len(player.hand) <= Game.HAND_SIZE:
            player.hand.extend(self.tile_bag.draw_n(Game.HAND_SIZE - len(player.hand)))
        else:
            raise ValueError(
                f"Cheater! hand too big: {player.hand} > {Game.HAND_SIZE}."
            )

    def is_game_over(self):
        """
        Checks if the game is over
        """
        raise NotImplementedError()

    def add_player(self, player: Player):
        """
        Adds player to the game
        """
        self.players.append(player)

    def __increment_turn_counter(self):
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.current_player = self.players[self.player_turn]

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
