import sys
from random import choice
import re
from hangman_pics import HANGMANPICS

class Hangman:
    def __init__(self):
        self.score = 0
        self.wrong_guess = []
        self.right_guess = []
        self.word_scheme = []

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, score):
        self._score = score

    @property
    def wrong_guess(self):
        return self._wrong_guess
    
    @wrong_guess.setter
    def wrong_guess(self, wrong_guess):
        self._wrong_guess = wrong_guess
    
    @property
    def right_guess(self):
        return self._right_guess
    
    @right_guess.setter
    def right_guess(self, right_guess):
        self._right_guess = right_guess

    @property
    def word_scheme(self):
        return self._word_scheme
    
    @word_scheme.setter
    def word_scheme(self, word_scheme):
        self._word_scheme = word_scheme
    

    def select_word(self):
        # Select a word from words.txt file in data
        # Open the words.txt file and read the lines into a list
        try:
            with open(".\data\words.txt") as file:
                words = file.readlines()
        except FileNotFoundError:
            sys.exit("File does not exist")
        
        # Choose a word
        word = choice(words).strip()

        # Build the word_scheme
        self.build_word_scheme(word)
        return word
    
    def build_word_scheme(self, word):
        # Display one "_" for each letter in the word
        for _ in word:
            self.word_scheme.append("_")

def main():

    hangman = Hangman()

    # Print instructions
    print(*get_instructions(), sep="\n")
   
    # Choose a word
    word = hangman.select_word()

    # REMOVE WHEN FINISHED TESTING
    print(word)

    # Guesses loop
    while (hangman.score < 6):
        # Display the initial hangman structure 
        print(HANGMANPICS[hangman.score], " ",  *hangman.word_scheme, "   Guessed:", *hangman.wrong_guess)

        # Check to see if the user won
        if "_" not in hangman.word_scheme:
            sys.exit("You won! :)")

        # Ask for a guess from the user
        guess = get_guess(hangman.wrong_guess, hangman.right_guess)

        # Evaluate the guess
        if guess in word:
            print("The guessed letter is in the word")
            # Find the indexes of the first char of the substrings that start with the guessed letter, 
            # Returns a list of all the indexes
            indexes = [i for i in range(len(word)) if word.startswith(guess, i)] 
            for i in indexes:
                hangman.word_scheme[i] = guess.upper()
                hangman.right_guess.append(guess.upper())
        else:
            hangman.score += 1
            hangman.wrong_guess.append(guess.upper())
        

    # If they guess and loose
    print(HANGMANPICS[hangman.score], *hangman.word_scheme)
    sys.exit(f"You lost! :( The word was {word.upper()}")

def get_instructions():
    instructions = []
    instructions.append("Welcome to Musical Hangman!")
    instructions.append("A random English word will be selected and you have to guess it.")
    instructions.append("You have 6 guesses in total, represented by the human in the hangman noose.")
    instructions.append("When the hanged human is completed, you loose.")
    return instructions

def get_guess(wrong_guess, right_guess):
    guess = input("Guess: ").strip().lower()
    while re.fullmatch(r"^[a-z]$", guess) is None:
        print("Please, guess a single letter.")
        guess = input("Guess: ").strip().lower()
    while guess.upper() in wrong_guess or guess.upper() in right_guess:
        print("You already guessed this letter. Please, guess again.")
        guess = input("Guess: ").strip().lower()
    return guess


if __name__ == "__main__":
    main()