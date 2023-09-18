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
                'bavid blaine', 'Uncle Wong', 'Shrek', 'Donkey', 'Mrs. Lemon',
                'Will', 'Bike', 'Unicycle', '뛰는놈', '나는놈', 'Mr. 8east',
                '아는놈', '새', 'Chicken', 'Bread', 'Onion', 'Cheese', 'a']
    class POKER_HAND_RANKING(Enum):
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

    @staticmethod
    def bubble_sort(lst: list[Any]) -> list[Any]:
        """
        Return a sorted version of `lst`, from highest to lowest,
        from left to right.

        NOTE: This method does NOT mutate the arg list.

        NOTE: All items in `lst` must be data types whose `__lt__`, `__gt__`,
        `__eq__`, `__le__`, `__ge__` methods are defined in relation to each
        other.
        """
        retlst = lst.copy()
        for _ in range(len(retlst)-1):
            i = 0
            j = 1
            for _ in range(len(retlst)-1):
                # print('DEBUGGGGGGGGGGGGGG', i, j)
                if retlst[i] < retlst[j]:
                    retlst.insert(i, retlst.pop(j))
                i += 1
                j += 1
        return retlst


class Dealer:
    name: str
    deck: Deck

    def __init__(self, name: str) -> None:
        self.name = name
        self.deck = Deck()

    def draw(self) -> Card:
        return self.deck.draw()

    def new_deck(self) -> None:
        """
        Equip this dealer with a brand-new shuffled deck.
        """
        self.deck = Deck()


