# Scramble API Documentation

U dont get a contents section

## Making A Bot

### Creation

To start, import the Api Module from api.py and create a new class inheriting from Api

```python
from api import Api  # Likely different for you

class MyBot(Api):
  def __init__(self):
    super().__init__()
```

You should note that in the ```__init__``` method, you cant read any game or player data as it has not yet been created.

---

### Overrides

You have two methods you can override to create your bot. ```_init``` and ```_on_turn```


```python
class MyBot(Api):
  def __init__(self):
    super().__init__()

  def _init(self):
    """ Here you can init your bot, data from the board is now available """
    pass

  def _on_turn(self):
    """ This is called when its your bots turn. The time taken for this method to run is measured.  """
    pass
```

---

### Actions

Every turn, your bot must completle one of three actions. When a action is called / executed, your turn ends imediatly.

#### Place Word
Allows you to place a word on the board. Note, if this move is illegal an exception will be raised and your bot will lose.

```python
  def place_word(word: str, is_vertical: bool, x: int, y: int):
    """
    The x/y coords are the location of the first character in the word.
    The word must connect with at least one other word.
    """
    ...
```

#### Exchanging / Discarding Letters
Allows you to spend your turn exchanging between 1 and 7 letters and get new, random letters (for next turn)

```python
  def discard_letters(letters: list[str]):
    """
    The letters in this list must be in your hand or else an error will be raised.
    You can discard multiple of the same letter by having multiple of them in the list.
    """
    ...
```

#### Passing / No Action
Allows you to skip your turn without doing anything

```python
  def pass_turn(self):
    """ Ends your turn instantly """
    ...
```

---

### Additional Methods & Attributes
Your handy dandy Api has some more in-store for you ;)

#### Checking Moves

```python
  def check_placement(self, word: str, is_vertical: bool, x: int, y: int) -> bool:
    """ Returns a blanket True/False value for if the move is legal """
    ...
```

#### Getting Games Dictionary

```python
  def get_dictionary(self) -> Dictionary:
    """ Returns a dictionary of all valid words in play """
    ...

```

#### Getting Current Letters / Hand

```python
  def get_tiles_in_hand(self) -> list[str]:
    """ Returns a list of letters that make up your hand """
    ...

```

#### Board Attributes

```Api.board_size: list[row: int, col: int]```

```Api.board: list[list[BoardTile]]```
