class Board:
    """
    Basic Scrabble board.
    """

    def __init__(self, rows=15, cols=15):
        self.rows = rows
        self.cols = cols
        self.grid = [[" " for _ in range(cols)] for _ in range(rows)]

    def display(self):
        for row in self.grid:
            print("|".join(row))
            print("-" * (self.cols * 2 - 1))

    def place_piece(self, row, col, piece):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = piece
        else:
            raise ValueError("Position out of bounds")

    def is_full(self):
        return all(cell != " " for row in self.grid for cell in row)
