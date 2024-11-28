import sys
from random import choice
import re
import json
import requests
from hangman_pics import HANGMANPICS

class Hangman:
    def __init__(self):
        self.score = 0
        self.wrong_guess = []
        self.right_guess = []
        self.phrase_scheme = []

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
    def phrase_scheme(self):
        return self._phrase_scheme
    
    @phrase_scheme.setter
    def phrase_scheme(self, phrase_scheme):
        self._phrase_scheme = phrase_scheme
    

    def select_word(self):
        # Select a word from words.txt file in data
        # Open the words.txt file and read the lines into a list
        try:
            with open(".\\data\\words.txt") as file:
                words = file.readlines()
        except FileNotFoundError:
            sys.exit("File does not exist")
        
        # Choose a word
        word = choice(words).strip()

        # Build the phrase_scheme
        self.build_phrase_scheme(word)

        return word
    
    def build_phrase_scheme(self, word):
        # Display one "_" for each letter in the word
        for _ in word:
            self.phrase_scheme.append("_")

    def evaluate_guess(self, word, guess):
        # Evaluate the guess
        if guess in word:
            # Returns a list of all the indexes
            indexes = [i for i in range(len(word)) if word.startswith(guess, i)] 
            for i in indexes:
                self.phrase_scheme[i] = guess.upper()
                self.right_guess.append(guess.upper())
        else:
            self.score += 1
            self.wrong_guess.append(guess.upper())


class Musical_Hangman(Hangman):
    def __init__(self):
        super().__init__()
        self.lyric = ""
        self.lyric_indexes = []
    
    @property
    def lyric(self):
        return self._lyric
    
    @lyric.setter
    def lyric(self, lyric):
        self._lyric = lyric
    
    @property
    def lyric_indexes(self):
        return self._lyric_indexes
    
    @lyric_indexes.setter
    def lyric_indexes(self, lyric_indexes):
        self._lyric_indexes = lyric_indexes

    def select_word(self):
        # Choose a word
        # LYRIST API
        response = requests.get("https://lyrist.vercel.app/api/Chandelier/Sia")
        lyrics = response.json()["lyrics"].split("\n")
        
        # Remove annotations and empty lines from the lyrics list
        lines_to_remove = []
        for line in lyrics:
            if ("[" in line) or (line == ""):
                lines_to_remove.append(line)
        for line in lines_to_remove:
            lyrics.remove(line)

        # Choose a lyric
        self.lyric = choice(lyrics)

        # Separate into a word list
        lyric_words = self.lyric.split(" ")

        word = choice(lyric_words)
        # If it has punctuation, change the word
        while re.search(r"[^a-zA-Z]", word) is not None:
            word = choice(lyric_words)

        self.build_phrase_scheme(word, self.lyric)

        return word

    def build_phrase_scheme(self, word, lyric):
        # Get a list of indexes of the first letter of every occurence of the word in the lyric.
        self.lyric_indexes = [i for i in range(len(lyric)) if self.lyric.startswith(word, i)]
        # Phrase scheme template
        self.phrase_scheme = list(lyric)
        # Switch the chosen word's characters for "_"
        for i in self.lyric_indexes:
            for j in range(len(word)):
                self.phrase_scheme[i + j] = "_"
        return self.phrase_scheme

    def evaluate_guess(self, word, guess):
        # Evaluate the guess
        if guess in word:
            print("The guessed letter is in the word")
            # Find the indexes of the first char of the substrings within the word that start with the guessed letter, 
            # Returns a list of all the indexes
            word_indexes = [i for i in range(len(word)) if word.startswith(guess, i)] 
            for i in self.lyric_indexes:
                for j in word_indexes:
                    self.phrase_scheme[i + j] = guess.upper()
                    self.right_guess.append(guess.upper())
        else:
            self.score += 1
            self.wrong_guess.append(guess.upper())

def main():

    # Ask the user for mode of play
    mode = choose_play_mode()

    # Create an instance of Hangman (mode == A) or Musical_Hangman (mode == B) class
    if mode == "A":
        hangman = Hangman()
    else:
        hangman = Musical_Hangman()

    # Print instructions
    print(*get_instructions(mode), sep="\n")

    # Choose a word
    word = hangman.select_word()
    
    # Guesses loop
    while (hangman.score < 6):
        # Display the initial hangman structure 
        print(HANGMANPICS[hangman.score], " ",  *hangman.phrase_scheme)
        print("Already guessed:", *hangman.wrong_guess)

        # Check to see if the user won
        if "_" not in hangman.phrase_scheme:
            sys.exit("You won! :)")

        # Ask for a guess from the user
        guess = get_guess(hangman.wrong_guess, hangman.right_guess)

        # Evaluate the guess
        hangman.evaluate_guess(word, guess)
        

    # If they guessed 6 times and lose
    print(HANGMANPICS[hangman.score], *hangman.phrase_scheme)

    print(get_lose_message())
    


def choose_play_mode():
    print("Hi! Welcome to Musical Hangman!")
    print("Please choose between our two modes by typing A or B:")
    print("A) Tradicional Hangman")
    print("B) Musical Hangman")
    mode = input("Mode: ")
    while re.fullmatch(r"^[abAB]$", mode) is None:
        print("Please type A or B.")
        mode = input("Mode: ")
    return mode.upper()

# Move to class?
def get_instructions(mode):
    instructions = []
    if mode == "A":
        instructions.append("Welcome to traditional Hangman!")
        instructions.append("A random English word will be selected and you have to guess it.")
        instructions.append("You have 6 guesses in total, represented by the human in the hangman noose.")
        instructions.append("When the hanged human is completed, you loose.")
    else:
        instructions.append("Welcome to musical Hangman!")
        instructions.append("A random word from a lyric will be selected and you have to guess it.")
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

def get_lose_message(word, mode, lyric=None):
    message = []
    message.append(f"You lost! :( The word was {word.upper()}")
    if mode == "B":
        message.append("The complete lyric is:")
        message.append(lyric)
        message.append("From the song Chandelier by Sia")
        message.append("Spotify link: ")
    

if __name__ == "__main__":
    main()