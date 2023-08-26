"""
Project_8: Texas Hold'em (v0.0.2)
=================================

Texas Hold'em Poker Q&A:
------------------------

Q: How many hole cards are dealt to each player in Texas Hold'em?
A: Each player is dealt two private hole cards.

Q: What are the betting rounds in Texas Hold'em?
A: Pre-flop, Flop, Turn, and River.

Q: What's the difference between "No Limit", "Pot Limit", and "Limit" Hold'em?
A: - "No Limit": Players can bet any amount, up to all their chips.
   - "Pot Limit": Maximum bet is the current pot size.
   - "Limit": Bets and raises are of a fixed amount.

Q: What is a "blinds" in poker?
A: Forced bets posted by players to the left of the dealer button. Includes "small blind" and "big blind".

Q: What is the "button" in poker?
A: A marker indicating the nominal dealer. It rotates clockwise after each hand.

Q: What does "All-in" mean?
A: A player bets all their remaining chips.

Q: What is a "community card"?
A: Cards placed face-up in the center, shared by all players to form their best hand.

Q: What happens when multiple players go "All-in"?
A: The pot is split into main and side pots. Players can only win from players they've covered in chips.

Q: What is a "kicker" in poker?
A: An unpaired card used to determine the winner between two similar hands.

Q: What is the "burn card"?
A: A card discarded from the top of the deck before dealing community cards.

Q: How is the winner determined in Texas Hold'em?
A: The player with the best five-card hand or the last player remaining after all others have folded.

Q: What is a "called player" in poker?
A: A player who has matched a bet/raise.

Q: What is an "aggresive player" in poker?
A: The player who initiated the last bet/raise.

Q: In the showdown, does the aggressor have the option to not show his cards?
A: Yes. If no one calls the last aggressor's bet, the aggressor can choose to
   muck (not show) their hand and still win the pot. If called, they must show.

Q: If the winner is determined before the showdown, must the winner reveal his
   cards?
A: No. If all players fold to a bet or raise, the winner can choose to muck
   their hand without revealing it.

Note: This is a basic list, and there are many more specific and nuanced questions players might have about Texas Hold'em.
"""
from __future__ import annotations
from typing import Any, Union, Optional
from enum import Enum
import random as rand
import sys

from playingcards import Card, Deck
import playingcards as pc


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
    def shuffle_ai_names() -> None:
        rand.shuffle(Ann.AI_NAMES)


class Player:
    """
    #TODO
    """
    # Attributes
    username: str
    stack: int
    hole_cards: list[Card, Card]
    curr_hand: list[Card, Card, Card, Card, Card]
    #
    is_you: bool
    is_hum: bool
    is_cpu: bool

    def __init__(self, is_hum: bool, username: str, stack: int, is_you=False) -> None:
        """
        #TODO
        """
        self.is_you = is_you
        if is_hum:
            self.is_hum = True
            self.is_cpu = False
        else:
            self.is_hum = False
            self.is_cpu = True
        self.username = username
        self.stack = stack
        self.hole_cards = []
        self.curr_hand = []


class Dealer:
    """
    The `Dealer` class contains all methods associated with handling cards.
    """
    # Attributes
    deck: Deck

    def __init__(self) -> None:
        """
        #TODO
        """
        self.deck = Deck()
    
    def new_deck(self) -> None:
        """
        Toss the old deck & initialize a new `Deck`.
        """
        self.deck = Deck()
    
    def shuffle_deck(self) -> None:
        """
        Shuffle the deck.
        """
        self.deck.shuffle()
    
    def draw_card(self) -> Card:
        """
        Draw a card from the top of the deck.
        """
        return self.deck.draw()


class PokerTable:
    """
    Use the `PokerTable` class to instantiate a game manager for a single
    buy-in. It provides a structure for the moving parts of poker in one place.
    It also collects stats from each hand.

    Assuming an abstract perspective, you should be able to "exit the current
    poker table with your winnings (or losses)" and instantiate a new instance
    of `PokerTable` that will, then, manage that new poker table with the
    minimum buy-in amount of your choice.
    """
    # Action Takers
    player_queue: list[Player]  # Use a queue to conveniently shift turn order.
    dealer: Dealer
    half_blind: int
    full_blind: int

    board: list[Card]
    burned_cards: list[Card]
    pot: int
    # stats: dict[str, Any]

    def __init__(self,
                 players: list[Player],
                 min_bet: int) -> None:
        """
        #TODO
        """
        rand.shuffle(players)
        self.player_queue = players  # Lowest index = left of the dealer
        self.dealer = Dealer()
        self.half_blind = min_bet // 2
        self.full_blind = min_bet
        self.board = []
        self.burned_cards = []
        self.pot = 0
        # self.stats = {'#KEY': '#VAL'}

    def show_player_order(self) -> None:
        """
        Phase 0: Print the turn order representation for user players to see.
        """
        pass

    def post_blinds(self) -> None:
        """
        Phase 1: Ask the small & big blinds to post their bets.
        """
        # Player actions
        small_blind = self.player_queue[0]
        small_blind.stack -= self.half_blind
        big_blind = self.player_queue[1]
        big_blind.stack -= self.full_blind
        # Update pot
        self.pot += self.half_blind + self.full_blind
        # Print results
        print(f'Player: {small_blind.username} posted ${self.half_blind}')
        print(f'Player: {big_blind.username} posted ${self.full_blind}')

    def deal_hole_cards(self) -> None:
        """
        Phase 2: Dealer deals hole cards to players.
        """
        for i in range(2):
            for player in self.player_queue:
                player.hole_cards.append(self.dealer.draw_card())
                if player.is_you and i == 1:
                    print(f'Your hole cards: {player.hole_cards}')

