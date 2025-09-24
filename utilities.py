import hangman

def validguess(guess):
    if len(guess) == 1 and guess.isalpha():
        return True
    return False


def congrats_message(word):
    print(f"Congratulations! You guessed the word '{word}' correctly!")


def fail_message(word):
    hangman.print_hangman(6)
    print(f"\nSorry, you ran out of tries. The correct word was '{word}'. Better luck next time!")


def endl():
    print("\n")
