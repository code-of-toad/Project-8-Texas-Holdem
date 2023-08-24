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


class ANN:
    """
    Dev assistant that carries cool constants and static methods.
    """
    @staticmethod
    def get_ai_list():
        ai_list = ['Mr. Johnson', 'Eng Mo', 'Shashta', 'Ishmael', 'Jesse',
                   'xXgregXx', 'citizen_sane', 'codge', 'Elvis', 'Cat', 'Dog',
                   'Monkey', 'neand69', 'ManBearPig', 'Team-O', 'j0ker',
                   'Bavid Dlaine', 'Uncle Wong', 'IT', 'Shrek', 'Donkey',
                   'Sill Wmith', 'a bicycle', 'a unicycle', '뛰는놈', '나는놈',
                   '아는놈', '새', 'Chicken', 'Bread', 'Onion', 'Cheese', 'a']
        rand.shuffle(ai_list)
        return(ai_list)


class PokerTable():
    """
    Use the `PokerTable` class to instantiate a game manager for a single
    buy-in.

    This class is designed to be an emulation of a real-scenario poker table,
    w/ moving parts (i.e., players, cards, dealer, pot). That way, debugging
    logic becomes easier.

    In other words, you should be able to "exit the current poker table with
    your winnings (or losses)" and instantiate a new instance of `PokerTable`
    that will, then, manage that new poker table with the minimum buy-in amount
    of your choice.
    """
    # Individuals
    players: list[Player]
    dealer: Dealer
    # Cards
    board: list[Card]
    burned_cards: list[Card]
    # Pot
    pot: int


class Dealer():
    """
    Duties:
    -------
    0.1. Speaks to the players; e.g., announcing hands in the showdown, etc.
    0.2. Assigns the small blind and the big blind.
    1. Shuffles the deck of cards.
    2. Deals hole cards to players one at a time & starting from the left.
    3. Burns a card before revealing each of the flop, turn, and river cards
    for a maximum total of three times per hand.
    4. Collects rake.
    5. Repeat
    """


class Player():
    """
    """
    best_hand: list[Card]


class Ai():
    """
    """


class User():
    """
    """


def proj_8():
    """
    Project_8: Texas Hold'em.
    -------------------------
    Keep it simple, stupid.
    """
    print('\n---------------DeBuG---------------Scope-------proj_8()\n')
    print("\nWelcome to Project_8: Texas Hold'em, by proj_Studio.")
    print("--v0.0.2\n")
    print("The game will be Texas Hold'em style poker. Let's get ready to play!\n")


if __name__ == '__main__':
    proj_8()
    sys.exit()


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
        print(f"    ai_{n + 2}: {ai_list[n]}")
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