# -----------------------------------------------------------------------------

def event1_print_welcome_msg():
    """
    Event 1: Print welcome message.
    """
    print("\nFrom proj_Studio,\nWelcome to Project_8: Texas Hold'em, v0.0.2.")
    print("\nNote: Pressing 'ctrl + c' will exit the game.\n")
    print("\nThe game will be Texas Hold'em style poker. Let's get ready to play!\n")

def event2_request_table_info() -> tuple[str, int, int, int]:
    """
    Event 2: Request table info.
    """
    print("---------- TABLE SETUP ----------")
    username = input("    - Username: ")
    player_count = input("    - Number of seats: ")
    min_buyin = input("    - Minimum buy-in: $")
    min_bet = input("    - Minimum bet: $")
    print("---------------------------------")
    print("  ^")
    return username, int(player_count), int(min_buyin), int(min_bet)

def event2_re_request_table_info() -> tuple[str, int, int, int]:
    """
    Event 2: Request table info. Again.
    """
    print("---------- TABLE SETUP ----------")
    username = input("    - Username: ")
    player_count = input("    - Number of seats: ")
    min_buyin = input("    - Minimum buy-in: $")
    min_bet = input("    - Minimum bet: $")
    print("---------------------------------")
    print("  ^")

    ans = input("Proceed with these settings? (y/n) ")
    if ans in ['Y', 'y', 'Yes', 'yes', '']:
        print("\nLet's begin! Enjoy responsibly.\n")
        return username, int(player_count), int(min_buyin), int(min_bet)
    elif ans in ['N', 'n', 'No', 'no']:
        print("\nNo worries. Let's get our table set up again.\n")
        return event2_re_request_table_info()
    else:
        print("Invalid input. To confirm your Hold'em table settings, input 'y' or 'n' and hit enter.\n")
        event3_table_confirmation()

def event3_table_confirmation() -> bool:
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
        event3_table_confirmation()

def event4_init_user_player(username: str, stack: int) -> Player:
    """
    Init and return the user `Player` instance.
    """
    return Player(True, username, stack, is_you=True)

def event5_init_cpu_players(num_cpu: int, stack: int) -> list[Player]:
    """
    Init and return a list of CPU `Player` instances.
    """
    Ann.shuffle_ai_names()
    return [Player(False, username, stack) for username in Ann.AI_NAMES[:num_cpu]]

def event6_init_poker_table(players: list[Player], min_bet: int) -> PokerTable:
    """
    Init and return an instance of `PokerTable`.
    """
    return PokerTable(players, min_bet)

# As a coding exercise, limit yourself only to these functions above.
# The rest of the code should be as "procedural" as you can help it to be, by
# using the variables.
#     This is the fun part. Get the functions implemented and over with.

def proj_8():
    """
    Project_8: Texas Hold'em.
    -------------------------
    Keep it simple, stupid.
    """
    # +----------------------------------------------------------------------+
    # |                                                                      |
    # |   TODO: Implement credential system & prompt user authentication.    |
    # |                                                                      |
    # +----------------------------------------------------------------------+

    event1_print_welcome_msg()

    (
    username,
    player_count,
    min_buyin,
    min_bet
    ) = event2_request_table_info()

    if not event3_table_confirmation():
        (
        username,
        player_count,
        min_buyin,
        min_bet
        ) = event2_re_request_table_info()

    players = [event4_init_user_player(username, min)] + event5_init_cpu_players(player_count - 1, min_buyin) 
    poker = event6_init_poker_table(players, min_bet)

    poker.post_blinds()
    poker.deal_hole_cards()

    # def shuffle_deck(self)

    # def small_blind(self)
    # def big_blind(self)

    # def deal(self)
    # def betting_round_1(self)

    # def burn_card(self)
    # def flop_card(self)
    # def betting_round_2(self)

    # def burn_card(self)
    # def turn_card(self)
    # def betting_round_3(self)

    # def burn_card(self)
    # def river_card(self)
    # def betting_round_4(self)

    # ..if at showdown phase:
    #     def reveal_aggressor_hand(self)
    #     ..if there's a better hand:
    #         def reveal_best_hand(self)
    # def let_show_or_muck(self)

    # def rake(self)
    # def award_winner(self)

    # def shift_turn_order_queue(self)
    # LOOP-BACK: def shuffle_deck(self)


