from dataclasses import dataclass, field
from typing import Literal, Set


@dataclass
class GameState:

    secret_word: str
    remaining_guesses: int = 6
    guessed_chr: Set[str] = field(default_factory=set)
    status: Literal["ongoing", "won", "lost"] = "ongoing"

    # --- Properties (computed, read-only) ---

    @property
    def display_word(self) -> str:
        """Returns the word with unguessed letters hidden, e.g. 'h _ l l o'"""
        return "".join(c if c in self.guessed_chr else "_" for c in self.secret_word)

    @property
    def wrong_guesses(self) -> Set[str]:
        """Returns only the guessed letters that are NOT IN the secret word"""
        return set(list(c for c in self.guessed_chr if c not in self.secret_word))

    @property
    def correct_guesses(self) -> Set[str]:
        """Returns only the guessed letters that are IN the secret word"""
        return set(list(c for c in self.guessed_chr if c in self.secret_word))

    @property
    def is_word_solved(self) -> bool:
        """Returns True if every letter in the secret word has been guessed"""
        return "_" not in self.display_word

    # --- Methods (actions that change or check state) ---

    def guess_chr(self, letter: str) -> None:
        """Adds a letter to guessed_chr, decrements remaining if wrong, updates status"""
        self.guessed_chr.add(letter)

    def is_already_guessed(self, letter: str) -> bool:
        """Returns True if the letter has already been guessed"""
        return letter in self.guessed_chr


if __name__ == "__main__":
    test = GameState("hello")
    print(test)
    print(test.display_word)

    test.guessed_chr.add("h")
    print(test)
    print(test.display_word)

    test.guessed_chr.add("l")
    print(test)
    print(test.display_word)

    test.guessed_chr.add("o")
    print(test)
    print(test.display_word)

    test.guessed_chr.add("a")
    print(test)
    print(test.wrong_guesses)

    test.guessed_chr.add("b")
    print(test)
    print(test.wrong_guesses)

    test.guessed_chr.add("c")
    print(test)
    print(test.wrong_guesses)