class Player:
    # Player Cards
    hole_cards: list[Card, Card]
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

    def __eq__(self, other: Player) -> bool:
        if isinstance(other, Player):
            return self.username == other.username
        return False

    def get_best_hand(self, community_cards: list[Card]) -> dict:
        """
        Designed to be called by `PokerGame.e10_showdown()`.

        Texas Hold'em: Hands
        --------------------
        10. Royal Flush
        9. Straight Flush
        8. Four of a Kind
        7. Full House
        6. Flush
        5. Straight
        4. Three of a Kind
        3. Two Pair
        2. Pair
        1. High Card

        __Dev Notes
        -----------
        Let the `int` representation of a card's rank be an integer member of
        the set [2, 14], where:  1 = "Ace",
                                 2 = "2",
                                10 = "10",
                                13 = "King".
        This is done to reduce the number of edge cases that must be
        implemented if "Ace" were to be assigned to the `int` value, 1.
        """
        cards_pre = [c for c in community_cards] + self.hole_cards
        cards: tuple[Card] = tuple(Ann.bubble_sort(cards_pre))
        suit_count: dict[str, int] = {suit: 0 for suit in Ann.SUITS_STR}
        rank_count: dict[int, int] = {rank: 0 for rank in range(1, 14)}
        for c in cards:
            # Count collection of suits.
            suit_count[c.get_suit()] += 1
            # Count collection of ranks.
            rank_count[c.get_rank_int()] += 1


        # Prep Crew
        # =========
        # Condition: Flush
        cnd_flush: bool = False
        flush_suit: Optional[str] = None
        for suit, count in suit_count.items():
            if count == 5:
                cnd_flush = True
                flush_suit = suit
        # Condition: Four of a Kind
        cnd_foak: bool = False
        foak_rank: Optional[int] = None
        for rank, count in rank_count.items():
            if count == 4:
                cnd_foak = True
                foak_rank = rank
        # Condition: Three of a Kind
        cnd_toak: bool = False
        toak_rank: Optional[int] = None
        for rank, count in rank_count.items():
            if count == 3:
                if not cnd_toak:
                    cnd_toak = True
                    toak_rank = rank
                else:
                    toak_rank = rank if (rank == 1 or toak_rank < rank) else toak_rank
        # Condition: Two Pair and/or Pair
        cnd_pair1: bool = False
        cnd_pair2: bool = False
        pair_ranks: list[int] = []
        for rank, count in rank_count.items():
            if count == 2:
                # update `pair_ranks` list
                pair_ranks.append(rank).reverse()
                # move the Ace (rank == 1) to the front (index == 0)
                if pair_ranks[-1] == 1:
                    pair_ranks.insert(0, pair_ranks.pop())
                # if no pair has been seen yet
                if not cnd_pair1:
                    cnd_pair1 = True
                else:
                    cnd_pair2 = True


        # ----------------------------- INVENTORY -----------------------------
        #
        #  cards: list[Card]
        #     :
        #     +---> Contains all 7 cards in descending order.
        #
        #  suit_count: dict[str, int]
        #     :
        #     +---> Counts how many of each suit are present in `cards`.
        #
        #  rank_count: dict[int, int]
        #     :
        #     +---> Counts how many of each rank are present in `cards`.
        #           NOTE: 13 = 'King'
        #                 10 = '10'
        #                  2 = '2'
        #                  1 = 'Ace'
        #
        #  cnd_flush: bool
        #  cnd_foak: bool
        #  cnd_toak: bool
        #  cnd_pair2: bool
        #  cnd_pair1: bool
        #
        #  flush_suit: Optional[str]
        #  foak_rank: Optional[int]
        #  toak_rank: Optional[int]
        #  pair_ranks: list[int]
        #
        # ---------------------------------------------------------------------

        # Determine Hands
        # ===============
        if cnd_flush:
            """
            Check for:
               10. Royal Flush
                9. Straight Flush
                6. Flush
            """
            # ---------------
            # 10. Royal Flush
            #
            # Test Cases:
            # -----------
            # success
            # - [ace-A, king-A, queen-A, jack-A, 10-A, ---, ---]
            # - [ace-A, ace--, queen-A, jack-A, 10-A, ---, ---]
            # failure
            # - [ace-S, ace-H, ace-D, ace-C, ---, ---, ---] 
            # - [ace-A, ace-B, ace-C, king-B, queen-B, jack-B, 10-C] 
            # - [ace-A, king-A, queen-A, 5-A, 4-A, 3-A, 2-A]
            # ---------------
            ## card: list[Card*7], descending order
            royal_flush: list[Card] = []
            kickers: list[Card] = []

            # Iterate thru `cards` to generate your hand.
            i_count: int = 0

            # Check each of the seven `cards` one at a time.
            for c in cards:
                # No `flush suit` card has been detected yet.
                # if royal_flush == []
                if i_count == 0: 
                    if c.get_rank_str() == 'Ace' and c.get_suit() == flush_suit:
                        royal_flush.append(c)
                    else:
                        kickers.append(c)
                # elif royal_flush == [Ace]
                elif i_count == 1:
                    if c.get_rank_str() == 'King' and c.get_suit() == flush_suit:
                        royal_flush.append(c)
                    else:
                        kickers.append(c)
                # elif royal_flush == [Ace, King]
                elif i_count == 2:
                    if c.get_rank_str() == 'Queen' and c.get_suit() == flush_suit:
                        royal_flush.append(c)
                    else:
                        kickers.append(c)
                # elif royal_flush == [Ace, King, Queen]
                elif i_count == 3:
                    if c.get_rank_str() == 'Jack' and c.get_suit() == flush_suit:
                        royal_flush.append(c)
                    else:
                        kickers.append(c)
                # elif royal_flush == [Ace, King, Queen, Jack]
                elif i_count == 4:
                    if c.get_rank_str() == '10' and c.get_suit() == flush_suit:
                        royal_flush.append(c)
                    else:
                        kickers.append(c)
                # elif royal_flush == [Ace, King, Queen, Jack, 10]
                else:
                    kickers.append(c)
                # Update iterator.
                i_count += 1

            # Final Check: Royal Flush
            if i_count == 5:
                return {'hand_rank': 10,
                        'hand_type': royal_flush,
                        'kickers': kickers}

            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
            print()
            pprint(royal_flush)
            pprint(kickers)
            print()
            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG

            # -----------------
            # 9. Straight Flush
            #
            # Test Cases:
            # -----------
            # success
            # - [jack-A, 10-A, 9-A, 8-A, 7-A, ---, ---]
            # - [---, jack-A, 10-A, 9-A, 8-A, 7-A, ---]
            # - [---, ---, jack-A, 10-A, 9-A, 8-A, 7-A]
            # - [ace-A, king-A, queen-A, 5-A, 4-A, 3-A, 2-A]
            # failure
            # - [jack-A, 10-A, 9-A, 8-C, 7-C, 6-C, 5-C]
            # -----------------
            ## card: list[Card*7], descending order
            str8_flush: list[Card] = []
            kickers: list[Card] = []
            flush_cards: list[Card] = [c for c in cards if c.get_suit() == flush_suit]

            # Update iterator.
            i_count: int = 0
            last_rank: int
            # Analyze each card, then append them to either `kickers` or `hand`
            for c in cards:
                # EZ-variables
                c_rank: int = c.get_rank_int()
                c_suit: str = c.get_suit()
                # if card == WRONG suit || len(str8_flush) == 5
                if c_suit != flush_suit or i_count == 5:
                    kickers.append(c)
                # Now, all following elif-branches run for CORRECT card suit.
                #
                # elif str8_flush == [5, 4, 3, 2 ]
                elif i_count == 4 and last_rank == 2:
                    if flush_cards[0].get_rank_str == 'Ace':
                        flush.append(flush_cards[0])
                        last_rank = 1
                        i_count += 1
                # elif str8_flush == [ ] && c_rank == 'Ace'
                elif i_count == 0 and c.get_rank_str() == 'Ace':
                    str8_flush.append(c)
                    last_rank = 14
                    i_count += 1
                # elif str8_flush == [ ]
                elif i_count == 0:
                    str8_flush.append(c)
                    last_rank = c_rank
                    i_count += 1
                # elif 1 <= len(str8_flush) <= 4
                elif c_rank == last_rank - 1:
                    str8_flush.append(c)
                    last_rank = c_rank
                    i_count += 1

            # Final Check: Royal Flush
            if i_count == 5:
                return {'hand_rank': 9,
                        'hand_type': str8_flush,
                        'kickers': kickers}


            # --------
            # 6. Flush
            # --------
            ## card: list[Card*7], descending order
            flush: list[Card] = []
            kickers: list[Card] = []

            # Update iterator.
            i_count: int = 0
            last_rank: str = ''
            # Analyze each card, then append them to either `kickers` or `hand`
            for c in cards:
                # EZ-variables
                c_rank: int = c.get_rank_int()
                c_suit: str = c.get_suit()
                # if 1 <= len(flush) <= 5
                if len(flush) < 5:
                    flush.append(c)
                    i_count += 1
                else:
                    kickers.append(c)

            # Final Check: Flush
            if i_count == 5:
                return {'hand_rank': 6,
                        'hand_type': flush,
                        'kickers': kickers}

        else:
            """
            #todo
                8. Four of a Kind
                7. Full House
                5. Straight
                4. Three of a Kind
                3. Two Pair
                2. Pair
                1. High Card
            """
            pass


