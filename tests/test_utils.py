from _pytest.monkeypatch import monkeypatch
import pytest
from utils import select_random_word

def test_returns_words_from_list():
    words = ["python", "java", "cpp", "go", "rust"]
    word = select_random_word(words)
    assert word in words

def test_returns_lowercase():
    words = ["PYTHON", "JAVA", "CPP", "GO", "RUST"]
    word = select_random_word(words)
    assert word.islower()

def test_loads_default_list(tmp_path, monkeypatch):
    temp_file = tmp_path / "words.txt"
    temp_file.write_text('["python", "java", "cpp", "go", "rust"]')
    monkeypatch.chdir(tmp_path)
    word = select_random_word()
    assert word in ["python", "java", "cpp", "go", "rust"]
