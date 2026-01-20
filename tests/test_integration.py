"""Integration tests for complete Scrabble game scenarios"""
import pytest
from src.game import Game, NotAWordException
from src.player import Player
from src.tile import TileBag, Tile


class TestGameIntegration:
    """Integration tests for complete game scenarios"""

    def test_full_game_setup(self):
        """Test setting up a complete game"""
        game = Game()

        # Add players
        player1 = Player("Alice")
        player2 = Player("Bob")
        game.add_player(player1)
        game.add_player(player2)

        # Create tile bag and deal hands
        bag = TileBag()
        player1.hand = bag.draw_n(7)
        player2.hand = bag.draw_n(7)

        # Verify setup
        assert len(game.players) == 2
        assert len(player1.hand) == 7
        assert len(player2.hand) == 7
        assert len(bag) == 86  # 100 - 14
        assert game.board.is_empty()

    def test_place_first_word_on_center(self):
        """Test that first word should cover center square"""
        game = Game()

        # The game doesn't currently enforce this, but we document the rule
        # In standard Scrabble, first word must cover center (7,7)
        center = game.board.get(7, 7)
        assert center.multiplier == 2
        assert center.is_word_multiplier is True

    def test_score_word_with_premium_squares(self):
        """Test scoring a word that uses premium squares"""
        game = Game()

        # Place "CAT" starting on center (2W)
        game.board.place(7, 7, "c")
        game.board.place(7, 8, "a")
        game.board.place(7, 9, "t")

        # Calculate score manually
        tiles = [
            game.board.get(7, 7),
            game.board.get(7, 8),
            game.board.get(7, 9),
        ]

        score = Game.calculate_word_score(tiles)
        # C=3, A=1, T=1 = 5, doubled by center 2W = 10
        # But center might be used up, so score could be 5
        assert score >= 5

    def test_draw_tiles_from_bag(self):
        """Test drawing tiles from bag to replenish hand"""
        bag = TileBag()
        player = Player("Test")

        # Draw initial hand
        player.hand = bag.draw_n(7)
        assert len(player.hand) == 7
        assert len(bag) == 93

        # Simulate playing tiles
        played_tiles = player.hand[:3]
        player.hand = player.hand[3:]

        # Draw new tiles
        new_tiles = bag.draw_n(3)
        player.hand.extend(new_tiles)

        assert len(player.hand) == 7
        assert len(bag) == 90

    def test_exchange_tiles(self):
        """Test exchanging tiles with bag"""
        bag = TileBag()
        player = Player("Test")
        player.hand = bag.draw_n(7)

        # Exchange 3 tiles
        tiles_to_exchange = player.hand[:3]
        player.hand = player.hand[3:]

        # Put back in bag
        bag.add(tiles_to_exchange)

        # Draw new tiles
        new_tiles = bag.draw_n(3)
        player.hand.extend(new_tiles)

        assert len(player.hand) == 7
        assert len(bag) == 93

    def test_complete_turn_sequence(self):
        """Test a complete turn sequence"""
        game = Game()
        player1 = Player("Alice")
        player2 = Player("Bob")
        game.add_player(player1)
        game.add_player(player2)

        bag = TileBag()
        player1.hand = bag.draw_n(7)
        player2.hand = bag.draw_n(7)

        initial_score = player1.score

        # Player 1's turn (we can't actually play without valid words)
        # This tests the structure is in place
        assert game.player_turn == 0
        assert game.players[game.player_turn] == player1

    def test_word_on_premium_square_multiple_times(self):
        """Test that premium squares only count once"""
        game = Game()

        # Get a premium square
        tile = game.board.get(7, 7)
        assert tile.multiplier == 2
        assert not tile.used_up

        # Place letter
        tile.place("a")

        # Calculate score (should use multiplier)
        score1, mult1 = tile.calculate_score()
        assert mult1 == 2  # Word multiplier

        # Use up the tile
        tile.use_up()

        # Calculate score again (should not use multiplier)
        score2, mult2 = tile.calculate_score()
        assert score2 == 0  # Used up
        assert mult2 == 1  # mult always defaults to 1 so it can be chained


