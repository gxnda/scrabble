"""Tests for Board class"""
import pytest
from src.board import Board
from src.tile import BoardTile


class TestBoard:
    """Test Board functionality"""

    def test_board_creation(self, empty_board):
        """Test creating a board"""
        assert empty_board is not None
        assert empty_board.rows == 15
        assert empty_board.cols == 15
        assert len(empty_board.grid) == 15
        assert all(len(row) == 15 for row in empty_board.grid)

    def test_board_is_empty(self, empty_board):
        """Test that new board is empty"""
        assert empty_board.is_empty()

    def test_board_not_empty_after_placement(self, empty_board):
        """Test that board is not empty after placing a letter"""
        empty_board.place(7, 7, "a")
        assert not empty_board.is_empty()

    def test_board_get_valid_position(self, empty_board):
        """Test getting a tile at valid position"""
        tile = empty_board.get(0, 0)
        assert isinstance(tile, BoardTile)

        tile = empty_board.get(7, 7)
        assert isinstance(tile, BoardTile)

        tile = empty_board.get(14, 14)
        assert isinstance(tile, BoardTile)

    def test_board_get_out_of_bounds(self, empty_board):
        """Test getting a tile at invalid position raises error"""
        with pytest.raises(ValueError, match="out of bounds"):
            empty_board.get(-1, 0)

        with pytest.raises(ValueError, match="out of bounds"):
            empty_board.get(0, -1)

        with pytest.raises(ValueError, match="out of bounds"):
            empty_board.get(15, 0)

        with pytest.raises(ValueError, match="out of bounds"):
            empty_board.get(0, 15)

    def test_board_place(self, empty_board):
        """Test placing a letter on the board"""
        empty_board.place(7, 7, "x")
        tile = empty_board.get(7, 7)
        assert tile.letter == "x"
        assert not tile.is_empty()

    def test_board_place_multiple(self, empty_board):
        """Test placing multiple letters"""
        empty_board.place(7, 7, "c")
        empty_board.place(7, 8, "a")
        empty_board.place(7, 9, "t")

        assert empty_board.get(7, 7).letter == "c"
        assert empty_board.get(7, 8).letter == "a"
        assert empty_board.get(7, 9).letter == "t"

    def test_board_center_is_word_multiplier(self, empty_board):
        """Test that center square (7,7) is a double word score"""
        center = empty_board.get(7, 7)
        assert center.multiplier == 2
        assert center.is_word_multiplier is True

    def test_board_corner_triple_word_scores(self, empty_board):
        """Test that corners are triple word scores"""
        corners = [(0, 0), (0, 14), (14, 0), (14, 14)]
        for row, col in corners:
            tile = empty_board.get(row, col)
            assert tile.multiplier == 3, f"Corner ({row}, {col}) should be 3W"
            assert tile.is_word_multiplier is True, f"Corner ({row}, {col}) should be word multiplier"

    def test_board_premium_squares_symmetric(self, empty_board):
        """Test that premium squares are symmetric"""
        # Test horizontal symmetry
        for row in range(15):
            for col in range(15):
                left_tile = empty_board.get(row, col)
                right_tile = empty_board.get(row, 14 - col)
                assert left_tile.multiplier == right_tile.multiplier
                assert left_tile.is_word_multiplier == right_tile.is_word_multiplier

        # Test vertical symmetry
        for row in range(15):
            for col in range(15):
                top_tile = empty_board.get(row, col)
                bottom_tile = empty_board.get(14 - row, col)
                assert top_tile.multiplier == bottom_tile.multiplier
                assert top_tile.is_word_multiplier == bottom_tile.is_word_multiplier

    def test_board_double_letter_scores_exist(self, empty_board):
        """Test that double letter scores exist on board"""
        found_2l = False
        for row in range(15):
            for col in range(15):
                tile = empty_board.get(row, col)
                if tile.multiplier == 2 and not tile.is_word_multiplier:
                    found_2l = True
                    break
            if found_2l:
                break
        assert found_2l, "Board should have double letter scores"

    def test_board_triple_letter_scores_exist(self, empty_board):
        """Test that triple letter scores exist on board"""
        found_3l = False
        for row in range(15):
            for col in range(15):
                tile = empty_board.get(row, col)
                if tile.multiplier == 3 and not tile.is_word_multiplier:
                    found_3l = True
                    break
            if found_3l:
                break
        assert found_3l, "Board should have triple letter scores"

    def test_board_display_no_error(self, empty_board):
        """Test that display doesn't raise errors"""
        # Just make sure it doesn't crash
        empty_board.display()

        # Place some letters and display again
        empty_board.place(7, 7, "h")
        empty_board.place(7, 8, "i")
        empty_board.display()
