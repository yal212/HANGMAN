import json
import random
import hangman
import utilities

with open ("words.txt", "r") as f:    # load words.txt into words
    words = json.load(f)

played = False    # if the player played the game already

while True:

    if not played:
        response = input("Type 'start' to start the game!\n\n")    # response to start the game
    elif played:
        response = input("Type 'play again' to start the game!\n\n")    # response to play again 
    utilities.endl()

    if (not played and response.lower() == "start") or (played and response.lower() == "play again"):    # make sure response is correct in both situation
        
        played = True
        word = random.choice(words).lower()    # pick a random word
        guessed = list()    # keep track of the players guesses
        l = len(word)
        hidden_word = ['_'] * l    # player's word so far
        correct_guesses = 0    # the count of characters guessed that matches the correct word
        wrong_guesses = 0    # the count of characters guessed that doesn't match the correct word
        correct = False    # if the player correctly guessed the word
        wrong = False    # if the player ran out of guesses

        while not correct and not wrong:    # loop when haven't guessed the correct word or haven't run out of guesses

            hangman.print_hangman(wrong_guesses)    # generate hangman text image
            print("\n", *hidden_word, "\n")    # print current status of the player's word
            guess = input("3nter your guess below:\n(your guess should be a character only :)\n\n")    # input guess
            utilities.endl()
            
            while not utilities.validguess(guess):    # make sure the guess is valid
                guess = input("Please enter only a single alphabet!\n\n")
                utilities.endl()

            while guess in guessed:
                temp_char = guess
                guess = input(f"You have already guessed the character {temp_char}, please enter another character!\n\n")
                utilities.endl()

            guessed.append(guess)
            guessed.sort()

            correct_guess = False

            for i in range(l):    # check if guess is in the correct word
                if guess == word[i]:
                    hidden_word[i] = guess
                    correct_guess = True
                    correct_guesses += 1
            
            if not correct_guess:
                wrong_guesses += 1

            if correct_guesses == l:    # checks if the player correctly guessed the word or ran out of guesses
                correct = True
            if wrong_guesses == 6:
                wrong = True

        if correct:    # print the message of result
            utilities.congrats_message(word)
            correct = False
        elif wrong:
            utilities.fail_message(word)
            wrong = False
        utilities.endl()

