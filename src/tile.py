class Tile:
    """
    Basic scrabble tile, can either be blank or have a letter.
    """

    def __init__(self, letter: str = " "):
        """Initialize a tile with an optional letter (default is blank). Use "?" for blank tiles."""
        self.letter = letter

    def is_empty(self) -> bool:
        return self.letter == " "

    def place_letter(self, letter: str):
        if self.is_empty():
            self.letter = letter
        else:
            raise ValueError("Tile already has a letter")

    def clear(self):
        self.letter = " "

    def __str__(self):
        return self.letter


class BoardTile(Tile):
    """
    A tile on the Scrabble board that may have special properties.
    """

    def __init__(self, multiplier: int = 1, is_word_multiplier: bool = False):
        super().__init__()
        self.multiplier = multiplier
        self.is_word_multiplier = is_word_multiplier
        self.used = False

    @staticmethod
    def quick_create(creation_str: str):
        """
        Create a BoardTile from a shorthand string.
        Examples:
            "2L" -> double letter score
            "3W" -> triple word score
            "1"  -> normal tile
        """
        if creation_str.endswith("L"):
            multiplier = int(creation_str[:-1])
            return BoardTile(multiplier=multiplier, is_word_multiplier=False)
        elif creation_str.endswith("W"):
            multiplier = int(creation_str[:-1])
            return BoardTile(multiplier=multiplier, is_word_multiplier=True)
        else:
            return BoardTile()

    def use_tile(self):
        self.used = True

    def reset(self):
        self.used = False
        super().clear()