def print_card(card: Card) -> None:
    if card.is_blk():
        print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f"  {card}  ", end='')
    elif card.is_red():
        print(Style.BRIGHT + Back.WHITE + Fore.RED + f"  {card}  ", end='')


class PokerGame:
    # Active "Participants"
    _dealer: Dealer  # never changes
    # If size must be reduced, the next two lists MUST UPDATE SIMULATANEOUSLY.
    _players_queue: list[Player]            # When game is over, replace this w/ the one below.
    _next_game_players_queue: list[Player]  # Remove players ONLY when a player cashes out of the table.
    # Physical Aspects
    _pot: int
    _burn_cards: list[Card]
    _comm_cards: list[Card]
    # Game Info
    _curr_bet: int
    _last_aggressor: Player
    # _total_seats: int    # decrement everytime a player cashes out
    _big_blind: int
    _sml_blind: int
    _buyin_amt: int
    _hands_played: int   # increment everytime a game ends successfully

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
        self._last_aggressor = None
        # self._total_seats = len(players_list)
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
        # P0
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
        # print("DEBUG", f"{p0.username}'s stack: {p0.stack}")
        # print("DEBUG", f"{p0.username}'s last bet: {p0.last_bet}")
        # print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
        print(": ", end='')
        print(Fore.CYAN + f"{p0}", end='')
        print(f" posted a small blind bet of ${sml_blind}.\n")
        p0.stack -= sml_blind
        p0.last_bet = sml_blind
        self._pot += sml_blind
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
        # print("DEBUG", f"{p0.username}'s stack: {p0.stack}")
        # print("DEBUG", f"{p0.username}'s last bet: {p0.last_bet}")
        # print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
        # P1
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
        # print("\nDEBUG", f"{p1.username}'s stack: {p1.stack}")
        # print("DEBUG", f"{p1.username}'s last bet: {p1.last_bet}")
        # print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
        print(": ", end='')
        print(Fore.CYAN + f"{p1}", end='')
        print(f" posted a big blind bet of ${big_blind}.\n")
        p1.stack -= big_blind
        p1.last_bet = big_blind
        self._pot += big_blind
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
        # print("DEBUG", f"{p1.username}'s stack: {p1.stack}")
        # print("DEBUG", f"{p1.username}'s last bet: {p1.last_bet}")
        # print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
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

    def e3_preflop(self) -> Optional[bool]:
        # EZ-Variables
        players: list[Player] = self._players_queue
        old_bet: int = self._curr_bet
        dealer: str = self._dealer.name
        # Go thru each player, and continue until every player has called/folded.
        caller_count = 0
        i = 2
        while caller_count < len(players):
            # If only one player remains, reward the pot to the winner.
            if len(players) == 1:
                winner = players[0]
                print("\n" + Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                print(": ", end='')
                print(f"{winner}", end='')
                print(" is the only player remaining. ", end='')
                print(Fore.CYAN + f"{winner}" + Style.RESET_ALL + " is the winner! :)")
                print(Fore.CYAN + f"{winner}" + Style.RESET_ALL + " claims the pot of ", end='')
                print(Fore.GREEN + Style.BRIGHT + f"${self._pot}" + Style.RESET_ALL + ".")
                winner.stack += self._pot
                self._pot = 0
                print(f"{p.username}'s Stack: ${p.stack}\n")
                return False
            # Valid Index Check
            if i == len(players):
                i = 0
            # Player
            p = players[i]
            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
            # print("\nDEBUG", f"{p.username}'s stack: {p.stack}")
            # print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            # print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
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
                    print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                    print(": ", end='')
                    print(Fore.CYAN + f"{p.username}", end='')
                    player_choice = input(", will you [c]all, [r]aise, or [f]old? ")
                    if player_choice in ['Call', 'call', 'C', 'c', 'CALL', '']:
                        ans = 'CALL'
                        break
                    elif player_choice in ['Raise', 'raise', 'R', 'r', 'RAISE']:
                        # Broke Ninja Check:
                        if p.stack <= self._curr_bet - p.last_bet:
                            print(Fore.LIGHTRED_EX + "You have no chips left to raise the bet :(\n") 
                        # Good to proceed.
                        else:
                            ans = 'RAISE'
                            break
                    elif player_choice in ['Fold', 'fold', 'F', 'f', 'FOLD']:
                        ans = 'FOLD'
                        break
                    else:
                        print(Fore.LIGHTRED_EX + "Invalid Input: Enter 'c', 'r', or 'f'.\n")

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
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Call.")
                    # Print Pot
                    print(f"Pot: ${self._pot} (Your Stack: ${p.stack})\n")

                # RAISE:
                elif ans == 'RAISE':
                    # Invalid Input Check:
                    while True:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        raise_amt = input(f": The current bet is ${self._curr_bet}. What will you raise it to? $")
                        if raise_amt.isdigit() and int(raise_amt) in range(self._curr_bet + 1, (p.stack + 1) + p.last_bet):
                            break
                        print(Fore.LIGHTRED_EX + f"Invalid Input: The raise amount must be an integer from ${self._curr_bet + 1} (minimum raise) to ${p.stack + p.last_bet} (your maximum raise).\n")
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
                    print(f"Pot: ${self._pot} (Your stack: ${p.stack})\n")

                # FOLD:
                elif ans == 'FOLD':
                    players.pop(i)
                    i -= 1  # Offset to account for the increment in '# Close While-Loop'
                    # Annouce Player Action 
                    print("\n" + Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                    print(": ", end='')
                    print(Fore.CYAN + f"{p.username}", end='')
                    print(" has ", end='')
                    print(Fore.RED + "folded" + Style.RESET_ALL + ". ")
                    print(f"{p.username}'s Stack: ${p.stack}\n")

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
            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
            # print("DEBUG", f"{p.username}'s stack: {p.stack}")
            # print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            # print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
        # Print Pot
        print(Fore.GREEN + f"\nPot (Pre-Flop): ${self._pot}\n")

    def e4_deal_flop(self):
        self._handle_deals(flop=True)

    def e5_flop(self) -> Optional[bool]:
        return self._handle_flop_turn_river(round='Flop')

    def e6_deal_turn(self):
        self._handle_deals()

    def e7_turn(self) -> Optional[bool]:
        return self._handle_flop_turn_river(round='Turn')

    def e8_deal_river(self):
        self._handle_deals()

    def e9_river(self) -> Optional[bool]:
        return self._handle_flop_turn_river(round='River')

    def e10_showdown(self):
        """Handle the showdown phase and reward pot to the winner."""
        # EZ-Variables
        last_aggressor = self._last_aggressor
        # Edge Case
        if last_aggressor is None:
            # Start comparing hands starting from player left to the dealer.
            pass
        # 1. Collect a list of players who hold the highest-ranking hand.
        pass
        # 2. Show the last aggressor's hand. 
        pass
        # 3. If the next-turn player has a better hand, show the hand.
        pass
        # 4. Otherwise, give the next-turn player a choice to Show/Muck.
        pass
        # 5. Determine the winner(s).
        pass
        # 6. Reward the winner(s).
        pass

    def e11_save_data(self):
        """Save data locally."""
        # Update game info.
        self._hands_played += 1
        # Save data locally.
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
        self._DEBUG()
        # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG

    def _DEBUG(self) -> None:
        """DEBUG"""
        print('DEBUGGGGGGGGGGGGG at `e11_save_data()`', self._hands_played)

        print()
        pprint(self._comm_cards)
        print()
        for player in self._players_queue:
            if player.is_hum:
                pprint(self._comm_cards + player.hole_cards)
                print()
        pprint(self._players_queue)

    def e12_prep_next_game(self):
        """Reset this instance of `PokerGame` for the upcoming new hand."""
        # Give dealer a brand-new shuffled deck for the next hand.     
        self._dealer.new_deck()
        # Reset the player queues.
        players_list_1 = self._next_game_players_queue.copy()
        players_list_2 = self._next_game_players_queue.copy()
        self._players_queue = players_list_1
        players_list_2.append(players_list_2.pop(0))
        self._next_game_players_queue = players_list_2
        # Reset public cards.
        self._burn_cards = []
        self._comm_cards = []
        # Reset game stats.
        self._curr_bet = self._big_blind
        self._last_aggressor = None
        # Reset each player's attributes.
        for p in self._players_queue:
            p.hole_cards = []
            p.last_bet = 0

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

    def _handle_deals(self, flop=False):
        # EZ-Variables
        dealer: Dealer = self._dealer
        burn_cards: list[Card] = self._burn_cards
        comm_cards: list[Card] = self._comm_cards
        # Common Logic
        burn_cards.append(dealer.draw())
        if flop:
            # Dealer ACtion
            for _ in range(3):
                comm_cards.append(dealer.draw())
            print(Fore.LIGHTMAGENTA_EX + f"{dealer.name}" + Style.RESET_ALL + " \
burns a card & reveals three community cards on the board:\n\
-----------------------------------------------------------------\n")
        else:
            # Dealer ACtion
            comm_cards.append(dealer.draw())
            print(Fore.LIGHTMAGENTA_EX + f"{dealer.name}" + Style.RESET_ALL + " \
burns a card & reveals another community card on the board:\n\
------------------------------------------------------------------\n")
        # Display Community Cards
        for card in comm_cards:
            print("  ", end='')
            print_card(card)
        print()
        print()
        # Display Player Cards
        self._display_hum_cards()

    def _handle_flop_turn_river(self, round: str) -> Optional[bool]:
        """
        Helper handler method called by:
          1. `self.e5_flop()`
          2. `self.e7_turn()`
          3. `self.e9_river()`
        
        Return `False` if only one player remains BEFORE the showdown is
        reached. Otherwise, return `None`.

        Features:
          - 'CALL' or 'CHECK'
          - 'RAISE' or 'BET'
        """
        # Error Check
        if round not in ['Flop', 'Turn', 'River']:
            raise Exception('u good?')
        # EZ-Variables
        players: list[Player] = self._players_queue
        dealer: str = self._dealer.name
        old_bet: int = self._curr_bet
        # Go thru each player, and continue until every player has called/folded.
        bet_already_occurred: bool = False
        caller_count = 0
        i = 0
        while caller_count < len(players):
            # If only one player remains, reward the pot to the winner.
            if len(players) == 1:
                winner = players[0]
                print("\n" + Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                print(": ", end='')
                print(f"{winner}", end='')
                print(" is the only player remaining. ", end='')
                print(Fore.CYAN + f"{winner}" + Style.RESET_ALL + " is the winner! :)")
                print(Fore.CYAN + f"{winner}" + Style.RESET_ALL + " claims the pot of ", end='')
                print(Fore.GREEN + Style.BRIGHT + f"${self._pot}" + Style.RESET_ALL + ".")
                winner.stack += self._pot
                self._pot = 0
                print(f"{p.username}'s Stack: ${p.stack}\n")
                return False
            # Valid Index Check
            if i == len(players):
                i = 0
            # Player
            p = players[i]
            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
            # print("\nDEBUG", f"{p.username}'s stack: {p.stack}")
            # print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            # print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
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
                            # Broke Ninja Check:
                            if p.stack <= self._curr_bet - p.last_bet:
                                print(Fore.LIGHTRED_EX + "You have no chips left to raise the bet :(\n") 
                            # Good to proceed.
                            else:
                                ans = 'RAISE'
                                break
                        elif player_choice in ['Fold', 'fold', 'F', 'f', 'FOLD']:
                            ans = 'FOLD'
                            break
                        else:
                            print(Fore.LIGHTRED_EX + "Invalid Input: Enter 'c', 'r', or 'f'.\n")
                    else:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        print(": ", end='')
                        print(Fore.CYAN + f"{p.username}", end='')
                        player_choice = input(", will you [c]heck, [b]et, or [f]old? ")
                        if player_choice in ['Check', 'check', 'C', 'c', 'CHECK', '']:
                            ans = 'CHECK'
                            break
                        elif player_choice in ['Bet', 'bet', 'B', 'b', 'BET']:
                            # Broke Ninja Check:
                            if p.stack <= self._curr_bet - p.last_bet:
                                print(Fore.LIGHTRED_EX + "You have no chips left to raise the bet :(\n") 
                            # Good to proceed.
                            else:
                                ans = 'BET'
                                bet_already_occurred = True
                                break
                        elif player_choice in ['Fold', 'fold', 'F', 'f', 'FOLD']:
                            ans = 'FOLD'
                            break
                        else:
                            print(Fore.LIGHTRED_EX + "Invalid Input: Enter 'c', 'b', or 'f'.\n")

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
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Call.")
                    # Print Pot
                    print(f"Pot: ${self._pot} (Your Stack: ${p.stack})\n")

                # CHECK:
                elif ans == 'CHECK':
                    # Update Caller Count
                    caller_count += 1
                    # Annouce Player Action 
                    print("\n" + Fore.CYAN + f"{p.username}" + Style.RESET_ALL + f": Check.")
                    # Print Pot
                    print(f"Pot: ${self._pot} (Your Stack: ${p.stack})\n")

                # RAISE or BET:
                elif ans in ['RAISE', 'BET']:
                    # Invalid Input Check:
                    while True:
                        print(Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                        raise_amt = input(f": The current bet is ${self._curr_bet}. What will you raise it to? $")
                        if raise_amt.isdigit() and int(raise_amt) in range(self._curr_bet + 1, (p.stack + 1) + p.last_bet):
                            break
                        if ans == 'RAISE':
                            print(Fore.LIGHTRED_EX + f"Invalid Input: The raise amount must be an integer from ${self._curr_bet + 1} (minimum raise) to ${p.stack + p.last_bet} (your maximum raise).\n")
                        elif ans == 'BET':
                            print(Fore.LIGHTRED_EX + f"Invalid Input: The bet amount must be an integer from ${self._curr_bet + 1} (minimum bet) to ${p.stack + p.last_bet} (your maximum bet).\n")
                    # Update Caller Count
                    caller_count = 1
                    # Mark player as the last aggressor (for Showdown phase)
                    self._last_aggressor = p
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
                    print(f" raised the bet from ${old_bet} to ${self._curr_bet}.")   # the only usage of `old_bet` to print betting update
                    # Print Pot
                    print(f"Pot: ${self._pot} (Your stack: ${p.stack})\n")

                # FOLD:
                elif ans == 'FOLD':
                    players.pop(i)
                    i -= 1  # Offset to account for the increment at '# Close While-Loop'
                    # Annouce Player Action 
                    print("\n" + Fore.LIGHTMAGENTA_EX + f"{dealer}", end='')
                    print(": ", end='')
                    print(Fore.CYAN + f"{p.username}", end='')
                    print(" has ", end='')
                    print(Fore.RED + "folded" + Style.RESET_ALL + ". ")
                    print(f"{p.username}'s Stack: ${p.stack}\n")

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
            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
            # print("DEBUG", f"{p.username}'s stack: {p.stack}")
            # print("DEBUG", f"{p.username}'s last bet: {p.last_bet}")
            # print("DEBUG", f"Current Minimum Bet: {self._curr_bet}")
            # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG

        # Print Pot
        print(Fore.GREEN + f"\nPot ({round}): ${self._pot}\n")


def config_table_settings() -> tuple[str, int, int, int]:
    """
    Prompt user input for configuring game settings.
    """
    print("----------- TABLE SETUP -----------")
    username = input("   - Username: ")
    player_count = input("   - Number of seats: ")
    buyin_amt = input("   - Buy-in (min. $100): $")
    min_bet = input("   - Minimum bet: $")
    print("-----------------------------------")
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
        print(Style.BRIGHT + Fore.LIGHTRED_EX + "Invalid Input: To confirm your Hold'em table settings, input 'y' or 'n' and hit enter.\n")
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
        print(Style.BRIGHT + Fore.LIGHTRED_EX + "Invalid Input: To confirm your Hold'em table settings, input 'y' or 'n' and hit enter.\n")
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
        username,         # TODO: Implement a recursive input babysitter.
        player_count,     #       This code is faulty. Currently, there's no
        buyin_amt,        #       recursion happening here. It breaks after two
        min_bet,          #       complete init prompt cycles.
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

    # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
    # print(poker._players_queue)
    # print(poker._next_game_players_queue, end='\n\n\n')
    # DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG

    # Poker Events
    # ============
    while True:
        print("\n============== Proj_8: Texas Hold'em ==============\n")
        poker.e0_show_player_stats()
        print("\n============== Blind Bets ==============\n")
        poker.e1_blind_bet()
        print("\n============== Deal: POCKET CARDS ==============\n")
        poker.e2_deal_pocket()
        print("\n============== Bet (1/4): PRE-FLOP ==============\n")
        if poker.e3_preflop() == False:
            poker.e11_save_data()
            poker.e12_prep_next_game()
            continue
        print("\n============== Deal: FLOP ==============\n")
        poker.e4_deal_flop()
        print("\n============== Bet(2/4): FLOP ==============\n")
        if poker.e5_flop() == False:
            poker.e11_save_data()
            poker.e12_prep_next_game()
            continue
        print("\n============== Deal: TURN ==============\n")
        poker._handle_deals()
        print("\n============== Bet(3/4): TURN ==============\n")
        if poker.e7_turn() == False:
            poker.e11_save_data()
            poker.e12_prep_next_game()
            continue
        print("\n============== Deal: RIVER ==============\n")
        poker.e8_deal_river()
        print("\n============== Bet (4/4): RIVER ==============\n")
        if poker.e9_river() == False:
            poker.e11_save_data()
            poker.e12_prep_next_game()
            continue
        print("\n============== SHOWDOWN ==============\n")
        poker.e10_showdown()
        poker.e11_save_data()
        poker.e12_prep_next_game()
        sys.exit('bruh\n')
        # And... Repeat.


if __name__ == '__main__':
    DEV_MODE = False
    # DEV_MODE = True          # UNCOMMENT this line to debug and/or test code #
    if DEV_MODE is False:
        try:
            run()
        except:
            sys.exit('\n\n\n  [[ EXIT GAME ]]  \n  ---------------\n  keep ya head up\n')
    else:
        print()

        c1 = Card(1, 's')
        c2 = Card(8, 'h')
        c3 = Card(2, 'd')
        c4 = Card(1, 'c')
        c5 = Card(3, 's')
        c6 = Card(7, 'h')
        c7 = Card(6, 'd')
        c8 = Card(11, 'c')

        # lst1 = [c4, c7, c8, c1, c6, c5, c3, c2]
        # lst2 = Ann.bubble_sort(lst1)
        # print(lst1)
        # print(lst2, end='\n\n')
        comm_cards = [c1, c2, c3, c4, c5]
        hole_cards = [c8, c7]
        cards_pre = [c for c in comm_cards] + hole_cards
        cards: list[Card] = Ann.bubble_sort(cards_pre)
        suit_count: dict[str, int] = {suit: 0 for suit in Ann.SUITS_STR}
        rank_count: dict[int, int] = {rank: 0 for rank in range(2, 15)}

        print()
        pprint(cards_pre)
        print()
        pprint(cards)
        print()
        pprint(suit_count)
        print()
        pprint(rank_count)
        print()

        for c in cards:
            # Count collection of suits.
            suit_count[c.get_suit()] += 1
            # Count collection of ranks.
            if c.get_rank_int() == 1:
                rank_count[14] += 1
            else:
                rank_count[c.get_rank_int()] += 1

        print()
        pprint(suit_count)
        print()
        pprint(rank_count)
        print()
















































































































    def _get_best_hand_ARCHIVE_01(self, comm_cards: list[Card]) -> dict:
        """Designed to be called by `PokerGame.e10_showdown()`."""
        # ---------------------------------------------------------------------
        # TODO: Write an algorithm that takes a list of seven `Card` instances
        #       and determines the best possible 5-card hand that can be
        #       formed, plus an ordered list of high cards that can be used,
        #       optionally for tie-breakers.
        #
        # Implementation Remarks:
        # -----------------------
        # - Don't do completely separate individual checks for each hand type.
        #   Instead: 1. Count the suits first to see if flush occurs;
        #            2. Take it from there.
        # ---------------------------------------------------------------------
        #
        # EZ-Variables
        suit_count: dict[str, int] = {'Spades': 0,
                                      'Hearts': 0,
                                      'Diamonds': 0,
                                      'Clubs': 0}
        rank_count_int: dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
                                          6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                                          11: 0, 12: 0, 13: 0}
        rank_count_str: dict[int, int] = {'Ace': 0, '2': 0, '3': 0, '4': 0,
                                          '5': 0, '6': 0, '7': 0, '8': 0,
                                          '9': 0, '10': 0, 'Jack': 0,
                                          'Queen': 0, 'King': 0}
        cards = self.hole_cards + comm_cards
        sorted_cards: tuple[Card] = tuple(Ann.bubble_sort(cards))
        # Collect useful data
        # -------------------
        # (out of 7 cards):
        #   1. Count how many times each 'suit' appears
        #   2. Count how many times each 'rank' appears (int E [1, 13])
        #   3. Have a descending-order list of ranks handy
        for c in cards:
            suit_count[c.get_suit()] += 1
            rank_count_int[c.get_rank_int()] += 1
            rank_count_str[c.get_rank_str()] += 1   # just in case

        # Use collected data to determine if conditions are met for either...
        # -------------------------------------------------------------------
        #   10. Royal Flush
        #   9. Straight Flush
        #   8. Four of a Kind
        #   7. Full House
        #   6. Flush
        #   5. Straight
        #   4. Three of a Kind
        #   3. Two Pair
        #   2. Pair
        #   1. High Card
        # -------------------------------------------------------------------
        # ... Then, return the relevant data back to the caller.
        #
        # Condition Check: Flush Variants
        flush_suit: Optional[str] = None
        for suit in suit_count:
            if suit >= 5:
                flush_suit = suit

        # Condition Check: Four of a Kind (foak)
        foak_rank: Optional[int] = None
        for rank, count in rank_count_int.items():
            if count == 4:
                foak_rank = rank

        # Condition Check: Three of a Kind (toak)
        toak_rank: Optional[int] = None
        _toak_ranks = []
        for rank, count in rank_count_int.items():
            if count == 3:
                _toak_ranks.append(rank)
        _toak_ranks.sort(reverse=True)

        if _toak_ranks[-1] == 1:
            toak_rank = _toak_ranks[-1]
        else:
            toak_rank = _toak_ranks[0]

        # Condition Check: Pair Variants
        pair_ranks: Optional[list[int]] = None
        _pair_ranks = []
        for rank, count in rank_count_int.items():
            if count == 2:
                _pair_ranks.append(rank)
        _pair_ranks.sort(reverse=True)
        if _pair_ranks[-1] == 1:
            _pair_ranks.insert(0, _pair_ranks.pop())

        if toak_rank is not None:
            pair_ranks = _pair_ranks[:1]
        else:
            pair_ranks = _pair_ranks[:2]


        # Flush conditions have been met.
        if flush_suit is not None:
            """
            There are five or more cards w/ the same suit.
            Determine the hand from:
              10. Royal Flush
              9. Straight Flush
              6. Flush
            """
            # 10. Royal Flush
            # ---------------
            # EZ-Variables: Royal Flush
            royal_flush: list[Card] = []
            kickers: list[Card] = []
            # Assemble royal_flush hand & kickers.
            for c in sorted_cards:
                if c.get_suit() == flush_suit and len(royal_flush) <= 5:
                    royal_flush.append(c)
                else:
                    kickers.append(c)
            # Check if Royal Flush conditions have been met.
            if royal_flush[0].get_rank_str() == 'Ace' and len(royal_flush) == 5 \
              and royal_flush[1].get_rank_int() == 13 \
              and royal_flush[2].get_rank_int() == 12 \
              and royal_flush[3].get_rank_int() == 11 \
              and royal_flush[4].get_rank_int() == 10:
                return 10, royal_flush, kickers, self.username

            # 9. Straight Flush
            # -----------------
            # EZ-Variables: Straight Flush
            str8_flush: list[Card] = []
            kickers: list[Card] = []
            same_suits: list[Card] = []   # NEVER contains duplicate ranks.
            for c in sorted_cards:
                if c.get_suit() == flush_suit:
                    same_suits.append(c)
                else:
                    kickers.append(c)
            len(same_suits) == 5 | 6 | 7

            # Edge Case: Low Straight Flush, where 'Ace' is the LOWEST ranking.
            if same_suits[0].get_rank_str() == 'Ace':
                for i in range(1, len(same_suits)-3):
                    if same_suits[i].get_rank_int() == 5:
                        # Assemble low-straight flush hand.
                        str8_flush += [same_suits[i] + same_suits[i+1] +
                                       same_suits[i+2] + same_suits[i+3] +
                                       same_suits[0]]
                        # Assemble kickers.
                        if len(same_suits) == 7:
                            if i == 1:
                                kickers += [same_suits[5], same_suits[6]]
                            elif i == 2:
                                kickers += [same_suits[1], same_suits[6]]
                            elif i == 3:
                                kickers += [same_suits[1], same_suits[2]]
                        elif len(same_suits) == 6:
                            if i == 1:
                                kickers.append(same_suits[5])
                            elif i == 2:
                                kickers.append(same_suits[1])
                        # Return Low-Straight Flush
                        return 9, str8_flush, Ann.bubble_sort(kickers), self.username
            # Regular Cases
            for i in range(len(same_suits)-4):
                # Check if the next five cards are straight (descending order).
                # Remember: Cases where 'Ace' is the highest card are handled
                #           already.
                if same_suits[i].get_rank_int()-1 == same_suits[i+1].get_rank_int() \
                  and same_suits[i].get_rank_int()-2 == same_suits[i+2].get_rank_int() \
                  and same_suits[i].get_rank_int()-3 == same_suits[i+3].get_rank_int() \
                  and same_suits[i].get_rank_int()-4 == same_suits[i+4].get_rank_int():
                    # Assemble flush hand.
                    str8_flush += [same_suits[i] + same_suits[i+1] +
                                   same_suits[i+2] + same_suits[i+3] +
                                   same_suits[i+4]]
                    # Assemble kickers.
                    if len(same_suits) == 7:
                        if i == 0:
                            kickers = [same_suits[5], same_suits[6]]
                        elif i == 1:
                            kickers = [same_suits[0], same_suits[6]]
                        elif i == 2:
                            kickers = [same_suits[0], same_suits[1]]
                    elif len(same_suits) == 6:
                        if i == 0:
                            kickers.append(same_suits[5])
                        elif i == 1:
                            kickers.append(same_suits[0])
                    # Return Straight Flush
                    return 9, str8_flush, Ann.bubble_sort(kickers), self.username

            # 6. Flush
            # --------
            # EZ-Variables: Flush
            flush: list[Card] = []
            kickers: list[Card] = []
            for c in sorted_cards:
                if c.get_suit() == flush_suit and len(flush) <= 5:
                    flush.append(c)
                else:
                    kickers.append(c)
            return 6, flush, kickers, self.username

        # 8. Four of a Kind
        # -----------------
        elif foak_rank is not None:
            # EZ-Variables: Four of a Kind
            foak: list[Card] = []
            kickers: list[Card] = []
            for c in sorted_cards:
                if c.get_rank_int() == foak_rank:
                    foak.append(c)
                else:
                    kickers.append(c)
            return 8, foak, kickers, self.username

        # 7. Full House
        # -------------
        elif toak_rank is not None and pair_ranks is not None:
            # EZ-Variables: Full House
            full_house: list[Card] = []
            kickers: list[Card] = []
            # Assemble full house hand
            for c in sorted_cards:
                if c.get_rank_int() == toak_rank:
                    full_house.append(c)
            for c in sorted_cards:
                if c.get_rank_int() in pair_ranks:
                    full_house.append(c)
                # Assemble Kickers
                elif c.get_rank_int() != toak_rank:
                    kickers.append(c)
            return 7, full_house, kickers, self.username

        # if none of the above...
        else:
            """
            5. Straight
            4. Three of a Kind
            3. Two Pair
            2. Pair
            1. High Card
            """
            # 5. Straight
            # -----------
            # EZ-Variables: Straight
            str8: list[Card] = []
            kickers: list[Card] = []
            rank_seen_so_far: Optional[int] = None
            # Edge Case: Low Straight, where 'Ace' is the LOWEST rank.
            if sorted_cards[0].get_rank_str() == 'Ace':
                for i in range(1, 7):
                    if rank_seen_so_far is None:
                        if sorted_cards[i].get_rank_int() == 5:
                            rank_seen_so_far = 5
                            str8.append(sorted_cards[i])
                    elif rank_seen_so_far == 5:
                        if sorted_cards[i].get_rank_int() == 4:
                            rank_seen_so_far = 4
                            str8.append(sorted_cards[i])
                    elif rank_seen_so_far == 4:
                        if sorted_cards[i].get_rank_int() == 3:
                            rank_seen_so_far = 3
                            str8.append(sorted_cards[i])
                    elif rank_seen_so_far == 3:
                        if sorted_cards[i].get_rank_int() == 2:
                            rank_seen_so_far = 2
                            str8.append(sorted_cards[i])
                            str8.append(sorted_cards[0])
                if rank_seen_so_far == 2:
                    for c in sorted_cards:
                        if c not in str8:
                            kickers.append(c)
                    return 5, str8, kickers, self.username
            # Regular Cases
            else:
                pass
                



        # 4. Three of a Kind
        # ------------------
        # EZ-Variables: Three of a Kind
        pass

        # 3. Two Pair
        # -----------
        # EZ-Variables: Two Pair
        pass

        # 2. Pair
        # -------
        # EZ-Variables: Pair
        pass

        # 1. High Card
        # ------------
        # EZ-Variables: High Card
        pass
