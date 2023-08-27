"""
Project_8: Texas Hold'em
========================
Keep it simple, stupid.
"""
from __future__ import annotations
from typing import Optional, Any, Union
from pprint import pprint
from dataclasses import dataclass
import random as rand


RANK_MAP_STR: dict[int, str] = {1: 'Ace', 2: '2', 3: '3', 4: '4', 5: '5',
                                6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
                                11: 'Jack', 12: 'Queen', 13: 'King'}

RANK_MAP_INT: dict[int, str] = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                                '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                                'Jack': 11, 'Queen': 12, 'King': 13}

SUIT_MAP: dict[str, str] = {'s': 'Spades',
                            'h': 'Hearts',
                            'd': 'Diamonds',
                            'c': 'Clubs'}

CARD_INVENTORY: dict[str, bool] = {}
for s in ['s', 'h', 'd', 'c']:
    for r in range(1, 14):
        init_str = f'{RANK_MAP_STR[r]} of {SUIT_MAP[s]}'
        CARD_INVENTORY.setdefault(init_str, 0)
# pprint(CARD_INVENTORY)


class Card:
    """
    Card
    ----
    A minimalistic representation of a single playing card. Instantiation takes
    two parameters: rank & suit of the Card object.

    Symbolic Representation Guide:
        - ranks: `1` --> Ace, `11` --> Jack, `12` --> Queen, `13` --> King
        - suits: `'s'` --> Spades, `'h'` --> Hearts; `'d'` --> "Diamonds", `'c'` --> "Clubs"

    Instance Attributes:
    --------------------
        - `_rank`: `str`
        - `_suit`: `str`
    
    Use the getters and setters for both attributes. Do not access them
    directly, as doing so could break the clicent code.

    How To Instantiate:
    -------------------
        >>> ace_of_spades = Card(1, 's')
        >>> ten_of_hearts = Card(10, 'h')
        >>> jack_of_diamonds = Card(11, 'd')
        >>> queen_of_clubs = Card(12, 'c')
        >>> king_of_spades = Card(13, 's')
        >>> # str representation
        >>> str(ace_of_spades)
        'Ace of Spades'
        >>> str(ten_of_hearts)
        '10 of Hearts'
        >>> str(jack_of_diamonds)
        'Jack of Diamonds'
        >>> str(queen_of_clubs)
        'Queen of Clubs'
        >>> str(king_of_spades)
        'King of Spades'

    Representation Invariants:
    --------------------------
    - After `__init__()`, a Card instance cannot be altered, in the same
    way that an irl playing card cannot magically change its rank and suit.
    """
    # Instance Attributes:
    _rank: str
    _suit: str

    def __init__(self, rank: int, suit: str) -> None:
        """
        __Doctests:
        -----------
        >>> ace_of_spades = Card(1, 's')
        >>> ten_of_hearts = Card(10, 'h')
        >>> jack_of_diamonds = Card(11, 'd')
        >>> queen_of_clubs = Card(12, 'c')
        >>> king_of_spades = Card(13, 's')
        """
        # Error Check: Invalid Args
        if rank<=0 or rank>=14 or suit not in SUIT_MAP:
            raise InvalidArgException
        # Initialize Card
        self._rank = RANK_MAP_STR[rank]
        self._suit = SUIT_MAP[suit]


    def __str__(self) -> str:
        """
        __Doctests:
        -----------
        >>> str(Card(1, 's'))
        'Ace of Spades'
        >>> str(Card(10, 'h'))
        '10 of Hearts'
        >>> str(Card(11, 'd'))
        'Jack of Diamonds'
        >>> str(Card(12, 'c'))
        'Queen of Clubs'
        >>> str(Card(13, 's'))
        'King of Spades'
        """
        return f'{self._rank} of {self._suit}'


    def __repr__(self) -> str:
        """
        __Doctests:
        -----------
        >>> Card(1, 's')
        Ace of Spades
        >>> Card(10, 'h')
        10 of Hearts
        >>> Card(11, 'd')
        Jack of Diamonds
        >>> Card(12, 'c')
        Queen of Clubs
        >>> Card(13, 's')
        King of Spades
        """
        return self.__str__()
    

    def __eq__(self, other: Card) -> bool:
        """
        __Doctests:
        -----------
        >>> c1 = Card(1, 's')
        >>> c2 = Card(1, 's')
        >>> c1 == c2
        True
        >>> c1 = Card(1, 's')
        >>> c2 = Card(1, 'h')
        >>> c1 == c2
        True
        >>> c1 = Card(1, 's')
        >>> c2 = Card(2, 'h')
        >>> c1 == c2
        False
        """
        if isinstance(other, Card):
            return self._rank == other._rank
        return False


    def __lt__(self, other: Card) -> bool:
        """
        __Doctests:
        -----------
        >>> c1 = Card(1, 's')
        >>> c2 = Card(7, 's')
        >>> c3 = Card(7, 'h')
        >>> c1 < c2
        True
        >>> c1 < c3
        True
        >>> c2 < c1
        False
        >>> c2 < c3
        False
        >>> c3 < c1
        False
        >>> c3 < c2
        False
        """
        return self.get_rank_int() < other.get_rank_int()


    def __gt__(self, other: Card) -> bool:
        """
        __Doctests:
        -----------
        >>> c1 = Card(1, 's')
        >>> c2 = Card(7, 's')
        >>> c3 = Card(7, 'h')
        >>> c1 > c2
        False
        >>> c1 > c3
        False
        >>> c2 > c1
        True
        >>> c2 > c3
        False
        >>> c3 > c1
        True
        >>> c3 > c2
        False
        """
        return self.get_rank_int() > other.get_rank_int()


    def __le__(self, other: Card) -> bool:
        """
        __Doctests:
        -----------
        >>> c1 = Card(1, 's')
        >>> c2 = Card(7, 's')
        >>> c3 = Card(7, 'h')
        >>> c1 <= c2
        True
        >>> c1 <= c3
        True
        >>> c2 <= c1
        False
        >>> c2 <= c3
        True
        >>> c3 <= c1
        False
        >>> c3 <= c2
        True
        """
        return self.get_rank_int() <= other.get_rank_int()


    def __ge__(self, other: Card) -> bool:
        """
        __Doctests:
        -----------
        >>> c1 = Card(1, 's')
        >>> c2 = Card(7, 's')
        >>> c3 = Card(7, 'h')
        >>> c1 >= c2
        False
        >>> c1 >= c3
        False
        >>> c2 >= c1
        True
        >>> c2 >= c3
        True
        >>> c3 >= c1
        True
        >>> c3 >= c2
        True
        """
        return self.get_rank_int() >= other.get_rank_int()


    def get_rank_str(self) -> str:
        """
        Return the `str` value of this card's rank.
        
        __Doctests:
        -----------
        >>> c = Card(1, 's')
        >>> c.get_rank_str()
        'Ace'
        >>> c = Card(13, 's')
        >>> c.get_rank_str()
        'King'
        """
        return self._rank


    def get_rank_int(self) -> int:
        """
        Return the `int` value of this card's rank.
        
        __Doctests:
        -----------
        >>> c = Card(1, 's')
        >>> c.get_rank_int()
        1
        >>> c = Card(13, 's')
        >>> c.get_rank_int()
        13
        """
        return RANK_MAP_INT[self._rank]


    def get_suit(self) -> str:
        """
        Return the str value of this card's suit.
        
        __Doctests:
        -----------
        >>> c = Card(1, 's')
        >>> c.get_suit()
        'Spades'
        """
        return self._suit


