import sys
from random import choice
import re
from hangman_pics import HANGMANPICS

def main():
    # Print instructions
    print(*get_instructions(), sep="\n")

    
    # Select a word from words.txt file in data
    # Open the words.txt file and read the lines into a list
    try:
        with open(".\data\words.txt") as file:
            words = file.readlines()
    except FileNotFoundError:
        sys.exit("File does not exist")
    
    # Choose a word
    word = choice(words).strip()

    # REMOVE WHEN FINISHED TESTING
    print(word)

    # Initialize guess_counter and score
    guess_counter = 0
    score = 0

    # Display one "_" for each letter in the word
    word_scheme = []
    for _ in word:
        word_scheme.append("_")

    # Guesses loop
    while (score < 6):
        # Display the initial hangman structure 
        print(HANGMANPICS[score], " ",  *word_scheme)

        # Check to see if the user won
        if "_" not in word_scheme:
            sys.exit("You won! :)")

        # Ask for a guess from the user
        guess = get_guess()

        # Evaluate the guess
        if guess in word:
            print("The guessed letter is in the word")
            # Find the indexes of the first char of the substrings that start with the guessed letter, 
            # Returns a list of all the indexes
            indexes = [i for i in range(len(word)) if word.startswith(guess, i)] 
            for i in indexes:
                word_scheme[i] = guess.upper()
        else:
            score += 1
        
        guess_counter += 1

        print("End of guess: ", guess_counter, "Current score: ", score)

    # If they guess and loose
    print(HANGMANPICS[score], *word_scheme)
    sys.exit("You lost! :(")

def get_instructions():
    instructions = []
    instructions.append("Welcome to Musical Hangman!")
    instructions.append("A random English word will be selected and you have to guess it.")
    instructions.append("You have 6 guesses in total, represented by the human in the hangman noose.")
    instructions.append("When the hanged human is completed, you loose.")
    return instructions

def get_guess():
    guess = input("Guess: ").strip().lower()
    while re.fullmatch(r"^[a-z]$", guess) is None:
        print("Please, guess a single letter.")
        guess = input("Guess: ").strip().lower()
    return guess


if __name__ == "__main__":
    main()