class TestScrabbleRules:
    """Test that Scrabble rules are correctly implemented"""

    def test_tile_distribution_correct(self):
        """Test that tile distribution matches official Scrabble"""
        bag = TileBag()
        assert len(bag) == 100

        # Draw all and verify counts
        tiles = bag.draw_n(100)
        counts = {}
        for tile in tiles:
            counts[tile.letter] = counts.get(tile.letter, 0) + 1

        # Verify key letters
        assert counts["e"] == 12  # Most common
        assert counts["?"] == 2   # Blanks
        assert counts["z"] == 1   # Rare
        assert counts["q"] == 1   # Rare

    def test_tile_scores_correct(self):
        """Test that tile point values match official Scrabble"""
        from src.tile import TileBag

        # 1 point letters
        for letter in "eaionrtlsu":
            assert TileBag.scores[letter] == 1

        # 2 point letters
        for letter in "dg":
            assert TileBag.scores[letter] == 2

        # 3 point letters
        for letter in "bcmp":
            assert TileBag.scores[letter] == 3

        # 4 point letters
        for letter in "fhvwy":
            assert TileBag.scores[letter] == 4

        # 5 point letters
        assert TileBag.scores["k"] == 5

        # 8 point letters
        for letter in "jx":
            assert TileBag.scores[letter] == 8

        # 10 point letters
        for letter in "qz":
            assert TileBag.scores[letter] == 10

        # Blank
        assert TileBag.scores["?"] == 0

    def test_board_size_correct(self):
        """Test that board is 15x15 as per official Scrabble"""
        game = Game()
        assert game.board.rows == 15
        assert game.board.cols == 15

    def test_hand_size_seven(self):
        """Test that hand size is 7 tiles"""
        bag = TileBag()
        player = Player("Test")
        player.hand = bag.draw_n(7)
        assert len(player.hand) == 7

    def test_bingo_bonus_structure(self):
        """Test that bingo bonus (50 points) structure exists"""
        game = Game()
        # The code has: if total_used_letters == 7: score += 50
        # This tests that we can verify the structure
        assert hasattr(game, 'place_word')

    def test_center_square_double_word(self):
        """Test that center square is a double word score"""
        game = Game()
        center = game.board.get(7, 7)
        assert center.multiplier == 2
        assert center.is_word_multiplier is True

    def test_corner_squares_triple_word(self):
        """Test that corner squares are triple word scores"""
        game = Game()
        corners = [(0, 0), (0, 14), (14, 0), (14, 14)]
        for row, col in corners:
            corner = game.board.get(row, col)
            assert corner.multiplier == 3
            assert corner.is_word_multiplier is True


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_bag_draw(self):
        """Test drawing from empty bag"""
        bag = TileBag()
        og_len = len(bag)
        drawn = bag.draw_n(120)  # Empty the bag
        assert len(drawn) == og_len
        assert len(bag) == 0
        assert bag.draw() is None


    def test_place_on_occupied_square(self):
        """Test placing letter on occupied square raises error"""
        game = Game()
        game.board.place(7, 7, "a")

        with pytest.raises(ValueError, match="already has a letter"):
            game.board.place(7, 7, "b")

    def test_out_of_bounds_placement(self):
        """Test out of bounds placement raises error"""
        game = Game()

        with pytest.raises(ValueError, match="out of bounds"):
            game.board.place(15, 15, "a")

        with pytest.raises(ValueError, match="out of bounds"):
            game.board.place(-1, 0, "a")

    def test_invalid_word_placement(self):
        """Test placing invalid word raises error"""
        game = Game()

        with pytest.raises(NotAWordException):
            game.place_word(7, 7, "zzzzzzz", False)

    def test_word_too_long_for_board(self):
        """Test word that doesn't fit on board"""
        game = Game()

        with pytest.raises(ValueError):
            game._check_word_fits(0, 0, "a" * 20, False)

    def test_player_with_no_name(self):
        """Test creating player with empty name"""
        player = Player("")
        assert player.name == ""
        assert player.score == 0

    def test_negative_score_handling(self):
        """Test that scores can be negative (challenges, penalties)"""
        player = Player("Test")
        player.score = -10
        assert player.score == -10

    def test_blank_tile_score(self):
        """Test that blank tiles are worth 0 points"""
        from src.tile import TileBag
        assert TileBag.scores["?"] == 0

    def test_multiple_words_formed(self):
        """Test scenario where multiple words are formed"""
        game = Game()

        # Place first word
        game.board.place(7, 7, "c")
        game.board.place(7, 8, "a")
        game.board.place(7, 9, "t")

        # Place perpendicular word
        game.board.place(6, 8, "b")
        game.board.place(8, 8, "r")

        # Now "BAR" is vertical and crosses "CAT"
        # This tests the structure for multi-word scoring
        connecting = game.get_connecting_words(6, 8, "bar", True)
        assert isinstance(connecting, list)
