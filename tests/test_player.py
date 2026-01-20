"""Tests for Player class"""
import pytest
from src.player import Player
from src.tile import Tile


class TestPlayer:
    """Test Player functionality"""

    def test_player_creation(self, player):
        """Test creating a player"""
        assert player.name == "TestPlayer"
        assert player.score == 0
        assert player.hand == []
        assert player.time_remaining_s == 180  # 3 minutes
        assert player.api is None

    def test_player_custom_name(self):
        """Test creating player with custom name"""
        player = Player("Alice")
        assert player.name == "Alice"

    def test_player_score_initialization(self, player):
        """Test player score starts at 0"""
        assert player.score == 0

    def test_player_hand_empty(self, player):
        """Test player hand starts empty"""
        assert len(player.hand) == 0
        assert player.hand == []

    def test_player_hand_add_tiles(self, player):
        """Test adding tiles to player hand"""
        tile1 = Tile("a")
        tile2 = Tile("b")
        player.hand.extend([tile1, tile2])
        assert len(player.hand) == 2
        assert tile1 in player.hand
        assert tile2 in player.hand

    def test_player_hand_max_seven_tiles(self, player):
        """Test that typical Scrabble hand has 7 tiles"""
        tiles = [Tile(letter) for letter in "abcdefg"]
        player.hand = tiles
        assert len(player.hand) == 7

    def test_player_score_update(self, player):
        """Test updating player score"""
        player.score = 25
        assert player.score == 25

        player.score += 10
        assert player.score == 35

    def test_player_time_remaining(self, player):
        """Test time remaining tracking"""
        assert player.time_remaining_s == 180

        player.time_remaining_s -= 30
        assert player.time_remaining_s == 150

    def test_player_assign_bot(self, player, game):
        """Test assigning a bot to player"""
        # Create a mock bot class
        class MockBot:
            def hook(self, game, player):
                self.game = game
                self.player = player

        player.assign_bot(game, MockBot)
        assert player.api is not None
        assert isinstance(player.api, MockBot)

    def test_multiple_players_independent(self):
        """Test that multiple players are independent"""
        player1 = Player("Alice")
        player2 = Player("Bob")

        player1.score = 10
        player2.score = 20

        player1.hand.append(Tile("a"))
        player2.hand.append(Tile("b"))

        assert player1.score != player2.score
        assert player1.hand != player2.hand
        assert player1.name != player2.name
