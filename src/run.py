"""
Project_8: Texas Hold'em, v0.0.3
"""
from __future__ import annotations
from typing import Any, Optional, Union
from pprint import pprint
from random import randint
import random as rand
import sys

from playingcards import Card, Deck


# KEEP IT SIMPLE, STUPID: Write the client code for JUST THE POKER GAME ITSELF.
# -----------------------
# Writing good documentation is great. Writing good documentation by yourself
# is a waste of time and a sin. Just plan well, and test your code.

class Ann:
    """
    Dev assistant that carries cool constants and static methods.
    """
    SUITS_EMJ: tuple = ('♠', '♥', '♦', '♣')
    SUITS_STR: tuple = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
    VALID_RANKS: tuple = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 255)
    RANKS_NO_JOKERS: tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    STANDARD_DECK_EMJ: dict = {'♠': RANKS_NO_JOKERS,
                            '♥': RANKS_NO_JOKERS,
                            '♦': RANKS_NO_JOKERS,
                            '♣': RANKS_NO_JOKERS}
    STANDARD_DECK_STR: dict = {'Spades': RANKS_NO_JOKERS,
                            'Hearts': RANKS_NO_JOKERS,
                            'Diamonds': RANKS_NO_JOKERS,
                            'Clubs': RANKS_NO_JOKERS}
    AI_NAMES = ['Mr. Johnson', 'Eng Mo', 'Shashta', 'Ishmael', 'Jesse',
                'xXgregXx', 'citizen_sane', 'codge', 'Elvis', 'Cat', 'Dog',
                'Monkey', 'neand69', 'ManBearPig', 'Team-O', 'j0ker',
                'Bavid Dlaine', 'Uncle Wong', 'IT', 'Shrek', 'Donkey',
                'Sill Wmith', 'a bicycle', 'a unicycle', '뛰는놈', '나는놈',
                '아는놈', '새', 'Chicken', 'Bread', 'Onion', 'Cheese', 'a']
    
    @staticmethod
    def shuffle_ai_names() -> list[str]:
        rand.shuffle(Ann.AI_NAMES)
        return Ann.AI_NAMES


class Dealer:
    name: str
    deck: Deck

    def __init__(self, name: str) -> None:
        self.name = name
        self.deck = Deck()
    
    def draw(self) -> Card:
        return self.deck.draw()

class Player:
    # Player Cards
    # curr_hand: list[Card, Card, Card, Card, Card]
    hole_cards: list[Card, Card]
    # Player Info
    username: str
    stack: int
    is_hum: bool
    is_cpu: bool

    def __init__(self,
                 username: str,
                 stack: int,
                 is_hum: bool) -> None:
        # Player Cards
        # self.curr_hand = []
        self.hole_cards = []
        # Player Info
        self.username = username
        self.stack = stack
        self.is_hum = is_hum
        self.is_cpu = not is_hum
    
    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return self.username
    
    def bet(self) -> None:
        pass
    
    def raise_(self) -> None:
        pass

    def call(self) -> None:
        pass

    def check(self) -> None:
        pass

    def fold(self) -> None:
        pass

    def show(self) -> None:
        pass

    def muck(self) -> None:
        pass


