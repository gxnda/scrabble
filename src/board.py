from colorama import init, Back, Style

from tile import BoardTile

init()


class Board:
    """
    Basic Scrabble board.
    """

    def __init__(self, rows=15, cols=15):
        self.rows = rows
        self.cols = cols
        self.grid: list[list[BoardTile]] = self._create_empty_board()
        print(self.display())

    def _create_empty_board(self):
        with open("blankboard.txt", "r") as f:
            temp = [line.strip().split() for line in f.readlines()]
        board = []
        for row in temp:
            new = []
            for col in row:
                tile = BoardTile.quick_create(col)
                new.append(tile)
            board.append(new)

        return board

    def display(self):
        for i, row in enumerate(self.grid):
            print("|".join([tile.get_style() + str(tile) + Back.RESET for tile in row]))
            if i < self.rows - 1:
                print("-" * (self.cols * 2 - 1))

    def place_letter(self, row, col, piece):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = piece
        else:
            raise ValueError("Position out of bounds")


if __name__ == "__main__":
    board = Board()
