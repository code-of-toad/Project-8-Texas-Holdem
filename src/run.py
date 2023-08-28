"""
Project_8: Texas Hold'em, v0.0.3
"""
from __future__ import annotations
from typing import Any, Optional, Union
from pprint import pprint
from random import randint
from enum import Enum, auto
from colorama import Fore, Back, Style, init
import random as rand
import sys

from playingcards import Card, Deck


init(autoreset=True)

# KEEP IT SIMPLE, STUPID: Write the client code for JUST THE POKER GAME ITSELF.
# -----------------------
# Writing good documentation is great. Writing good documentation by yourself
# is a waste of time and a sin. Just plan well, and test your code.

class Ann:
    """
    Proj_ Assistant
    ---------------
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
                'Monkey', 'ManBearPig', 'Team-O', 'j0ker', 'Mr. White',
                'bavid blaine', 'Uncle Wong', 'IT', 'Shrek', 'Donkey', 'Mrs. Lemon',
                'Will Wmith', 'Bike', 'Unicycle', '뛰는놈', '나는놈', 'Mr. 8east',
                '아는놈', '새', 'Chicken', 'Bread', 'Onion', 'Cheese', 'a']
    class POKER_HANDS_RANKING(Enum):
        ROYAL_FLUSH = 10
        STRAIGHT_FLUSH = 9
        FOUR_OF_A_KIND = 8
        FULL_HOUSE = 7
        FLUSH = 6
        STRAIGHT = 5
        THREE_OF_A_KIND = 4
        TWO_PAIR = 3
        PAIR = 2
        HIGH_CARD = 1

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
    hole_cards: list[Card, Card]
    # curr_hand: list[Card, Card, Card, Card, Card]
    # Player Info
    username: str
    stack: int
    last_bet: int
    is_hum: bool
    is_cpu: bool
    # Player Choices
    class Choice(Enum):
        BET = 'b'
        RAISE = 'r' 
        CALL = 'c'
        CHECK = 'k'
        FOLD = 'f'
        SHOW = 's'
        MUCK ='m'

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
        self.last_bet = 0
        self.is_hum = is_hum
        self.is_cpu = not is_hum
    
    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return self.username


class PokerGame:
    # Active "Participants"
    _dealer: Dealer
    _players_queue: list[Player]  # When game is over, replace this w/ the one below.
    _next_game_players_queue: list[Player]  # Remove players ONLY when one exits the table.
    # Physical Aspects
    _pot: int
    _burn_cards: list[Card]
    _comm_cards: list[Card]
    # Game Info
    _curr_bet: int
    # _total_seats: int  # decrement everytime a player cashes out
    _big_blind: int
    _sml_blind: int
    _buyin_amt: int
    _hands_played: int  # increment everytime a game ends successfully

    def __init__(self,
                 dealer: Dealer,
                 players_list: list[Player],
                 min_bet: int,
                 buyin_amt: int) -> None:
        # Copy Mutable Params
        players_list_1 = players_list.copy()
        players_list_2 = players_list.copy()
        # Active "Participants"
        self._dealer = dealer
        self._players_queue = players_list_1
        players_list_2.append(players_list_2.pop(0))
        self._next_game_players_queue = players_list_2
        # Physical Aspects
        self._pot = 0
        self._burn_cards = []
        self._comm_cards = []
        # Game Info
        self._curr_bet = min_bet
        self._total_seats = len(players_list)
        self._big_blind = min_bet
        self._sml_blind = min_bet // 2
        self._buyin_amt = buyin_amt
        self._hands_played = 0

    def e0_show_player_stats(self):
        # Introduce the dealer!
        print("============== PROJ_8: TEXAS HOLD'EM ==============\n")
        print(f"The dealer of this poker table is: ", end='')
        print(Fore.LIGHTMAGENTA_EX + f"{self._dealer.name}", end='')
        print(".\n\n")
        # EZ-Variables
        players: list[Player] = self._players_queue
        for i, player in enumerate(players):
            print(f"p{i}: ", end='')
            print(Fore.CYAN + f"{player.username}", end='')
            print(f"'s stack = ", end='')
            print(Fore.GREEN + f"${player.stack}\n")

    def e1_blind_bet(self):
        print("\n============== BLIND BET ==============\n")
        # EZ-Variables
        dealer: str = self._dealer.name
        p0: Player = self._players_queue[0]
        p1: Player = self._players_queue[1]
        sml_blind: int = self._sml_blind
        big_blind: int = self._big_blind
        # P1
        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
        print(": ", end='')
        print(Fore.CYAN + f"{p0}", end='')
        print(f" posted a small blind bet of ${sml_blind}.\n")
        p0.stack -= sml_blind
        p0.last_bet = sml_blind
        self._pot += sml_blind
        # P2
        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
        print(": ", end='')
        print(Fore.CYAN + f"{p1}", end='')
        print(f" posted a big blind bet of ${big_blind}.\n")
        p1.stack -= big_blind
        p1.last_bet = big_blind
        self._pot += big_blind
        # Print Pot
        print()
        print(Fore.GREEN + f"Pot = ${self._pot}\n")

    def e2_deal_pocket(self):
        # EZ-Variables
        dealer: Dealer = self._dealer
        players: list[Player] = self._players_queue
        # Deal Cards
        for _ in range(2):
            # Deal card one at a time, starting from the dealer's left.
            for p in players:
                p.hole_cards.append(dealer.draw())
        # Print the user's current hole cards.
        for p in players:
            if p.is_hum:
                hole_1 = p.hole_cards[0]
                hole_2 = p.hole_cards[1]
                print("Your cards:\n-----------\n\n  ", end='')
                if hole_1.get_suit() in ['Spades', 'Clubs']:
                    print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f" {hole_1} ", end='')
                    if hole_2.get_suit() in ['Spades', 'Clubs']:
                        print("  ", end='')
                        print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f" {hole_2} ")
                        print()
                    else:
                        print("  ", end='')
                        print(Style.BRIGHT + Back.WHITE + Fore.RED + f" {hole_2} ")
                        print()
                else:
                    print(Style.BRIGHT + Back.WHITE + Fore.RED + f" {hole_1} ", end='')
                    if hole_2.get_suit() in ['Spades', 'Clubs']:
                        print("  ", end='')
                        print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f" {hole_2} ")
                        print()
                    else:
                        print("  ", end='')
                        print(Style.BRIGHT + Back.WHITE + Fore.RED + f" {hole_2} ")
                        print()

    def e3_preflop(self):
        # EZ-Variables
        players: list[Player] = self._players_queue
        num_p: int = self._total_seats
        # Edge Case: 1v1
        if num_p == 2:
            pass   #TODO
        # Betting Round: Pre-Flop
        # ====================================================================
        # TODO: Write `_handle_turn_order_preflop`, an iterative helper that
        #       handles all player calls, raises, and folds until every player
        #       has called or folded. Figure it out.
        # ====================================================================
        # Call iterative turn handler
        self._turn_order_preflop(players)
        # Print Pot
        print(Fore.GREEN + f"\nPot (Pre-Flop): ${self._pot}\n")

    def _turn_order_preflop(self, players: list[Player]) -> tuple[int, int, int]:
        # EZ-Variables
        dealer: str = self._dealer.name
        old_bet: int = self._curr_bet
        # Go thru each player, and continue until every player has called/folded.
        caller_count = 0
        i = 2
        while caller_count < len(players):
            # Valid Index Check
            if i == len(players):
                i = 0
            # Player
            p = players[i]

            # Human Player Turn:
            if p.is_hum:
                # Invalid Input Check:
                while True:
                    # Ask user for decision.
                    print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                    print(": ", end='')
                    print(Fore.CYAN + f"{p.username}", end='')
                    player_choice = input(", will you [c]all, [r]aise, or [f]old? ")
                    if player_choice in ['Call', 'call', 'C', 'c', 'CALL', '']:
                        ans = 'CALL'
                        break
                    elif player_choice in ['Raise', 'raise', 'R', 'r', 'RAISE']:
                        ans = 'RAISE'
                        break
                    elif player_choice in ['Fold', 'fold', 'F', 'f', 'FOLD']:
                        ans = 'FOLD'
                        break
                    print(Style.BRIGHT + Fore.LIGHTRED_EX + "Invalid input: Enter 'c', 'r', or 'f'.\n")

                # if player CALLS:
                if ans ==  p.Choice.CALL.name:
                    # Adjust Attributes
                    caller_count += 1
                    self._pot += self._curr_bet - p.last_bet
                    p.stack -= self._curr_bet - p.last_bet
                    p.last_bet = self._curr_bet
                    # Annouce Player Action 
                    print(f"{p.username}: call.")
                    # Print Pot
                    print(f"Pot: ${self._pot}\n")

                # elif player RAISES:
                elif ans == p.Choice.RAISE.name:
                    # Invalid Input Check:
                    while True:
                        print(Fore.LIGHTMAGENTA_EX + f"\n{dealer}", end='')
                        raise_amt = input(f": The current bet is ${self._curr_bet}. What will you raise it to? $")
                        if raise_amt.isdigit() and int(raise_amt) in range(self._curr_bet + 1, p.stack):
                            break
                        print(Style.BRIGHT + Fore.LIGHTRED_EX + f"Invalid Input: The raise amount must be an integer from ${self._curr_bet + 1} (minimum raise) to ${p.stack} (your stack).")
                    # Adjust Attributes & Variables
                    old_bet = self._curr_bet
                    caller_count = 1
                    p.stack -= int(raise_amt) - old_bet
                    self._pot += int(raise_amt) - old_bet
                    self._curr_bet = int(raise_amt)
                    # Annouce Player Action 
                    print()
                    print(Fore.CYAN + f"{p.username}", end='')
                    print(f" raised the bet from ${old_bet} to ${self._curr_bet}.")
                    # Print Pot
                    print(f"Pot: ${self._pot} (Your current stack: ${p.stack})\n")

                # elif player FOLDS:
                elif ans == p.Choice.FOLD.name:
                    players.pop(i)
                    i -= 1  # Offset to account for the increment in '# Close While-Loop'
                    # Annouce Player Action 
                    print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                    print(": ", end='')
                    print(f"{p.username}", end='')
                    print(" has folded.\n")

            # CPU Player Turn:
            elif p.is_cpu:
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
                # Adjust Attributes
                caller_count += 1
                self._pot += self._curr_bet - p.last_bet
                p.stack -= self._curr_bet - p.last_bet
                p.last_bet = self._curr_bet
                # Annouce Player Action 
                print(Fore.CYAN + f"{p.username}", end='')
                print(f": call.")
                # Print Pot
                print(f"Pot: ${self._pot}\n")
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
            # Close While-Loop
            i += 1

    def e4_deal_flop(self):
        pass

    def e5_flop(self):
        pass

    def e6_deal_turn(self):
        pass

    def e7_turn(self):
        pass

    def e8_deal_river(self):
        pass

    def e9_river(self):
        pass

    def e10_showdown(self):
        pass

    def e11_reward_winner(self):
        pass

    def e12_save_data(self):
        pass

    def e13_shift_order(self):
        pass


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
        print("\nLet's begin! Good luck, and enjoy responsibly.\n\n")
        return username, int(player_count), int(buyin_amt), int(min_bet), True
    elif ans in ['N', 'n', 'No', 'no']:
        print("\nNo worries. Let's get our table set up again.\n")
        return config_table_settings()
    else:
        print(Style.BRIGHT + Fore.LIGHTRED_EX + "Invalid input. To confirm your Hold'em table settings, input 'y' or 'n' and hit enter.\n")
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
        print(Style.BRIGHT + Fore.LIGHTRED_EX + "Invalid input. To confirm your Hold'em table settings, input 'y' or 'n' and hit enter.\n")
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
    print(Fore.LIGHTGREEN_EX + "\nThe game will be Texas Hold'em style poker. Let's get ready to play!\n")
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
        buyin_amt,        #      This code is faulty. Currently, there's no
        min_bet,          #      recursion happening here, currently. It breaks
                          #      after two complete init prompt cycles.
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

    # Init Poker Game
    # ===============
    poker = PokerGame(dealer, players_list, min_bet, buyin_amt)

    # DEBUGGGGGGGGGGGGGGGGG
    # =====================
    # print(poker._players_queue)
    # print(poker._next_game_players_queue, end='\n\n\n')

    # Poker Events
    # ============
    poker.e0_show_player_stats()
    poker.e1_blind_bet()
    print("\n============== DEALER: HOLE CARDS ==============\n")
    poker.e2_deal_pocket()
    print("\n============== PRE-FLOP ==============\n")
    poker.e3_preflop()
    print("\n============== DEALER: FLOP ==============\n")
    print('\n\n\n')
    # poker.e4_deal_flop()
    # poker.e5_flop()
    # poker.e6_deal_turn()
    # poker.e7_turn()
    # poker.e8_deal_river()
    # poker.e9_river()
    # poker.e10_showdown()
    # poker.e11_reward_winner()
    # poker.e12_save_data()
    # poker.e13_shift_order()

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
    # print(Player.Choice.BET.name == 'BET')