class PokerGame:
    # Active "Participants"
    _dealer: Dealer
    _players_queue: list[Player]
    # Physical Aspects
    _pot: int
    _burn_cards: list[Card]
    _comm_cards: list[Card]
    # Game Info
    _players_remaining: int  # decrement everytime a player folds; reset at end
    _total_seats: int  # decrement everytime a player cashes out of the table
    _big_blind: int
    _sml_blind: int
    _buyin_amt: int
    _hands_played: int  # increment everytime a game ends successfully

    def __init__(self,
                 dealer: Dealer,
                 players_list: list[Player],
                 min_bet: int,
                 buyin_amt: int) -> None:
        # Active "Participants"
        self._dealer = dealer
        self._players_queue = players_list
        # Physical Aspects
        self._pot = 0
        self._burn_cards = []
        self._comm_cards = []
        # Game Info
        self._players_remaining = len(players_list)
        self._total_seats = len(players_list)
        self._big_blind = min_bet
        self._sml_blind = min_bet // 2
        self._buyin_amt = buyin_amt
        self._hands_played = 0

    def e0_show_player_stats(self):
        # Introduce the dealer!
        print(f"The dealer of this poker table is '{self._dealer.name}'.\n")
        # EZ-Variables
        players: list[Player] = self._players_queue
        for i, player in enumerate(players):
            print(f"P{i}: {player.username}\n{player.username}'s stack = ${player.stack}\n")

    def e1_post_min_bet(self):
        # EZ-Variables
        dealer: Dealer = self._dealer
        p1: Player = self._players_queue[0]
        p2: Player = self._players_queue[1]
        sml_blind: int = self._sml_blind
        big_blind: int = self._big_blind
        pot: int = self._pot
        # P1
        print(f'{dealer.name}: {p1} posted a small blind of ${sml_blind}.')
        p1.stack -= sml_blind
        pot += sml_blind
        # P2
        print(f'{dealer.name}: {p2} posted a small blind of ${big_blind}.\n')
        p2.stack -= big_blind
        pot += big_blind
        # Print Pot
        print(f"Pot = ${pot}\n")

    def e2_deal_cards(self):
        """
        ***IMPORTANT***
        ===============
        From here on out, treat 1v1 cases like an edge case. Separate code
        accordingly.
        """
        # EZ-Variables
        num_p: int = self._total_seats
        dealer: Dealer = self._dealer
        players: list[Player] = self._players_queue
        # Edge Case: 1v1
        if num_p == 2:
            pass   #TODO
        # Deal Cards
        i = 0
        while i < 2:
            # Deal card one at a time, starting from the dealer's left.
            for player in players:
                player.hole_cards.append(dealer.draw())
            i += 1
        # Print the user's current hole cards.
        for player in players:
            if player.is_hum:
                print(f"Your Cards: {player.hole_cards}\n")


def config_table_settings() -> tuple[str, int, int, int]:
    """
    Prompt user input for configuring game settings.
    """
    print("---------- TABLE SETUP ----------")
    username = input("   - Username: ")
    player_count = input("   - Number of seats: ")
    buyin_amt = input("   - Buy-in (min. $100): $")
    min_bet = input("   - Minimum bet: $")
    print("---------------------------------")
    print("  ^")
    # return username, int(player_count), int(buyin_amt), int(min_bet), table_confirm()

    ans = input("Proceed with these settings? (y/n) ")
    if ans in ['Y', 'y', 'Yes', 'yes', '']:
        print("\nLet's begin! Good luck, and enjoy responsibly.\n")
        return username, int(player_count), int(buyin_amt), int(min_bet), True
    elif ans in ['N', 'n', 'No', 'no']:
        print("\nNo worries. Let's get our table set up again.\n")
        return config_table_settings()
    else:
        print("Invalid input. To confirm your Hold'em table settings, input 'y' or 'n' and hit enter.\n")
        table_confirm()

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

def gen_user_player(username: str, stack: int) -> Player:
    return Player(username, stack, is_hum=True)

def gen_cpu_players_list(cpu_count: int, min_buyin: int) -> list[Player]:
    cpu_names = Ann.shuffle_ai_names()
    ret_list = []
    for i in range(cpu_count):
        ret_list.append(Player(cpu_names[i], randint(min_buyin, randint(min_buyin+10, min_buyin+250)), is_hum=False))
    return ret_list

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
    print("\nAnn: The game will be Texas Hold'em style poker. Let's get ready to play!\n")

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
    # print(f'{username}, {player_count}, {buyin_amt}, {min_bet}, {TABLE_CONFIRMED}')


    # "Client Code" Factory
    # =====================
    p_user = gen_user_player(username, buyin_amt)
    p_cpu = gen_cpu_players_list(player_count - 1, buyin_amt)
    players_list: list[Player] = p_cpu + [p_user]
    rand.shuffle(players_list)
    dealer = Dealer(Ann.AI_NAMES[21])
    print(players_list, end='\n\n')


    # Init Poker Game
    # ===============
    poker = PokerGame(dealer, players_list, min_bet, buyin_amt)

    # Poker Events
    # ============
    poker.e0_show_player_stats()
    poker.e1_post_min_bet()
    poker.e2_deal_cards()
    # poker.e3_bet_blind()
    # poker.e4_deal_flop()
    # poker.e5_bet_flop()
    # poker.e6_deal_turn()
    # poker.e7_bet_turn()
    # poker.e8_deal_river()
    # poker.e9_bet_river()
    # poker.e10_showdown()
    # poker.e11_shift_order()
    # And... Repeat.



    # Begin Hand
    # ==========


    # Reset Poker Hand Structure
    # ==========================


if __name__ == '__main__':
    # import doctest; doctest.testmod()
    # try:
    #     run()
    # except:
    #     sys.exit('\n\n\n  [[ EXIT GAME ]]  \n  ---------------\n  keep ya head up\n')
    run()
