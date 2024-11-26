import sys
from random import choice

HANGMANPICS = ['''
  +---+
  |   |
  |
  |
  |
  |
=========''', '''
  +---+
  |   |
  |   O
  |
  |
  |
=========''', '''
  +---+
  |   |
  |   O
  |   |
  |
  |
=========''', '''
  +---+
  |   |
  |   O
  |  /|
  |   
  |
  |
=========''', '''
  +---+
  |   |
  |   O
  |  /|\\
  |  
  |
=========''', '''
  +---+
  |   |
  |   O
  |  /|\\
  |  / 
  |
=========''', '''
  +---+
  |   |
  |   O
  |  /|\\
  |  / \\ 
  |
=========''']

def main():
    # Print instructions
    print("Welcome to Musical Hangman!")
    print("A random English word will be selected and you have to guess it.")
    print("You have X guesses in total, represented by the human in the hangman noose.")
    print("When the hanged human is completed, you loose.")

    
    # Select a word from words.txt file in data
    try:
        with open(".\data\words.txt") as file:
            words = file.readlines()
    except FileNotFoundError:
        sys.exit("File does not exist")

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

    while (score < 6):
        # Display the initial hangman structure 
        print(HANGMANPICS[score], *word_scheme)

        if "_" not in word_scheme:
            sys.exit("You won! :)")

        # Ask for a guess from the user
        guess = input("Guess: ").strip().lower()

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

        # Print the updated board
        # Repeat until win or lose
    print(HANGMANPICS[score], *word_scheme)
    sys.exit("You lost! :(")

if __name__ == "__main__":
    main()