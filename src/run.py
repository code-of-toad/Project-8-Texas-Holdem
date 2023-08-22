"""
This module contains all imports, constants, variables, functions, classes and
methods required to run Project_8: Texas Hold'em, v0.0.1
"""
from __future__ import annotations
from typing import Any, Union, Optional

import playingcards as pc


class GameOfPoker:
    """
    A static class designed to handle game events for Project_8: Texas Hold'em.
    """
    pass


def proj_8():
    """
    Run Project_8: Texas Hold'em.

    __Dev Game Plan:
    ----------------
    - Played on the output console of choice by showing inputs 
    - Holdem rules apply
    - 
    """
    # Event: Greeting message
    # Event: Init prompts--How many players, minimum buy-in, minimum bet, etc.
    # Event: Confirmation prompt
    # Event: * BEGIN GAME *
    # Event: Assign the dealer
    # Event: Blind bets
    # Event: Dealer deals 2 cards to each player
    # Event: Pre-Flop betting round
    # Event: Dealer reveals 3 community [Flop] cards
    # Event: [Flop] betting round
    # Event: Dealer reveals the community [Turn] card
    # Event: [Turn] betting round
    # Event: Dealer reveals the community [River] card
    # Event: [River] betting round
    # Optional Event: Move to the Showdown
    # Optional Event: Called player (the last player to make an aggressive
    #                 action, i.e., bet or raise) during the final betting
    #                 round must show their hand first
    # Optional Event: Other players choose to either show their hand to contest
    #                 the pot, or muck (discard w/o showing) in turn order
    # Optional Event: Move to the Winnder's Choice
    #                 I.e., if a player's hand is uncontested (no one calls
    #                       their final bet/raise), they can choose to show or
    #                       muck
    # Optional Event: Award the pot to the best hand shown or split the pot
    #                 for equal hands
    # Event: Prompt "Continue?" If (n)o, exit `proj_8`
    # Event: Else, Assign the new dealer based on the last turn order
    # Event: Loop until Player quits the game
    # Event: print food for thought
    # Optional Event: print error message (for whatever reason)


if __name__ == '__main__':
    proj_8()
