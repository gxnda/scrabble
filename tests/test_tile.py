"""Tests for Tile, TileBag, and BoardTile classes"""
import pytest
from src.tile import Tile, TileBag, BoardTile


class TestTile:
    """Test basic Tile functionality"""

    def test_tile_creation_empty(self):
        """Test creating an empty tile"""
        tile = Tile()
        assert tile.letter == ""
        assert str(tile) == " "
        assert not tile  # Empty tile is falsy

    def test_tile_creation_with_letter(self):
        """Test creating a tile with a letter"""
        tile = Tile("a")
        assert tile.letter == "a"
        assert str(tile) == "a"
        assert tile  # Non-empty tile is truthy

    def test_tile_blank(self):
        """Test blank tile represented by '?'"""
        tile = Tile("?")
        assert tile.letter == "?"
        assert tile  # Blank tile is truthy

    def test_tile_bool_none(self):
        """Test tile with None is falsy"""
        tile = Tile(None)
        assert not tile


class TestTileBag:
    """Test TileBag functionality"""

    def test_tile_bag_total_count(self):
        """Test that tile bag has exactly 100 tiles"""
        bag = TileBag()
        assert len(bag) == 100

    def test_tile_bag_distribution(self):
        """Test that tile bag has correct distribution"""
        bag = TileBag()
        # Draw all tiles and count them
        tiles = bag.draw_n(100)
        counts = {}
        for tile in tiles:
            letter = tile.letter
            counts[letter] = counts.get(letter, 0) + 1

        # Verify distribution matches Scrabble rules
        assert counts.get("?", 0) == 2  # 2 blanks
        assert counts.get("e", 0) == 12
        assert counts.get("a", 0) == 9
        assert counts.get("i", 0) == 9
        assert counts.get("o", 0) == 8
        assert counts.get("n", 0) == 6
        assert counts.get("r", 0) == 6
        assert counts.get("t", 0) == 6
        assert counts.get("l", 0) == 4
        assert counts.get("s", 0) == 4
        assert counts.get("u", 0) == 4
        assert counts.get("d", 0) == 4
        assert counts.get("g", 0) == 3
        assert counts.get("k", 0) == 1
        assert counts.get("j", 0) == 1
        assert counts.get("x", 0) == 1
        assert counts.get("q", 0) == 1
        assert counts.get("z", 0) == 1

    def test_tile_bag_draw(self):
        """Test drawing a single tile"""
        bag = TileBag()
        initial_count = len(bag)
        tile = bag.draw()
        assert isinstance(tile, Tile)
        assert len(bag) == initial_count - 1

    def test_tile_bag_draw_n(self):
        """Test drawing multiple tiles"""
        bag = TileBag()
        tiles = bag.draw_n(7)
        assert len(tiles) == 7
        assert len(bag) == 93  # 100 - 7
        assert all(isinstance(tile, Tile) for tile in tiles)

    def test_tile_bag_add_single(self):
        """Test adding a single tile back to bag"""
        bag = TileBag()
        bag.draw_n(5)
        tile = Tile("a")
        bag.add(tile)
        assert len(bag) == 96  # 100 - 5 + 1

    def test_tile_bag_add_multiple(self):
        """Test adding multiple tiles back to bag"""
        bag = TileBag()
        tiles_drawn = bag.draw_n(7)
        bag.add(tiles_drawn)
        assert len(bag) == 100

    def test_tile_scores(self):
        """Test that tile scores match Scrabble rules"""
        assert TileBag.scores["?"] == 0
        assert TileBag.scores["e"] == 1
        assert TileBag.scores["a"] == 1
        assert TileBag.scores["d"] == 2
        assert TileBag.scores["g"] == 2
        assert TileBag.scores["b"] == 3
        assert TileBag.scores["c"] == 3
        assert TileBag.scores["f"] == 4
        assert TileBag.scores["k"] == 5
        assert TileBag.scores["j"] == 8
        assert TileBag.scores["x"] == 8
        assert TileBag.scores["q"] == 10
        assert TileBag.scores["z"] == 10


