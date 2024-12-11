from musical_hangman import choose_play_mode, get_guess, get_win_lose
from simple_colors import *


def test_choose_play_mode():
    assert 1 == 1

def test_get_guess():
    # assert get_guess(["q", "w"], ["a", "e"]) == 
    assert 1 == 1

def test_get_win_lose():
    assert get_win_lose("won") == green("Congratulations! You won :)", "reverse")
    assert get_win_lose("lose") == red("You lost :(", "reverse")
    assert get_win_lose("cat") == "Not sure about the outcome of the game :/"

    