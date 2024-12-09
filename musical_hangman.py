import sys
from random import choice
import re
import requests
import csv
from hangman_pics import HANGMANPICS
from simple_colors import *

class Hangman:
    def __init__(self):
        self.score = 0
        self.wrong_guess = []
        self.right_guess = []
        self.phrase_scheme = []
        self.instructions = [
            "",
            cyan("You chose traditional Hangman!"),
            "",
            "Here a random English word will be selected and you have to guess it.",
            "You have 6 guesses in total, represented by the human in the hangman noose.",
            "When the hanged human is completed, you loose.",
            "",

        ]

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

    def get_end_message(self, outcome, word):
        message = []
        message.append(get_win_lose(outcome))
        message.append(cyan(f"The word was {word.upper()}"))
        message.append("You can check out the definition at https://www.merriam-webster.com/dictionary/" + word)
        message.append("")
        return message

class Musical_Hangman(Hangman):
    def __init__(self):
        super().__init__()
        self.song = {}
        self.lyric = ""
        self.lyric_indexes = []
        self.instructions = [
            "",
            yellow("You chose Musical Hangman!"),
            "",
            "A random word from a lyric will be selected and you have to guess it.",
            "You have 6 guesses in total, represented by the human in the hangman noose.",
            "When the hanged human is completed, you loose.",
            "", 
        ]
    
    @property
    def song(self):
        return self._song
    
    @song.setter
    def song(self, song):
        self._song = song
   
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
        # 1. User chooses a genre
        category = self.choose_category()

        # 2. Choose a random song from that file
        self.get_random_song(category)
        print(self.song)

        # 3. Get the lyrics from LYRIST API
        lyrics = self.get_lyrics(self.song)
        
        # 4. Choose a lyric
        self.lyric = choice(lyrics)

        # 5. Separate into a word list
        lyric_words = self.lyric.split(" ")

        # 6. Choose a random valid (without punctuation) word
        word = choice(lyric_words)
        # If it has punctuation, change the word
        while re.search(r"[^a-zA-Z]", word) is not None:
            word = choice(lyric_words)

        self.build_phrase_scheme(word, self.lyric)

        return word
    
    def choose_category(self):
        print(yellow("Please, pick a category by typing 1, 2, 3 or 4:"))
        print("     1. Best of the 80s")
        print("     2. 2000s Pop")
        print("     3. 2000s Rock")
        print("     4. Best of all time")
        category = input("Category: ")
        while re.fullmatch(r"[1-4]", category) is None:
            print(red("Please type a number between 1 and 4."))
            category = input("Category: ")
        return category
    
    def get_random_song(self, category):
        match category:
            case "1":
                path = ".\\data\\80ssongs.csv"
            case "2":
                path = ".\\data\\2000spopsongs.csv"
            case "3":
                path = ".\\data\\80ssongs.csv"
            case "4":
                path = ".\\data\\bestsongs.csv"
            case _:
                # Leave the path for best of all time
                path = ".\\data\\bestsongs.csv"

        songs = []
        try:
            with open(path) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    songs.append({"song": row["song"], "artist": row["artist"]})
        except FileNotFoundError:
            sys.exit("File does not exist")

        self.song = choice(songs)
        return self.song
    
    def get_lyrics(self, song):
        # Get the lyrics from LYRIST API
        response = requests.get("https://lyrist.vercel.app/api/" + song["song"].replace(" ", "_") + "/" + song["artist"].replace(" ", "_"))
        # Get a list of the individual lines of lyrics
        lyrics = response.json()["lyrics"].split("\n")
        
        # Remove annotations and empty lines from the lyrics list
        lines_to_remove = []
        for line in lyrics:
            if ("[" in line) or (line == ""):
                lines_to_remove.append(line)
        for line in lines_to_remove:
            lyrics.remove(line)

        return lyrics

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

    def get_end_message(self, outcome, word):
        message = []
        message.append(get_win_lose(outcome))
        message.append(yellow(f"The word was {word.upper()}"))
        message.append("")
        message.append("The complete lyric is:")
        message.append(green(self.lyric, "italic"))
        message.append(f"From the song {self.song["song"].upper()} by {self.song["artist"].upper()}")
        message.append("")
        message.append("Listen here: " + blue(self.get_spotify_track_url(), "underlined"))
        message.append("")
        return message
    
    def get_spotify_track_url(self):
        # Get access token
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": "c9b115e0664d451394c2b4121968154d",
            "client_secret": "4550ec5a054f413db26143ee8b485706"
        }
    
        # Make the POST request
        response = requests.post(url, headers=headers, data=data)
    
        # Check if the request was successful
        if response.status_code == 200:
            # print("Success!")
            # print(response.json())  # Print the response body as JSON
            access_token = response.json()["access_token"]
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)  # Print the response body

        search_url = f"https://api.spotify.com/v1/search?q=remaster%2520track%3A{self.song["song"].replace(" ", "%2520")}%2520artist%3A{self.song["artist"].replace(" ", "%2520")}&type=track&limit=1&offset=0"
        
        search_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Make the POST request
        search_response = requests.get(search_url, headers=search_headers)
    
        # Check if the request was successful
        if search_response.status_code == 200:
            # print("Success!")
            # print(search_response.json())  # Print the response body as JSON
            return f"{search_response.json()["tracks"]["items"][0]["external_urls"]["spotify"]}"
        else:
            print(f"Request failed with status code {search_response.status_code}")
            print(search_response.text)  # Print the search_response body
            return "Error with Spotify API request and/or response processing"

        


