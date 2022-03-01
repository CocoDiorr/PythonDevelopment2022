from textdistance import hamming, sorensen_dice
from random import choice
from typing import List

def bullscows(guess: str, secret: str) -> (int, int):
    bulls = len(guess) - hamming(guess, secret)
    cows = sorensen_dice(guess, secret) * len(guess)
    return bulls, int(cows)

def ask(promt: str, words: List[str] = None) -> str:
    guess = input(promt)
    if words:
        while guess not in words:
            print("Chosen word not in dictionary - try again")
            guess = input(promt)
    return guess

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
    secret = choice(words)
    bulls, cows = 0, 0
    tries = 0
    while bulls != len(secret):
        guess = ask("Введите слово: ", words)
        tries += 1
        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
    return tries