class InvalidArgException(Exception):
    def __init__(self) -> None:
        msg = "\n :\n +--> \
Refer to the class docstring on How To Instantiate.\n"
        super().__init__(msg)


class Deck():
    """
    Deck
    ----
    A stack representation of the standard 52-card deck. No joker cards.
        Note: This representation of the standard deck of cards is always \
              faced down.

    Three Ways To Instantiate:
    --------------------------
    1. Shuffled deck:
    >>> # Shuffled by default.
    >>> deck = Deck()

    2. Ordered (i.e., unshuffled) deck, w/ the top of the deck being the Card
    object that represents the 'King of Clubs', and w/ the bottom of the deck
    being the 'Ace of Spades':
    >>> deck = Deck(shuffle=False)

    3. Empty "deck" to manually insert custom cards into later:
    >>> deck = Deck(empty=True)
    >>> deck.size()
    0
    >>> deck.insert(Card(1, 's'))
    >>> deck.size()
    1
    >>> deck.draw()
    Ace of Spades
    >>> deck.size()
    0
    """
    # __Dev Representation Invariants:     
    # --------------------------------
    # - When called, `size()` must strictly return an `int` member of the
    #   inclusive set [0, 52].
    #
    _deck: list[Card]
    _card_dict: dict[str, int]


    def __init__(self, shuffle=True, empty=False) -> None:
        """
        __Doctests:
        -----------
        >>> d1 = Deck(shuffle=False)
        >>> d1.size()
        52
        >>> d1.draw()
        King of Clubs
        >>> d1.size()
        51
        >>> d1.draw()
        Queen of Clubs
        >>> for _ in range(49):
        ...     _ = d1.draw()
        ...
        >>> d1.size()
        1
        >>> d1.draw()
        Ace of Spades
        >>> d1.size()
        0
        >>> d2 = Deck()
        >>> # --- Insert tests involving a shuffled (default) deck.
        >>> d3 = Deck(empty=True)
        >>> d3.size()
        0
        >>> d3.insert(Card(1, 's'))
        >>> d3.size()
        1
        >>> d3.draw()
        Ace of Spades
        """
        self._deck = []
        self._card_dict = CARD_INVENTORY.copy()
        if not empty:
            for suit in ['s', 'h', 'd', 'c']:
                for rank in range(1, 14):
                    card = Card(rank, suit)
                    self._deck.append(card)
                    self._card_dict[str(card)] = 1
            if shuffle:
                rand.shuffle(self._deck)


    def draw(self) -> Card:
        """
        Remove & return the top card in the deck.

        How To Use:
        -----------
        >>> deck = Deck(shuffle=False)
        >>> deck.size()
        52
        >>> deck.draw()
        King of Clubs
        >>> deck.draw()
        Queen of Clubs
        >>> deck.draw()
        Jack of Clubs
        >>> deck.draw()
        10 of Clubs
        >>> deck.draw()
        9 of Clubs
        >>> deck.size()
        47
        >>> # You can keep drawing until the last card, Ace of Spades, is drawn.

        Exceptions:
        -----------
        Raises `EmptyDeckException` when called on an empty deck.
        """
        # __Dependencies:
        # ---------------
        # - self.size()
        #
        if self.size() == 0:
            raise EmptyDeckException
        pop_card = self._deck.pop()
        self._card_dict[str(pop_card)] = 0
        return pop_card


    def insert(self, card: Card) -> None:
        """Insert `<card>` back into a random location in the deck."""
        # __Dependencies:
        # ---------------
        # - self.size()
        #
        # Error Check: Duplicate Cards
        if self._card_dict[str(card)] == 1:
            raise DuplicateCardException
        # if self.size() >= 1:
        #     index = randint(0, self.size())
        #     self._deck.insert(index, card)
        # else:
        #     self.insert_top(card)
        if self.size() == 0:
            self._deck.append(card)
        elif self.size() == 1:
            self._deck.insert(0, card)
        else:
            i = rand.randint(0, self.size() - 1)
            self._deck.insert(i, card)

        self._card_dict[str(card)] = 1


    def place_top(self, card: Card) -> None:
        """Push `<card>` to the top of the deck."""
        # Error Check: Duplicate Cards
        if self._card_dict[str(card)] == 1:
            raise DuplicateCardException(card.get_rank_str(), card.get_suit())
        # Put `card` at the top of the deck
        self._deck.append(card)
        self._card_dict[str(card)] = 1


    def size(self) -> int:
        """
        Return the number of cards remaining in the deck.

        Representation Invariants:
        --------------------------
        - `size()` can only return `int` members of the set [0, 52].
        """
        return len(self._deck)


    def shuffle(self) -> Deck:
        """
        Shuffle the deck in place, and return this newly-shuffled `Deck`
        object.

        Note that this method does NOT instantiate new `Deck` objects. The
        caller of this method will be the same object as the `Deck` instance
        that is returned.
        """
        rand.shuffle(self._deck)
        return self

    def is_empty(self) -> bool:
        """
        Return `True` if the deck is empty. Otherwise, return `False`.

        Examples:
        ---------
        >>> d1 = Deck()
        >>> d2 = Deck(empty=True)
        >>> d1.is_empty()
        False
        >>> d2.is_empty()
        True
        """
        # __Dependencies:
        # ---------------
        # - `size()`
        #
        return self.size() == 0



class EmptyDeckException(Exception):
    def __init__(self):
        msg = "\n :\n +--> \
You cannot draw from an empty deck.\n"
        super().__init__(msg)


class DuplicateCardException(Exception):
    def __init__(self, rank, suit):
        msg = f"\n :\n +--> \
This deck already contains the '{rank} of {suit}' card.\n"
        super().__init__(msg)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
