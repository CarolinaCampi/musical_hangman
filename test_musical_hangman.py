from musical_hangman import choose_play_mode, get_guess, get_win_lose
from simple_colors import *
from unittest.mock import patch


def test_choose_play_mode():
    with patch("builtins.input", return_value="a"):
        assert choose_play_mode() == "A"
    with patch("builtins.input", return_value="b"):
        assert choose_play_mode() == "B"


def test_get_guess():
    with patch("builtins.input", return_value="g"):
        assert get_guess(["q", "w"], ["a", "e"]) == "g"


def test_get_win_lose():
    assert get_win_lose("won") == green("Congratulations! You won :)", "reverse")
    assert get_win_lose("lose") == red("You lost :(", "reverse")
    assert get_win_lose("cat") == "Not sure about the outcome of the game :/"

    