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
    def is_word_solved(self) -> bool:
        """Returns True if every letter in the secret word has been guessed"""
        return "_" not in self.display_word

    # --- Methods (actions that change or check state) ---

    def is_valid_chr(self, letter: str) -> bool:
        """Returns True if letter is a alphabet"""
        return len(letter) == 1 and letter.isalpha()

    def is_already_guessed(self, letter: str) -> bool:
        """Returns True if the letter has already been guessed"""
        return letter in self.guessed_chr

    def is_correct_guess(self, letter: str) -> bool:
        """Returns True if the letter is a correct guess"""
        return letter in self.secret_word

    def guess_chr(self, letter: str) -> bool:
        """Adds a letter to guessed_chr, decrements remaining if wrong, updates status if is valid guess"""
        letter.lower()
        if not self.is_valid_chr(letter) or self.is_already_guessed(letter):
            return False
        self.guessed_chr.add(letter)
        if self.is_correct_guess(letter):
            self.remaining_guesses -= 1
        return True

    def has_won(self):
        """Returns True if won"""
        return self.status == "won"

    def has_lost(self):
        """Returns True if lost"""
        return self.status == "lost"


if __name__ == "__main__":
    pass
