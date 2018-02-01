#!/usr/bin/python3

import pytest
from poker import Card


"""
This test module contains tests on the Card class
and its associated methods. 
"""


## Valid card tests
@pytest.mark.parametrize("string, expected_rank, expected_suit", [
    # Hearts
    ('2H', '2', 'H'),
    ('3H', '3', 'H'),
    ('4H', '4', 'H'),
    ('5H', '5', 'H'),
    ('6H', '6', 'H'),
    ('7H', '7', 'H'),
    ('8H', '8', 'H'),
    ('9H', '9', 'H'),
    ('10H', '10', 'H'),
    ('JH', 'J', 'H'),
    ('QH', 'Q', 'H'),
    ('KH', 'K', 'H'),
    ('AH', 'A', 'H'),

    # Clubs
    ('2C', '2', 'C'),
    ('3C', '3', 'C'),
    ('4C', '4', 'C'),
    ('5C', '5', 'C'),
    ('6C', '6', 'C'),
    ('7C', '7', 'C'),
    ('8C', '8', 'C'),
    ('9C', '9', 'C'),
    ('10C', '10', 'C'),
    ('JC', 'J', 'C'),
    ('QC', 'Q', 'C'),
    ('KC', 'K', 'C'),
    ('AC', 'A', 'C'),

    # Diamonds
    ('2D', '2', 'D'),
    ('3D', '3', 'D'),
    ('4D', '4', 'D'),
    ('5D', '5', 'D'),
    ('6D', '6', 'D'),
    ('7D', '7', 'D'),
    ('8D', '8', 'D'),
    ('9D', '9', 'D'),
    ('10D', '10', 'D'),
    ('JD', 'J', 'D'),
    ('QD', 'Q', 'D'),
    ('KD', 'K', 'D'),
    ('AD', 'A', 'D'),

    # Spades
    ('2S', '2', 'S'),
    ('3S', '3', 'S'),
    ('4S', '4', 'S'),
    ('5S', '5', 'S'),
    ('6S', '6', 'S'),
    ('7S', '7', 'S'),
    ('8S', '8', 'S'),
    ('9S', '9', 'S'),
    ('10S', '10', 'S'),
    ('JS', 'J', 'S'),
    ('QS', 'Q', 'S'),
    ('KS', 'K', 'S'),
    ('AS', 'A', 'S')
])
def test_valid_cards(string, expected_rank, expected_suit):
    """ Test valid card string representation is created as 
    a Card instance with the correct rank and suit attributes """
    card = Card(string)
    assert card.rank == expected_rank
    assert card.suit == expected_suit


## Invalid card tests
@pytest.mark.parametrize("string", [
    66,     # type invalid
    3.1,    # type invalid
    [],     # type invalid
    {},     # type invalid
    'XX',   # rank and suit invalid
    'XXX',  # len, rank, and suit invalid 
    'ZZZZ', # len, rank, and suit invalid
    '1H',   # rank invalid
    '0S',   # rank invalid
    '11D',  # rank invalid
    '2Z',   # suit invalid
    'Q!',   # suit invalid
    'C3',   # rank and suit flipped
    '10Q',  # ten - rank valid, suit invalid
    'H10'   # ten - rank and suit flipped
])
def test_invalid_cards(string):
    """ Test assertion error raised for 
    invalid card string representation """
    with pytest.raises(AssertionError):
        card = Card(string)