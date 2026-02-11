import json

def load_word_list():
    with open ("words.txt", "r") as f:
        return json.load(f)
