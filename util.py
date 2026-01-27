import hangman

def is_valid_guess(player_guess):
    if len(player_guess) == 1 and player_guess.isalpha():
        return True
    return False


def congrats_message(word):
    print(f"\nCongratulations! You guessed the word '{word}' correctly!")


def fail_message(word):
    hangman.print_hangman(6)
    print(f"\nSorry, you ran out of tries. The correct word was '{word}'. Better luck next time!")


def endl():
    print("\n")