def main():

    # Ask the user for mode of play
    mode = choose_play_mode()

    # Create an instance of Hangman (mode == A) or Musical_Hangman (mode == B) class
    if mode == "A":
        hangman = Hangman()
    else:
        hangman = Musical_Hangman()

    # Print instructions
    print(*hangman.instructions, sep="\n")

    # Choose a word
    word = hangman.select_word()
    
    # Guesses loop
    while (hangman.score < 6):
        # Display the hangman structure 
        print(HANGMANPICS[hangman.score], " ",  *hangman.phrase_scheme)
        print(black("Already guessed:", "italic"), *hangman.wrong_guess)
        print("")

        # Check to see if the user won
        if "_" not in hangman.phrase_scheme:
            print(*hangman.get_end_message("won", word), sep="\n")
            sys.exit()

        # Ask for a guess from the user
        guess = get_guess(hangman.wrong_guess, hangman.right_guess)

        # Evaluate the guess
        hangman.evaluate_guess(word, guess)
        

    # If they guessed 6 times and lose
    print(HANGMANPICS[hangman.score], *hangman.phrase_scheme)
    print(black("Already guessed:", "italic"), *hangman.wrong_guess)
    print("")

    # Print the lose message
    print(*hangman.get_end_message("lost", word), sep="\n")
    


def choose_play_mode():
    print(green('''
+-------------------------------------+
|                                     |
|     WELCOME TO MUSICAL HANGMAN      |
|                                     |
+-------------------------------------+
''', "bright"))
    print("Please choose between our two modes by typing A or B:")
    print(cyan("    A) Tradicional Hangman"))
    print(yellow("    B) Musical Hangman"))
    mode = input("Chosen mode: ")
    while re.fullmatch(r"^[abAB]$", mode) is None:
        print(red("Please type A or B."))
        mode = input("Chosen mode: ")
    return mode.upper()


def get_guess(wrong_guess, right_guess):
    guess = input(magenta("Guess: ", "bright")).strip().lower()
    while re.fullmatch(r"^[a-z]$", guess) is None:
        print(red("Please, guess a single letter."))
        guess = input("Guess: ").strip().lower()
    while guess.upper() in wrong_guess or guess.upper() in right_guess:
        print(red("You already guessed this letter. Please, guess again."))
        guess = input("Guess: ").strip().lower()
    return guess

def get_win_lose(outcome):
    if outcome == "won":
        return (green("Congratulations! You won :)", "reverse"))
    else:
        return (red("You lost :(", "reverse"))


if __name__ == "__main__":
    main()