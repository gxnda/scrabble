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

## Test Coverage

The test suite covers:

### Scrabble Rules Implementation
- ✅ 100 tiles with correct distribution
- ✅ Correct point values for all letters
- ✅ 15x15 board size
- ✅ Premium squares (2L, 3L, 2W, 3W)
- ✅ Center square is double word score
- ✅ Corner squares are triple word scores
- ✅ Board is symmetric
- ✅ Hand size of 7 tiles
- ✅ 50-point bingo bonus for using all 7 tiles
- ✅ Blank tiles worth 0 points
- ✅ Word validation against dictionary
- ✅ Multipliers only count once per turn

### Core Functionality
- ✅ Tile bag draw and shuffle
- ✅ Board tile placement
- ✅ Score calculation with multipliers
- ✅ Word overlap detection
- ✅ Connected word finding
- ✅ Turn management
- ✅ Player score tracking

### Edge Cases
- ✅ Out of bounds placement
- ✅ Empty tile bag
- ✅ Occupied square placement
- ✅ Invalid word placement
- ✅ Word too long for board
- ✅ Negative scores
- ✅ Multiple simultaneous words

## Known Issues / TODOs

1. **Word Placement** - The `place_word()` method doesn't actually place letters on the board or update player hands/scores
2. **First Move Validation** - No enforcement that first word must cover center square (7,7)
3. **Word Connectivity** - No validation that subsequent words must connect to existing words
4. **Turn Management** - Turn increment logic exists but isn't called after word placement

## Bug Fixes Applied

During test development, the following bugs were discovered and fixed:

1. **BoardTile.place()** - Fixed logic to check if tile is empty before placing
2. **BoardTile.calculate_score()** - Fixed to return neutral multiplier (1) instead of 0 for used up tiles
3. **Board._create_empty_board()** - Fixed to use absolute path for blankboard.txt
4. **Game.__find_connected()** - Fixed index calculation for finding connected words
5. **Game._check_word_fits()** - Fixed error message to show correct position

## Contributing

When adding new tests:
1. Follow the existing test structure
2. Use descriptive test names starting with `test_`
3. Add docstrings explaining what is being tested
4. Use fixtures from conftest.py when appropriate
5. Group related tests in classes
6. Test both success and failure cases

