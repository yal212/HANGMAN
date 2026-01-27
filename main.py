import json
import random
import hangman
import util

with open ("words.txt", "r") as f:
    words = json.load(f)

played = False

while True:

    if not played:
        response = input("Type 'start' to start the game!\n\n")
    else:
        response = input("Type 'play again' to start the game!\n\n")

    util.endl()

    if (not played and response.lower() == "start") or (played and response.lower() == "play again"):
        
        played = True
        word = random.choice(words).lower()
        guessed = list()
        l = len(word)
        hidden_word = ['_'] * l
        correct_guesses = 0
        wrong_guesses = 0
        correct = False
        wrong = False

        while not correct and not wrong:

            hangman.print_hangman(wrong_guesses)
            print("\n", *hidden_word, "\n")
            guess = input("3nter your guess below:\n(your guess should be a character only :)\n\n")
            util.endl()
            
            while not util.is_valid_guess(guess):
                guess = input("Please enter only a single alphabet!\n\n")
                util.endl()

            while guess in guessed:
                temp_char = guess
                guess = input(f"You have already guessed the character {temp_char}, please enter another character!\n\n")
                util.endl()

            guessed.append(guess)
            guessed.sort()

            correct_guess = False

            for i in range(l):
                if guess == word[i]:
                    hidden_word[i] = guess
                    correct_guess = True
                    correct_guesses += 1
            
            if not correct_guess:
                wrong_guesses += 1

            if correct_guesses == l:
                correct = True
            if wrong_guesses == 6:
                wrong = True

        if correct:
            util.congrats_message(word)
            correct = False
        elif wrong:
            util.fail_message(word)
            wrong = False
        util.endl()
