HANGMAN = [
    r"""  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
========="""
]


def print_hangman(stage):
    stage = max(0, min(stage, len(HANGMAN)-1))
    print(HANGMAN[stage])

# example:
# print_hangman(3)
