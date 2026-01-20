"""Pytest configuration and shared fixtures"""
import pytest
from pathlib import Path
from src.dictionary import Dictionary
from src.board import Board
from src.game import Game
from src.player import Player
from src.tile import TileBag
@pytest.fixture
def test_dictionary():
    """Provides a test dictionary with known words"""
    dict_path = Path(__file__).parent / "fixtures" / "test_dict.txt"
    return Dictionary(dict_path)
@pytest.fixture
def real_dictionary():
    """Provides the real SOWPODS dictionary"""
    dict_path = Path(__file__).parent.parent / "dicts" / "sowpods.txt"
    return Dictionary(dict_path)
@pytest.fixture
def empty_board():
    """Provides a fresh empty board"""
    return Board()
@pytest.fixture
def tile_bag():
    """Provides a fresh tile bag"""
    return TileBag()
@pytest.fixture
def game():
    """Provides a fresh game instance"""
    return Game()
@pytest.fixture
def player():
    """Provides a test player"""
    return Player("TestPlayer")