class TestBoardTile:
    """Test BoardTile functionality"""

    def test_board_tile_creation_normal(self):
        """Test creating a normal board tile"""
        tile = BoardTile()
        assert tile.multiplier == 1
        assert tile.is_word_multiplier is False
        assert tile.used_up is False
        assert tile.is_empty()

    def test_board_tile_creation_with_multipliers(self):
        """Test creating board tile with multipliers"""
        tile = BoardTile(multiplier=2, is_word_multiplier=False)
        assert tile.multiplier == 2
        assert tile.is_word_multiplier is False

        tile2 = BoardTile(multiplier=3, is_word_multiplier=True)
        assert tile2.multiplier == 3
        assert tile2.is_word_multiplier is True

    def test_board_tile_is_empty(self):
        """Test is_empty method"""
        tile = BoardTile()
        assert tile.is_empty()
        tile.place("a")
        assert not tile.is_empty()

    def test_board_tile_clear(self):
        """Test clearing a board tile"""
        tile = BoardTile()
        tile.letter = "a"
        tile.clear()
        assert tile.is_empty()
        assert tile.letter == ""

    def test_board_tile_place_string(self):
        """Test placing a string on a board tile"""
        tile = BoardTile()
        tile.place("x")
        assert tile.letter == "x"
        assert not tile.is_empty()

    def test_board_tile_place_tile(self):
        """Test placing a Tile object on a board tile"""
        tile = BoardTile()
        letter_tile = Tile("y")
        tile.place(letter_tile)
        assert tile.letter == "y"

    def test_board_tile_place_on_occupied(self):
        """Test that placing on occupied tile raises error"""
        tile = BoardTile()
        tile.place("a")
        with pytest.raises(ValueError, match="already has a letter"):
            tile.place("b")

    def test_board_tile_use_up(self):
        """Test using up multiplier"""
        tile = BoardTile(multiplier=2)
        assert not tile.used_up
        tile.use_up()
        assert tile.used_up

    def test_board_tile_quick_create_letter_multiplier(self):
        """Test quick_create with letter multipliers"""
        tile = BoardTile.quick_create("2L")
        assert tile.multiplier == 2
        assert tile.is_word_multiplier is False

        tile = BoardTile.quick_create("3L")
        assert tile.multiplier == 3
        assert tile.is_word_multiplier is False

    def test_board_tile_quick_create_word_multiplier(self):
        """Test quick_create with word multipliers"""
        tile = BoardTile.quick_create("2W")
        assert tile.multiplier == 2
        assert tile.is_word_multiplier is True

        tile = BoardTile.quick_create("3W")
        assert tile.multiplier == 3
        assert tile.is_word_multiplier is True

    def test_board_tile_quick_create_normal(self):
        """Test quick_create with normal tile"""
        tile = BoardTile.quick_create("1")
        assert tile.multiplier == 1
        assert tile.is_word_multiplier is False

    def test_board_tile_calculate_score_empty(self):
        """Test score calculation for empty tile"""
        tile = BoardTile()
        score, mult = tile.calculate_score()
        assert score == 0
        assert mult == 1  # Neutral multiplier

    def test_board_tile_calculate_score_used_up(self):
        """Test score calculation for used up tile"""
        tile = BoardTile(multiplier=2)
        tile.place("a")
        tile.use_up()
        score, mult = tile.calculate_score()
        assert score == 0
        assert mult == 1  # Neutral multiplier

    def test_board_tile_calculate_score_letter_multiplier(self):
        """Test score calculation with letter multiplier"""
        tile = BoardTile(multiplier=2, is_word_multiplier=False)
        tile.place("a")  # 'a' is worth 1 point
        score, mult = tile.calculate_score()
        assert score == 2  # 1 * 2
        assert mult == 1

        tile2 = BoardTile(multiplier=3, is_word_multiplier=False)
        tile2.place("d")  # 'd' is worth 2 points
        score, mult = tile2.calculate_score()
        assert score == 6  # 2 * 3
        assert mult == 1

    def test_board_tile_calculate_score_word_multiplier(self):
        """Test score calculation with word multiplier"""
        tile = BoardTile(multiplier=2, is_word_multiplier=True)
        tile.place("a")  # 'a' is worth 1 point
        score, mult = tile.calculate_score()
        assert score == 1  # Letter score not multiplied
        assert mult == 2  # Word multiplier returned

        tile2 = BoardTile(multiplier=3, is_word_multiplier=True)
        tile2.place("q")  # 'q' is worth 10 points
        score, mult = tile2.calculate_score()
        assert score == 10
        assert mult == 3
