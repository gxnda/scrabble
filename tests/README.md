# Scrabble Test Suite

This directory contains a comprehensive test suite for the Scrabble implementation using pytest.

## Test Structure

### Test Files

- **`test_tile.py`** - Tests for Tile, TileBag, and BoardTile classes
  - Tile creation and behavior
  - Tile bag distribution (100 tiles with correct Scrabble distribution)
  - Tile scoring values
  - Board tile multipliers (2L, 3L, 2W, 3W)
  - Score calculation with multipliers

- **`test_board.py`** - Tests for Board class
  - 15x15 board creation from blankboard.txt
  - Premium square placement (center 2W, corner 3W, etc.)
  - Board symmetry verification
  - Tile placement and retrieval
  - Bounds checking

- **`test_dictionary.py`** - Tests for Dictionary class
  - Dictionary loading from file
  - Case-insensitive word lookup
  - SOWPODS dictionary validation

- **`test_player.py`** - Tests for Player class
  - Player creation and initialization
  - Score tracking
  - Hand management (7 tiles)
  - Time tracking
  - Bot assignment

- **`test_game.py`** - Tests for Game class
  - Game initialization
  - Player management
  - Word scoring with multipliers
  - Word placement validation
  - Overlapping word detection
  - Connected word finding
  - Bingo bonus (50 points for using all 7 tiles)

- **`test_integration.py`** - Integration and end-to-end tests
  - Complete game setup
  - Tile distribution according to Scrabble rules
  - Premium square validation
  - Edge cases and error handling
  - Scrabble rules compliance

### Fixtures (`conftest.py`)

Shared pytest fixtures for all tests:
- `test_dictionary` - Small test dictionary with known words
- `real_dictionary` - Full SOWPODS dictionary
- `empty_board` - Fresh 15x15 board
- `tile_bag` - Fresh tile bag with 100 tiles
- `game` - New game instance
- `player` - Test player

### Test Dictionary (`fixtures/test_dict.txt`)

Small dictionary file with known words for predictable testing.

## Running Tests

### Run all tests
```bash
python -m pytest tests/
```

### Run with verbose output
```bash
python -m pytest tests/ -v
```

### Run specific test file
```bash
python -m pytest tests/test_tile.py -v
```

### Run specific test class
```bash
python -m pytest tests/test_tile.py::TestTileBag -v
```

### Run specific test
```bash
python -m pytest tests/test_tile.py::TestTileBag::test_tile_bag_distribution -v
```

### Run with coverage
```bash
python -m pytest tests/ --cov=src --cov-report=html
```
