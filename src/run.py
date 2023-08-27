"""
Project_8: Texas Hold'em, v0.0.3
"""
from __future__ import annotations
from typing import Any, Optional, Union
from pprint import pprint
import random as rand
import sys

from playingcards import Card, Deck


# KEEP IT SIMPLE, STUPID: Write the client code for JUST THE POKER GAME ITSELF.
# -----------------------
# Writing good documentation is great. Writing good documentation by yourself
# is a waste of time and a sin. Just plan well, and test your code.

class Dealer:
    deck: Deck

class Player:
    username: str
    curr_hand: list[Card, Card, Card, Card, Card]
    hole_cards: list[Card, Card]
    stack: int
    is_hum: bool
    is_cpu: bool


    def __init__(self, username: str, stack: int, is_hum: bool) -> None:
        self.username = username
        self.curr_hand = []
        self.hole_cards = []
        self.stack = stack
        self.is_hum = is_hum
        self.is_cpu = not is_hum


class PokerGame:
    # Physical Aspects
    pot: int
    burn_cards: list[Card]
    comm_cards: list[Card]
    players_queue: list[Player]
    # Information
    players_count: int
    big_blind: int
    sml_blind: int
    buyin_amt: int
    hands_played: int

    def __init__(self, players_list, min_bet, buyin_amt):
        self.pot = 0
        self.burn_cards = []
        self.comm_cards = []
        self.players_queue = players_list
        self.players_count = len(players_list)
        self.big_blind = min_bet
        self.sml_blind = min_bet // 2
        self.buyin_amt = buyin_amt
        self.hands_played = 0


def config_table_settings() -> tuple[str, int, int, int]:
    """
    Prompt user input for configuring game settings.
    """
    print("---------- TABLE SETUP ----------")
    username = input("    - Username: ")
    player_count = input("    - Number of seats: ")
    buyin_amt = input("    - Buy-in (min. $100): $")
    min_bet = input("    - Minimum bet: $")
    print("---------------------------------")
    print("  ^")
    return username, int(player_count), int(buyin_amt), int(min_bet), table_confirm()

    # ans = input("Proceed with these settings? (y/n) ")
    # if ans in ['Y', 'y', 'Yes', 'yes', '']:
    #     print("\nLet's begin! Good luck, and enjoy responsibly.\n")
    #     return username, int(player_count), int(buyin_amt), int(min_bet)
    # elif ans in ['N', 'n', 'No', 'no']:
    #     print("\nNo worries. Let's get our table set up again.\n")
    #     return config_table_settings()
    # else:
    #     print("Invalid input. To confirm your Hold'em table settings, input 'y' or 'n' and hit enter.\n")
    #     table_confirm()

def table_confirm() -> bool:
    """
    If user wants to proceed, return True.
    Else, loop back to the player_count request.
    """
    ans = input("Proceed with these settings? (y/n) ")
    if ans in ['Y', 'y', 'Yes', 'yes', '']:
        print("\nLet's begin! Enjoy responsibly.\n")
        return True
    elif ans in ['N', 'n', 'No', 'no']:
        print("\nNo worries. Let's get our table set up again.\n")
        return False
    else:
        print("Invalid input. To confirm your Hold'em table settings, input 'y' or 'n' and hit enter.\n")
        return table_confirm()

def gen_user_player(username: str, stack: int):
    user_player = Player(username, stack, is_hum=True)

def gen_cpu_player(username: str, stack: int):
    cpu_player = Player(username, stack, is_hum=False)

def run():
    """
    Poker Game Abstraction:
    -----------------------
    1. The house (here, the dealer) is NOT aware of the value of a face-down
    playing card, at any point in time.

    """
    # Input Prompts
    # =============
    print("\nFrom proj_Studio,\nWelcome to Project_8: Texas Hold'em, v0.0.3.")
    print("\nNote: Press 'ctrl + c' to exit the game at any time.\n")
    print("\nThe game will be Texas Hold'em style poker. Let's get ready to play!\n")

    (
    username,
    player_count,
    buyin_amt,
    min_bet,
    TABLE_CONFIRMED
    ) = config_table_settings()
    if not TABLE_CONFIRMED:
        (
        username,
        player_count,     #TODO: Implement a recursive input babysitter.
        buyin_amt,        #      This code is faulty. There's no recursion
        min_bet,          #      happening here, currently.
        TABLE_CONFIRMED
        ) = config_table_settings()

    pprint(f'{username}, {player_count}, {buyin_amt}, {min_bet}, {TABLE_CONFIRMED}')


    # "Client Code" Factory
    # =====================
    p_user = gen_user_player(username, buyin_amt)
    p_cpu = gen_cpu_player(NotImplemented)
    players_list: list[Player] = p_cpu + [p_user]
    rand.shuffle(players_list)


    # Init Poker Game
    # ===============
    pkr = PokerGame(players_list, min_bet, buyin_amt)


    # Begin Hand
    # ==========


    # Reset Poker Hand Structure
    # ==========================


if __name__ == '__main__':
    # import doctest; doctest.testmod()
    try:
        run()
    except:
        sys.exit('\n\n\n  [[ EXIT GAME ]]  \n  ---------------\n  keep ya head up\n')
