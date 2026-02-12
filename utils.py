import random
from words import load_word_list

def select_random_word(words: list[str] | None = None) -> str:
    if not words:
        words = load_word_list()
    elif not isinstance(words, list) or not words:
        raise ValueError(f"`words` must be a non-empty list.")
    return random.choice(words).lower()
