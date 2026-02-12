import json
from pathlib import Path


def load_word_list(filepath: str = "words.txt") -> list[str]:
    try:
        with open(filepath, "r") as file:
            words = json.load(file)
        if not isinstance(words, list) or not words:
            raise ValueError(f"File {filepath} must contain a non-empty JSON array.")
        return words
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filepath} does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError(f"File {filepath} contains invalid json: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while loading word list: {e}")
