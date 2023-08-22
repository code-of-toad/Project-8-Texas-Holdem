"""
Project_8: Texas Hold'em
========================
Keep it simple, stupid.
"""
from __future__ import annotations
from typing import Optional, Any, Union
from pprint import pprint
import random as rand


RANK_MAP: dict[int, str] = {1: 'Ace', 2: '2', 3: '3', 4: '4', 5: '5',
                            6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
                            11: 'Jack', 12: 'Queen', 13: 'King'}

SUIT_MAP: dict[str, str] = {'s': 'Spades',
                            'h': 'Hearts',
                            'd': 'Diamonds',
                            'c': 'Clubs'}

CARD_INVENTORY: dict[str, bool] = {}
for s in ['s', 'h', 'd', 'c']:
    for r in range(1, 14):
        init_str = f'{RANK_MAP[r]} of {SUIT_MAP[s]}'
        CARD_INVENTORY.setdefault(init_str, 0)
# pprint(CARD_INVENTORY)


class Card:
    """
    Card
    ----
    A minimalistic representation of a single playing card. Instantiation takes
    two parameters: rank & suit of the Card object.

    Symbolic Representation Map:
        - ranks: `1` --> Ace, `11` --> Jack, `12` --> Queen, `13` --> King
        - suits: `'s'` --> Spades, `'h'` --> Hearts; `'d'` --> "Diamonds", `'c'` --> "Clubs"

    Instance Attributes:
    --------------------
        - `_rank`: `str`
        - `_suit`: `str`
    
    Notice that these are private attributes. Please do NOT access them
    directly, but only through method calls.

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
    - After `self.__init__()`, a Card instance cannot be altered, in the same
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
        self._rank = RANK_MAP[rank]
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


    def get_rank(self) -> str:
        """Return the str value of this card's rank."""
        return self._rank


    def get_suit(self) -> str:
        """Return the str value of this card's suit."""
        return self._suit


class InvalidArgException(Exception):
    def __init__(self) -> None:
        m = "Refer to the class docstring on How To Instantiate."
        super().__init__(m)


class CardDeck():
    """
    PokerDeck
    ---------
    A stack representation of the standard 52-card deck. No joker cards.
    Note that this representation of the standard deck of cards is always face-
    down.

    How To Instantiate:
    -------------------
    1. For a shuffled deck:
    >>> # CardDeck stacks are shuffled by default.
    >>> deck = CardDeck()

    2. For an ordered (i.e., unshuffled) deck, w/ the top of the face-down deck
    being the Card object that represents the King of Clubs, and w/ the bottom
    of the face-down deck being the 'Ace of Spades':
    >>> deck = CardDeck(shuffle=False)

    3. For an empty "deck" to insert custom cards into:
    >>> deck = CardDeck(empty=True)
    """
    # __Dev Representation Invariants:
    # --------------------------------
    # - The only method call capable of altering the attribute
    #   `num_cards_in_deck` is `draw_top()`.
    #
    _deck: list[Card]
    _card_dict: dict[str, int]
    _cards_remaining: int


    def __init__(self, shuffle=True, empty=False) -> None:
        """
        __Doctests:
        -----------
        >>> d1 = CardDeck(shuffle=False)
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
        >>> d2 = CardDeck()
        >>> # --- Insert tests involving a shuffled (default) deck.
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
        >>> deck = CardDeck(shuffle=False)
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
        >>> # You can keep drawing until you reach the bottom face-down card: Ace of Spades.

        Exceptions:
        -----------
        `draw()` raises an `EmptyDeckException` when called on an empty deck.
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


    def insert_mid(self, card: Card) -> None:
        """Insert `card` back into a random location in the deck."""
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


    def insert_top(self, card: Card) -> None:
        """Push `card` to the top of the deck."""
        # Error Check: Duplicate Cards
        if self._card_dict[str(card)] == 1:
            raise DuplicateCardException(card.get_rank(), card.get_suit())
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


    def shuffle(self) -> CardDeck:
        """
        Shuffle the deck in place, and return this newly-shuffled `CardDeck`
        object.

        Note that this method does NOT instantiate new CardDeck objects. The
        caller of this method will be the same object as the `CardDeck`
        instance that is returned.
        """
        rand.shuffle(self._deck)
        return self


class EmptyDeckException(Exception):
    def __init__(self):
        m = "You cannot draw from an empty deck."
        super().__init__(m)


class DuplicateCardException(Exception):
    def __init__(self, rank, suit):
        m = f"This deck already has the '{rank} of {suit}' card."
        super().__init__(m)


if __name__ == '__main__':
    print()
    import doctest
    doctest.testmod()
