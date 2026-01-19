import time
from copy import deepcopy


class MoveException(Exception):
    pass

class EarlyExitException(Exception):
    pass


class EarlyExitContextManager:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            if isinstance(exc_val, EarlyExitException):
                return True  # Suppress Exception, turn has been ended

        return False


class Api:
    def __init__(self, game, player):
        self.__player = player
        self.__game = game
        self.__board = self.__game.board

        self.__task = None

    @property
    def board_size(self) -> tuple[int, int]:
        return self.__board.rows, self.__board.cols

    @property
    def board(self) -> list[list]:
        """
        Returns a copy of the board.

        THIS IS NOT THE ACTUAL BOARD CLASS BENEDICT DON'T TRY TO CALL RANDOM METHODS
        """
        return deepcopy(self.__board.grid)

    def get_tiles_in_hand(self) -> list[str]:
        return [
            tile.letter for tile in self.__player.hand
        ]

    def place_word(self, word: str, is_vertical: bool, x: int, y: int) -> None:
        """ Calling this method ends your turn instantly """
        if type(word) is not str or type(is_vertical) is not bool and type(x) is not int and type(y) is not int:
            raise MoveException(f"Invalid arguments passed to Api.place_word(word: str, is_vertical: bool, x: int, y: int)")

        self.__task = ("place", (word, is_vertical, x, y))
        raise EarlyExitException

    def discard_letters(self, letters: list[str]) -> None:
        """ Calling this method ends your turn instantly """
        if type(letters) is not list or len(letters) <= 0 or len(letters) > 7:
            raise MoveException(f"Invalid arguments passed to Api.discard_letters(letters: list[str]): Min 1, Max 7")

        self.__task = ("discard", (letters,))
        raise EarlyExitException

    def pass_turn(self):
        """ Calling this method ends your turn instantly """
        self.__task = ("pass", ())
        raise EarlyExitException

    def on_turn(self):
        self.__task = None

        start = time.perf_counter()

        with EarlyExitContextManager():
            self._on_turn()

        elapsed = time.perf_counter() - start

        self.__player.time_remaining_s -= elapsed

        if not self.__task:
            print("[WARNING] A action was not performed. The turn has been passed")
            self.__task = ("pass", ())

        task, args = self.__task

        if task == "place":
            self.__game.place_word(*args)

        elif task == "discard":
            self.__game.discard_letter(*args)

        elif task == "pass":
            pass

        else:  # This should never get raised. But I know my coding skills.
            raise NotImplementedError(f"A task '{task}' is not implemented or is not intended")



    def _on_turn(self) -> None:
        """ This is ur bit silly """
        raise NotImplementedError

