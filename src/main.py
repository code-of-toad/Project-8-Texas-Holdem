"""
Project_8: Texas Hold'em
========================
#TODO
"""
from __future__ import annotations
from typing import Optional, Any, Union


class Card:
    """
    Card
    ----
    A minimalistic representation of a playing card. Instantiation takes two
    arguments.

    Note:
        - ranks: `1` --> Ace, `11` --> Jack, `12` --> Queen, `13` --> King
        - suits: `'s'` --> Spades, `'h'` --> Hearts; `'d'` --> "Diamonds", `'c'` --> "Clubs"

    
    Instance Attributes:
    --------------------
        `_rank`: `str`
        `_suit`: `str`
    
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
    
    Representatino Invariants:
    --------------------------
    After `self.__init__()`, a Card instance cannot be altered, in the same way
    that an irl playing card cannot magically change its rank and suit.
    """
    # Useful Constants
    RANK_MAP: dict[int, str] = {1: 'Ace', 2: '2', 3: '3', 4: '4', 5: '5',
                                6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
                                11: 'Jack', 12: 'Queen', 13: 'King'}
    SUIT_MAP: dict[str, str] = {'s': 'Spades',
                                'h': 'Hearts',
                                'd': 'Diamonds',
                                'c': 'Clubs'}
    # Instance Attributes
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
        if rank<=0 or rank>=14 or suit not in self.SUIT_MAP:
            raise InvalidArgException
        self._rank = self.RANK_MAP[rank]
        self._suit = self.SUIT_MAP[suit]
    

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


class InvalidArgException(Exception):
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