if __name__ == '__main__':
    import doctest; doctest.testmod()
    try:
        proj_8()
    except KeyboardInterrupt:
        sys.exit("\n\n[[ Exiting Game ]]\n\nHave a nice day! Remember: Learn to forgive yourself.\n")














def proj_8_ARCHIVED_ON_AUGUST_23_2023():
    """
    Run Project_8: Texas Hold'em.

    __Dev Game Plan:
    ----------------
    - Played thru console I/O.
    - By default, 

    Hold'em Rules:
    --------------
    1. The turn order moves in the clockwise direction.
    2. In "self-deal" games, the dealer button moves from hand to hand, to each
    player, to whom it assigns the dealer duty for the hand about to begin.
    3. In a cash game, the small blind bets $1, and the big blind bets $2.
    4. In the first betting round, the first raise must be at least twice the
    minimum bet. Note: after the first raise, each subsequent player's call
    size is the most recent amount raised, and no longer the minimum bet.
    5. Starting from the second betting round, the turn order now starts from
    the player to the left of the dealer. Also, players can now "check" as long
    as the bet has not been raised by anyone. However, if the bet is raised,
    the three player options boil back down to "call", "raise", or "fold".


    Hold'em Terms:
    --------------
     - Hand: the best combination of five out of the seven total cards a
             player can claim.
     - Hole cards: private cards owned by all players.
     - Board: area in which five community cards lay.
     - Aggressor: the player who initiated the last bet/raise.
    """
    # Event: Greeting message
    print("\nWelcome to Project_8: Texas Hold'em, by proj_Studio.")
    print("--v0.0.1\n")
    print("The game will be Texas Hold'em style poker. Let's get ready to play!\n")

    # Event: Initialize your username.
    print("Enter your username: ", end='')
    username: str = input()
    #        Initialize Player class.


    # Event: Enter the number of players.
    print("Set the number of players (from 2 to 10): ", end='')
    num_players: int = int(input())

    # Event: Enter the minimum bet.
    print("Set the minimum buy-in amount: $", end='')
    min_buy_in: int = int(input())
    print("Set the minumum bet amount for each hand: $", end='')
    min_bet: int = int(input())

    # Event: Confirmation prompt.
    print("\nNice. Here's a summary of your hold'em game:")
    print("--------------------------------------------")
    print("Players:")
    print(f"    player_1: {username} (You)")
    for n in range(min(10, num_players) - 1):
        print(f"    ai_{n + 2}: {ai_names[n]}")
    print()
    print(f"Minimum buy-in amount:\n    ${min_buy_in}\n")
    print(f"Minimum bet amount:\n    ${min_bet}")
    print("--------------------------------------------")
    print("Is this correct? [y]es, or [n]o? ", end='')
    temp_str = input()
    ready_to_proceed = None
    if temp_str in ['y', 'Y', 'yes', 'Yes']:
        ready_to_proceed = True
    elif temp_str in ['n', 'N', 'no', 'No']:
        ready_to_proceed = False

    # Event: User answer to confirmation prompt.
    if not ready_to_proceed:
        print('\nyou must train harder son\n')
        exit()

    # Event: * BEGIN GAME *
    print("\nCool, let's begin. Shuffle up and deal!\n")
    deck = pc.Deck()
    print(f"{username}'s Cards:")
    print(f"    {deck.draw()}")
    print(f"    {deck.draw()}\n")
    print("Community Cards:")
    print(f"    {deck.draw()}")
    print(f"    {deck.draw()}")
    print(f"    {deck.draw()}")
    print(f"    {deck.draw()}")
    print(f"    {deck.draw()}")
    # Event: Assign the dealer
    #TODO: Write logic for assigning dealer duties
    print("\nexit game\n")

    # Event: Blind bets (to the dealer's left: small blind, big blind)
    # Event: Dealer deals 2 hole cards to each player, starting w/ one card
    #        each & from the dealer's left
    # Event: 1st betting round
    # Event: Dealer reveals 3 community [Flop] cards
    # Event: 2nd betting round
    # Event: Dealer reveals the community [Turn] card
    # Event: 3rd betting round
    # Event: Dealer reveals the community [River] card
    # Event: Final betting round
    # Optional Event: Move to the Showdown
    # Optional Event: The aggressor (i.e., the last player to make an
    #                 aggressive action, i.e., bet or raise) during the final
    #                 betting round MUST show their hand first
    # Optional Event: Other players choose to either show their hand to contest
    #                 the pot, or muck (discard w/o showing) in turn order
    # Optional Event: Move to the Winner's Choice
    #                 I.e., if a player's hand is uncontested (no one calls
    #                       their final bet/raise), they can choose to show or
    #                       muck
    # Event: Award the pot to the best hand shown OR split the pot among equal
    #        hands
    # Event: Prompt "Continue?" If (n)o, exit `proj_8`
    # Event: Else, assign the new dealer based on the last turn order
    # Event: Loop from "Event: * BEGIN GAME * "" until Player quits the game
    # Event: If Player quits the game, greet out & print some food for thought
    #
    # Optional Event: print error message (for whatever reason)
    #
