"""
Project_8: Texas Hold'em, v0.0.3
"""
from __future__ import annotations
from typing import Any, Optional, Union
from pprint import pprint
from random import randint
from enum import Enum, auto
from colorama import Style, Fore, Back, init
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


def print_card(card: Card) -> None:
    if card.is_blk():
        print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f"  {card}  ", end='')
    elif card.is_red():
        print(Style.BRIGHT + Back.WHITE + Fore.RED + f"  {card}  ", end='')


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
        print(f"The dealer of this poker table is: ", end='')
        print(Fore.LIGHTMAGENTA_EX + f"{self._dealer.name}", end='')
        print(".\n\n")
        # Introduce the players!
        players: list[Player] = self._players_queue
        for player in players:
            print(Fore.CYAN + f"{player.username}", end='')
            print(f"'s stack = ", end='')
            print(Fore.GREEN + f"${player.stack}\n")

    def e1_blind_bet(self):
        # EZ-Variables
        dealer: str = self._dealer.name
        p0: Player = self._players_queue[0]
        p1: Player = self._players_queue[1]
        sml_blind: int = self._sml_blind
        big_blind: int = self._big_blind
        # P1
        # DEBUGGGGGGGGGGGGGGGGGGGGG
        print("DEBUG", f"{p0.username}'s stack: {p0.stack}")
        print("DEBUG", f"{p0.username}'s last bet: {p0.last_bet}")
        print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
        # DEBUGGGGGGGGGGGGGGGGGGGGG
        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
        print(": ", end='')
        print(Fore.CYAN + f"{p0}", end='')
        print(f" posted a small blind bet of ${sml_blind}.\n")
        p0.stack -= sml_blind
        p0.last_bet = sml_blind
        self._pot += sml_blind
        # DEBUGGGGGGGGGGGGGGGGGGGGG
        print("DEBUG", f"{p0.username}'s stack: {p0.stack}")
        print("DEBUG", f"{p0.username}'s last bet: {p0.last_bet}")
        print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
        # DEBUGGGGGGGGGGGGGGGGGGGGG
        # P2
        # DEBUGGGGGGGGGGGGGGGGGGGGG
        print("\nDEBUG", f"{p1.username}'s stack: {p1.stack}")
        print("DEBUG", f"{p1.username}'s last bet: {p1.last_bet}")
        print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
        # DEBUGGGGGGGGGGGGGGGGGGGGG
        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
        print(": ", end='')
        print(Fore.CYAN + f"{p1}", end='')
        print(f" posted a big blind bet of ${big_blind}.\n")
        p1.stack -= big_blind
        p1.last_bet = big_blind
        self._pot += big_blind
        # DEBUGGGGGGGGGGGGGGGGGGGGG
        print("DEBUG", f"{p1.username}'s stack: {p1.stack}")
        print("DEBUG", f"{p1.username}'s last bet: {p1.last_bet}")
        print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
        # DEBUGGGGGGGGGGGGGGGGGGGGG
        # Print Pot
        print()
        print(Fore.GREEN + f"Pot (Blind) = ${self._pot}\n")

    def e2_deal_pocket(self):
        # EZ-Variables
        dealer: Dealer = self._dealer
        players: list[Player] = self._players_queue
        # Deal Cards
        for _ in range(2):
            # Deal card one at a time, starting from the dealer's left.
            for p in players:
                p.hole_cards.append(dealer.draw())
        # Print the user's pocket cards.
        self._display_hum_cards()

    def _display_hum_cards(self):
        # EZ_Variables
        players: list[Player] = self._players_queue
        for p in players:
            if p.is_hum:
                c1: Card = p.hole_cards[0]
                c2: Card = p.hole_cards[1]
                print("Your cards:\n-----------\n\n", end='')
                print("  ", end='')
                print_card(c1)
                print("  ", end='')
                print_card(c2)
                print(end='\n\n')
        # Below rests a prime example of inelegant code.
        # ----------------------------------------------
        # if c1.get_suit() in ['Spades', 'Clubs']:
        #     print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f" {c1} ", end='')
        #     if c2.get_suit() in ['Spades', 'Clubs']:
        #         print("  ", end='')
        #         print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f" {c2} ")
        #         print()
        #     else:
        #         print("  ", end='')
        #         print(Style.BRIGHT + Back.WHITE + Fore.RED + f" {c2} ")
        #         print()
        # else:
        #     print(Style.BRIGHT + Back.WHITE + Fore.RED + f" {c1} ", end='')
        #     if c2.get_suit() in ['Spades', 'Clubs']:
        #         print("  ", end='')
        #         print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f" {c2} ")
        #         print()
        #     else:
        #         print("  ", end='')
        #         print(Style.BRIGHT + Back.WHITE + Fore.RED + f" {c2} ")
        #         print()

    def e3_preflop(self):
        # EZ-Variables
        players: list[Player] = self._players_queue
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
        """
        To be used within `self.e3_preflop()`
        """
        # EZ-Variables
        old_bet = self._curr_bet
        dealer: str = self._dealer.name
        # Go thru each player, and continue until every player has called/folded.
        caller_count = 0
        i = 2
        while caller_count < len(players):
            # Valid Index Check
            if i == len(players):
                i = 0
            # Player
            p = players[i]
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            print("\nDEBUG", f"{p.username}'s stack: {p.stack}")
            print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGG
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
                    print(Fore.LIGHTRED_EX + "Invalid input: Enter 'c', 'r', or 'f'.\n")

                # CALL:
                if ans == 'CALL':
                    # Update Caller Count
                    caller_count += 1
                    # Adjust Attributes
                    toss_into_pot = self._curr_bet - p.last_bet
                    self._pot += toss_into_pot
                    p.stack -= toss_into_pot
                    p.last_bet = self._curr_bet
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Call. (your stack: ${p.stack})")
                    # Print Pot
                    print(f"Pot: ${self._pot}\n")

                # RAISE:
                elif ans == 'RAISE':
                    # Invalid Input Check:
                    while True:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        raise_amt = input(f": The current bet is ${self._curr_bet}. What will you raise it to? $")
                        if raise_amt.isdigit() and int(raise_amt) in range(self._curr_bet + 1, p.stack + 1):
                            break
                        print(Fore.LIGHTRED_EX + f"Invalid Input: The raise amount must be an integer from ${self._curr_bet + 1} (minimum raise) to ${p.stack} (your stack).\n")
                    # Update Caller Count
                    caller_count = 1
                    # Toss Chips Into Pot
                    chips =  int(raise_amt) - p.last_bet
                    p.stack -= chips
                    self._pot += chips
                    # Update Game Stats
                    self._curr_bet = int(raise_amt)
                    # Update Player Last Bet
                    p.last_bet = int(raise_amt)
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}", end='')
                    print(f" raised the bet from ${old_bet} to ${self._curr_bet}.")
                    # Print Pot
                    print(f"Pot: ${self._pot} (Your current stack: ${p.stack})\n")

                # FOLD:
                elif ans == 'FOLD':
                    players.pop(i)
                    i -= 1  # Offset to account for the increment in '# Close While-Loop'
                    # Annouce Player Action 
                    print("\n" + Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                    print(": ", end='')
                    print(f"{p.username}", end='')
                    print(" has ", end='')
                    print(Fore.RED + "folded" + Style.RESET_ALL + ". ")
                    print(f"{p.username}'s stack: ${p.stack}\n")

            # CPU Player Turn:
            elif p.is_cpu:
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
                # Update Caller Count
                caller_count += 1
                # Toss Chips Into Pot
                chips = self._curr_bet - p.last_bet
                self._pot += chips
                p.stack -= chips
                # Update Player Last Bet
                p.last_bet = self._curr_bet
                # Annouce Player Action 
                print(Fore.CYAN + f"{p.username}", end='')
                print(": Call.")
                # Print Pot
                print(f"Pot: ${self._pot}\n")
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
            # Close While-Loop
            i += 1
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            print("DEBUG", f"{p.username}'s stack: {p.stack}")
            print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGG

    def e4_deal_flop(self):
        # EZ-Variables
        dealer: Dealer = self._dealer
        burn_cards: list[Card] = self._burn_cards
        comm_cards: list[Card] = self._comm_cards
        # Print Dealer ACtion
        print(
Fore.LIGHTMAGENTA_EX + f"{dealer.name}" + Style.RESET_ALL + " \
burns a card & reveals three community cards on the board:\n\
-----------------------------------------------------------------\n")
        # Logic
        burn_cards.append(dealer.draw())   # burn card
        for _ in range(3):                 # collect community cards (3 total)
            comm_cards.append(dealer.draw()) 
        # Display Community Cards
        for card in comm_cards:
            print("  ", end='')
            print_card(card)
        print()
        print()
        # Display Player Cards
        self._display_hum_cards()
    
    def e5_flop(self):
        # EZ-Variables
        players: list[Player] = self._players_queue
        # Call iterative turn handler
        self._turn_order_flop(players)
        # Print Pot
        print(Fore.GREEN + f"\nPot (Flop): ${self._pot}\n")

    def _turn_order_flop(self, players: list[Player]) -> tuple[int, int, int]:
        """
        To be used within `self.e5_turn()`.

        Features:
          - 'CALL' or 'CHECK'
          - 'RAISE' or 'BET'
        """
        # EZ-Variables
        old_bet = self._curr_bet
        dealer: str = self._dealer.name
        bet_already_occurred: bool = False
        # Go thru each player, and continue until every player has called/folded.
        caller_count = 0
        i = 0
        while caller_count < len(players):
            # Valid Index Check
            if i == len(players):
                i = 0
            # Player
            p = players[i]
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            print("\nDEBUG", f"{p.username}'s stack: {p.stack}")
            print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            # BROKE NINJA CHECK:
            if p.stack < (self._curr_bet - p.last_bet):
                players.pop(i)
                i -= 1  # Offset to account for the auto increment in '# Close While-Loop'
                # Annouce Player Action 
                print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                print(": ", end='')
                print(f"{p.username}", end='')
                print(" does NOT have enough chips & ", end='')
                print(Fore.RED + "folds" + Style.RESET_ALL + ". ")
                print(f"{p.username}'s stack: ${p.stack}\n")
                continue
            # Human Player Turn:
            if p.is_hum:
                # Invalid Input Check:
                while True:
                    # Ask user for decision.
                    if bet_already_occurred:
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
                        print(Fore.LIGHTRED_EX + "Invalid input: Enter 'c', 'r', or 'f'.\n")
                    else:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        print(": ", end='')
                        print(Fore.CYAN + f"{p.username}", end='')
                        player_choice = input(", will you [c]heck, [b]bet, or [f]old? ")
                        if player_choice in ['Check', 'check', 'C', 'c', 'CHECK', '']:
                            ans = 'CHECK'
                            break
                        elif player_choice in ['Bet', 'bet', 'B', 'b', 'BET']:
                            ans = 'BET'
                            bet_already_occurred = True
                            break
                        elif player_choice in ['Fold', 'fold', 'F', 'f', 'FOLD']:
                            ans = 'FOLD'
                            break
                        print(Fore.LIGHTRED_EX + "Invalid input: Enter 'c', 'b', or 'f'.\n")

                # CALL:
                if ans == 'CALL':
                    # Update Caller Count
                    caller_count += 1
                    # Adjust Attributes
                    chips = self._curr_bet - p.last_bet
                    self._pot += chips
                    p.stack -= chips
                    p.last_bet = self._curr_bet
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Call. (your stack: ${p.stack})")
                    # Print Pot
                    print(f"Pot: ${self._pot}\n")
                
                # CHECK:
                elif ans == 'CHECK':
                    # Update Caller Count
                    caller_count += 1
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Check. (your stack: ${p.stack})")
                    # Print Pot
                    print(f"Pot: ${self._pot}\n")

                # RAISE or BET:
                elif ans in ['RAISE', 'BET']:
                    # Invalid Input Check:
                    while True:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        raise_amt = input(f": The current bet is ${self._curr_bet}. What will you raise it to? $")
                        if raise_amt.isdigit() and int(raise_amt) in range(self._curr_bet + 1, p.stack + 1):
                            break
                        print(Fore.LIGHTRED_EX + f"Invalid Input: The raise amount must be an integer from ${self._curr_bet + 1} (minimum raise) to ${p.stack} (your stack).\n")
                    # Update Caller Count
                    caller_count = 1
                    # Toss Chips Into Pot
                    chips =  int(raise_amt) - p.last_bet
                    p.stack -= chips
                    self._pot += chips
                    # Update Game Stats
                    self._curr_bet = int(raise_amt)
                    # Update Player Last Bet
                    p.last_bet = int(raise_amt)
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}", end='')
                    print(f" raised the bet from ${old_bet} to ${self._curr_bet}.")
                    # Print Pot
                    print(f"Pot: ${self._pot} (Your current stack: ${p.stack})\n")

                # FOLD:
                elif ans == 'FOLD':
                    players.pop(i)
                    i -= 1  # Offset to account for the increment in '# Close While-Loop'
                    # Annouce Player Action 
                    print("\n" + Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                    print(": ", end='')
                    print(f"{p.username}", end='')
                    print(" has ", end='')
                    print(Fore.RED + "folded" + Style.RESET_ALL + ". ")
                    print(f"{p.username}'s stack: ${p.stack}\n")

            # CPU Player Turn:
            elif p.is_cpu:
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
                # Update Caller Count
                caller_count += 1
                # Toss Chips Into Pot
                chips = self._curr_bet - p.last_bet
                self._pot += chips
                p.stack -= chips
                # Update Player Last Bet
                p.last_bet = self._curr_bet
                # Annouce Player Action 
                print(Fore.CYAN + f"{p.username}", end='')
                if chips == 0:
                    print(": Check.")
                else:
                    print(": Call.")
                # Print Pot
                print(f"Pot: ${self._pot}\n")
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
            # Close While-Loop
            i += 1
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            print("DEBUG", f"{p.username}'s stack: {p.stack}")
            print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGG
        

    def e6_deal_turn(self):
        # EZ-Variables
        dealer: Dealer = self._dealer
        burn_cards: list[Card] = self._burn_cards
        comm_cards: list[Card] = self._comm_cards
        # Print Dealer ACtion
        print(Fore.LIGHTMAGENTA_EX + f"{dealer.name}" + Style.RESET_ALL + " \
burns a card & reveals another community card on the board:\n\
------------------------------------------------------------------------\n")
        # Logic
        burn_cards.append(dealer.draw())   # burn card
        comm_cards.append(dealer.draw())   # collect one community card
        # Display Community Cards
        for card in comm_cards:
            print("  ", end='')
            print_card(card)
        print()
        print()
        # Display Player Cards
        self._display_hum_cards()

    def e7_turn(self):
        # EZ-Variables
        players: list[Player] = self._players_queue
        # Call iterative turn handler
        self._turn_order_turn(players)
        # Print Pot
        print(Fore.GREEN + f"\nPot (Turn): ${self._pot}\n")

    def _turn_order_turn(self, players: list[Player]) -> tuple[int, int, int]:
        """
        To be used within `self.e7_turn()`.

        Features:
          - 'CALL' or 'CHECK'
          - 'RAISE' or 'BET'
        """
        # EZ-Variables
        old_bet = self._curr_bet
        dealer: str = self._dealer.name
        bet_already_occurred: bool = False
        # Go thru each player, and continue until every player has called/folded.
        caller_count = 0
        i = 0
        while caller_count < len(players):
            # Valid Index Check
            if i == len(players):
                i = 0
            # Player
            p = players[i]
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            print("\nDEBUG", f"{p.username}'s stack: {p.stack}")
            print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            # BROKE NINJA CHECK:
            if p.stack < (self._curr_bet - p.last_bet):
                players.pop(i)
                i -= 1  # Offset to account for the auto increment in '# Close While-Loop'
                # Annouce Player Action 
                print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                print(": ", end='')
                print(f"{p.username}", end='')
                print(" does NOT have enough chips & ", end='')
                print(Fore.RED + "folds" + Style.RESET_ALL + ". ")
                print(f"{p.username}'s stack: ${p.stack}\n")
                continue
            # Human Player Turn:
            if p.is_hum:
                # Invalid Input Check:
                while True:
                    # Ask user for decision.
                    if bet_already_occurred:
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
                        print(Fore.LIGHTRED_EX + "Invalid input: Enter 'c', 'r', or 'f'.\n")
                    else:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        print(": ", end='')
                        print(Fore.CYAN + f"{p.username}", end='')
                        player_choice = input(", will you [c]heck, [b]bet, or [f]old? ")
                        if player_choice in ['Check', 'check', 'C', 'c', 'CHECK', '']:
                            ans = 'CHECK'
                            break
                        elif player_choice in ['Bet', 'bet', 'B', 'b', 'BET']:
                            ans = 'BET'
                            bet_already_occurred = True
                            break
                        elif player_choice in ['Fold', 'fold', 'F', 'f', 'FOLD']:
                            ans = 'FOLD'
                            break
                        print(Fore.LIGHTRED_EX + "Invalid input: Enter 'c', 'b', or 'f'.\n")

                # CALL:
                if ans == 'CALL':
                    # Update Caller Count
                    caller_count += 1
                    # Adjust Attributes
                    chips = self._curr_bet - p.last_bet
                    self._pot += chips
                    p.stack -= chips
                    p.last_bet = self._curr_bet
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Call. (your stack: ${p.stack})")
                    # Print Pot
                    print(f"Pot: ${self._pot}\n")
                
                # CHECK:
                elif ans == 'CHECK':
                    # Update Caller Count
                    caller_count += 1
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Check. (your stack: ${p.stack})")
                    # Print Pot
                    print(f"Pot: ${self._pot}\n")

                # RAISE or BET:
                elif ans in ['RAISE', 'BET']:
                    # Invalid Input Check:
                    while True:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        raise_amt = input(f": The current bet is ${self._curr_bet}. What will you raise it to? $")
                        if raise_amt.isdigit() and int(raise_amt) in range(self._curr_bet + 1, p.stack + 1):
                            break
                        print(Fore.LIGHTRED_EX + f"Invalid Input: The raise amount must be an integer from ${self._curr_bet + 1} (minimum raise) to ${p.stack} (your stack).\n")
                    # Update Caller Count
                    caller_count = 1
                    # Toss Chips Into Pot
                    chips =  int(raise_amt) - p.last_bet
                    p.stack -= chips
                    self._pot += chips
                    # Update Game Stats
                    self._curr_bet = int(raise_amt)
                    # Update Player Last Bet
                    p.last_bet = int(raise_amt)
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}", end='')
                    print(f" raised the bet from ${old_bet} to ${self._curr_bet}.")
                    # Print Pot
                    print(f"Pot: ${self._pot} (Your current stack: ${p.stack})\n")

                # FOLD:
                elif ans == 'FOLD':
                    players.pop(i)
                    i -= 1  # Offset to account for the increment in '# Close While-Loop'
                    # Annouce Player Action 
                    print("\n" + Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                    print(": ", end='')
                    print(f"{p.username}", end='')
                    print(" has ", end='')
                    print(Fore.RED + "folded" + Style.RESET_ALL + ". ")
                    print(f"{p.username}'s stack: ${p.stack}\n")

            # CPU Player Turn:
            elif p.is_cpu:
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
                # Update Caller Count
                caller_count += 1
                # Toss Chips Into Pot
                chips = self._curr_bet - p.last_bet
                self._pot += chips
                p.stack -= chips
                # Update Player Last Bet
                p.last_bet = self._curr_bet
                # Annouce Player Action 
                print(Fore.CYAN + f"{p.username}", end='')
                if chips == 0:
                    print(": Check.")
                else:
                    print(": Call.")
                # Print Pot
                print(f"Pot: ${self._pot}\n")
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
            # Close While-Loop
            i += 1
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            print("DEBUG", f"{p.username}'s stack: {p.stack}")
            print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGG

    def e8_deal_river(self):
        self.e6_deal_turn()

    def e9_river(self):
        # EZ-Variables
        players: list[Player] = self._players_queue
        # Call iterative turn handler
        self._turn_order_river(players)
        # Print Pot
        print(Fore.GREEN + f"\nPot (River): ${self._pot}\n")

    def _turn_order_river(self, players: list[Player]) -> tuple[int, int, int]:
        """
        To be used within `self.e9_turn()`.

        Features:
          - 'CALL' or 'CHECK'
          - 'RAISE' or 'BET'
        """
        # EZ-Variables
        old_bet = self._curr_bet
        dealer: str = self._dealer.name
        bet_already_occurred: bool = False
        # Go thru each player, and continue until every player has called/folded.
        caller_count = 0
        i = 0
        while caller_count < len(players):
            # Valid Index Check
            if i == len(players):
                i = 0
            # Player
            p = players[i]
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            print("\nDEBUG", f"{p.username}'s stack: {p.stack}")
            print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            # BROKE NINJA CHECK:
            if p.stack < (self._curr_bet - p.last_bet):
                players.pop(i)
                i -= 1  # Offset to account for the auto increment in '# Close While-Loop'
                # Annouce Player Action 
                print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                print(": ", end='')
                print(f"{p.username}", end='')
                print(" does NOT have enough chips & ", end='')
                print(Fore.RED + "folds" + Style.RESET_ALL + ". ")
                print(f"{p.username}'s stack: ${p.stack}\n")
                continue
            # Human Player Turn:
            if p.is_hum:
                # Invalid Input Check:
                while True:
                    # Ask user for decision.
                    if bet_already_occurred:
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
                        print(Fore.LIGHTRED_EX + "Invalid input: Enter 'c', 'r', or 'f'.\n")
                    else:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        print(": ", end='')
                        print(Fore.CYAN + f"{p.username}", end='')
                        player_choice = input(", will you [c]heck, [b]bet, or [f]old? ")
                        if player_choice in ['Check', 'check', 'C', 'c', 'CHECK', '']:
                            ans = 'CHECK'
                            break
                        elif player_choice in ['Bet', 'bet', 'B', 'b', 'BET']:
                            ans = 'BET'
                            bet_already_occurred = True
                            break
                        elif player_choice in ['Fold', 'fold', 'F', 'f', 'FOLD']:
                            ans = 'FOLD'
                            break
                        print(Fore.LIGHTRED_EX + "Invalid input: Enter 'c', 'b', or 'f'.\n")

                # CALL:
                if ans == 'CALL':
                    # Update Caller Count
                    caller_count += 1
                    # Adjust Attributes
                    chips = self._curr_bet - p.last_bet
                    self._pot += chips
                    p.stack -= chips
                    p.last_bet = self._curr_bet
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Call. (your stack: ${p.stack})")
                    # Print Pot
                    print(f"Pot: ${self._pot}\n")
                
                # CHECK:
                elif ans == 'CHECK':
                    # Update Caller Count
                    caller_count += 1
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Check. (your stack: ${p.stack})")
                    # Print Pot
                    print(f"Pot: ${self._pot}\n")

                # RAISE or BET:
                elif ans in ['RAISE', 'BET']:
                    # Invalid Input Check:
                    while True:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        raise_amt = input(f": The current bet is ${self._curr_bet}. What will you raise it to? $")
                        if raise_amt.isdigit() and int(raise_amt) in range(self._curr_bet + 1, p.stack + 1):
                            break
                        print(Fore.LIGHTRED_EX + f"Invalid Input: The raise amount must be an integer from ${self._curr_bet + 1} (minimum raise) to ${p.stack} (your stack).\n")
                    # Update Caller Count
                    caller_count = 1
                    # Toss Chips Into Pot
                    chips =  int(raise_amt) - p.last_bet
                    p.stack -= chips
                    self._pot += chips
                    # Update Game Stats
                    self._curr_bet = int(raise_amt)
                    # Update Player Last Bet
                    p.last_bet = int(raise_amt)
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}", end='')
                    print(f" raised the bet from ${old_bet} to ${self._curr_bet}.")
                    # Print Pot
                    print(f"Pot: ${self._pot} (Your current stack: ${p.stack})\n")

                # FOLD:
                elif ans == 'FOLD':
                    players.pop(i)
                    i -= 1  # Offset to account for the increment in '# Close While-Loop'
                    # Annouce Player Action 
                    print("\n" + Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                    print(": ", end='')
                    print(f"{p.username}", end='')
                    print(" has ", end='')
                    print(Fore.RED + "folded" + Style.RESET_ALL + ". ")
                    print(f"{p.username}'s stack: ${p.stack}\n")

            # CPU Player Turn:
            elif p.is_cpu:
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
                # Update Caller Count
                caller_count += 1
                # Toss Chips Into Pot
                chips = self._curr_bet - p.last_bet
                self._pot += chips
                p.stack -= chips
                # Update Player Last Bet
                p.last_bet = self._curr_bet
                # Annouce Player Action 
                print(Fore.CYAN + f"{p.username}", end='')
                if chips == 0:
                    print(": Check.")
                else:
                    print(": Call.")
                # Print Pot
                print(f"Pot: ${self._pot}\n")
                # +--------------------------------------------------------+
                # |                       #TODO:                           |
                # |  Replace this `elif` branch later when the CPU player  |
                # |           algorithm has been implemented.              |
                # +--------------------------------------------------------+
            # Close While-Loop
            i += 1
            # DEBUGGGGGGGGGGGGGGGGGGGGG
            print("DEBUG", f"{p.username}'s stack: {p.stack}")
            print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGG

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
        username,         #TODO: Implement a recursive input babysitter.
        player_count,     #      This code is faulty. Currently, there's no
        buyin_amt,        #      recursion happening here. It breaks after two
        min_bet,          #      complete init prompt cycles.
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
    print("\n============== Proj_8: Texas Hold'em ==============\n")
    poker.e0_show_player_stats()
    print("\n============== Blind Bets ==============\n")
    poker.e1_blind_bet()
    print("\n============== Deal: POCKET CARDS ==============\n")
    poker.e2_deal_pocket()
    print("\n============== Bet (1/4): PRE-FLOP ==============\n")
    poker.e3_preflop()
    print("\n============== Deal: FLOP ==============\n")
    poker.e4_deal_flop()
    print("\n============== Bet(2/4): FLOP ==============\n")
    poker.e5_flop()
    print("\n============== Deal: TURN ==============\n")
    poker.e6_deal_turn()
    print("\n============== Bet(3/4): TURN ==============\n")
    poker.e7_turn()
    print("\n============== Deal: RIVER ==============\n")
    poker.e8_deal_river()
    print("\n============== Bet (4/4): RIVER ==============\n")
    poker.e9_river()
    print("\n============== SHOWDOWN ==============\n")
    # poker.e10_showdown()
    # poker.e11_reward_winner()
    # poker.e12_save_data()
    # poker.e13_shift_order()

    # And... Repeat.


if __name__ == '__main__':
    # try:
    #     run()
    # except:
    #     sys.exit('\n\n\n  [[ EXIT GAME ]]  \n  ---------------\n  keep ya head up\n')
    run()
