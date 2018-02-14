#!/usr/bin/python3

import pytest
from poker import *

"""
This test module contains tests on the PokerHand class
and its associated methods.
"""


@pytest.fixture
def hand():
    """ Returns an empty PokerHand instance """
    return PokerHand()


# Invalid hand length tests
@pytest.mark.parametrize("card_list", [
    # length too short
    [],  # 0
    ['JC'],  # 1
    ['4H', '4S'],  # 2
    ['6S', 'KS', 'KH'],  # 3
    ['AS', '2C', 'AD', '6S'],  # 4
    # length too long
    ['3C', 'AH', 'KH', '9H', '8C', '9C'],  # 6
    ['5H', '2D', '4C', 'QC', 'AC', 'AS', '2C'],  # 7
    ['AS', '3C', '4S', '8D', 'QD', 'AD', '5C', '6S']  # 8
])
def test_invalid_hand_length(hand, card_list):
    """ Test hand raises assertion error due to invalid length """
    with pytest.raises(AssertionError):
        hand.add_cards(card_list)


# Invalid hand dupiclate cards tests
@pytest.mark.parametrize("card_list", [
    ['AS', '2C', 'AD', '6S', '6S'],
    ['3C', '3C', 'KH', '9H', '8C'],
    ['2D', '2D', '4C', 'QC', 'AC'],
    ['AH', 'AH', '4S', '8D', 'QD']
])
def test_duplicate_cards(hand, card_list):
    """ Test hand duplicate cards raises error """
    with pytest.raises(AssertionError):
        hand.add_cards(card_list)


# One-pair tests
@pytest.mark.parametrize("card_list, expected", [
    (['JC', 'JH', 'KC', 'QH', 'AH'], True),
    (['4H', '4S', '6C', '7H', 'AS'], True),
    (['6S', 'KS', 'KH', '9D', '3S'], True),
    (['AS', '2C', 'AD', '6S', '8H'], True),
    (['3C', 'AH', 'KH', '9H', '8C'], False),
    (['5H', '2D', '4C', 'QC', 'AC'], False),
    (['AS', '3C', '4S', '8D', 'QD'], False),
    (['2H', '3C', '4D', '5S', '6H'], False)
])
def test_hand_has_one_pair(hand, card_list, expected):
    """ Test hand contains at least one pair """
    hand.add_cards(card_list)
    assert hand.has_one_pair() == expected


# Two-pair tests
@pytest.mark.parametrize("card_list, expected", [
    (['JC', 'JH', 'QC', 'QH', 'AH'], True),
    (['4H', '4S', '7C', '7H', 'AS'], True),
    (['6S', 'KS', '6H', '3D', '3S'], True),
    (['AS', '2C', 'AD', '2S', 'KH'], True),
    (['JC', 'JH', 'JS', '9H', '9C'], False),
    (['4H', '4D', '4C', 'QC', 'AC'], False),
    (['AS', 'AC', '4S', '3D', '6D'], False),
    (['JH', '2C', '4D', '9S', 'AH'], False)
])
def test_hand_has_two_pair(hand, card_list, expected):
    """ Test hand contains two pairs """
    hand.add_cards(card_list)
    assert hand.has_two_pair() == expected


# 3-of-a-kind tests
@pytest.mark.parametrize("card_list, expected", [
    (['JC', 'JH', 'JD', '9H', 'AH'], True),
    (['JH', '4S', '10C', '10H', '10S'], True),
    (['AS', '3S', '3H', '3D', '6D'], True),
    (['AS', '2C', 'AD', '9S', 'AH'], True),
    (['JC', 'JH', '4H', '9H', 'AH'], False),
    (['4H', '4S', '7C', 'QC', 'AC'], False),
    (['AS', '3S', '4S', '3D', '6D'], False),
    (['JH', '2C', '4D', '9S', 'AH'], False)
])
def test_hand_has_three_of_a_kind(hand, card_list, expected):
    """ Test hand contains 3-of-a-kind """
    hand.add_cards(card_list)
    assert hand.has_three_of_a_kind() == expected


# All unique ranks tests
@pytest.mark.parametrize("card_list, expected", [
    (['JC', '2H', '10C', '5S', 'AH'], True),
    (['2H', '3S', '4C', '5H', '6S'], True),
    (['AS', 'JS', '9H', '5D', '3S'], True),
    (['QS', 'KC', 'AD', '6S', '8H'], True),
    (['AC', 'AH', 'KH', '9H', '8C'], False),
    (['5H', '2D', '2C', 'QC', 'AC'], False),
    (['AS', 'AC', 'AH', 'AD', 'QD'], False),
    (['3H', '3C', '3D', '5S', '5H'], False)
])
def test_hand_has_all_unique_ranks(hand, card_list, expected):
    """ Test hand has all unique ranks """
    hand.add_cards(card_list)
    assert hand.has_all_unique_ranks() == expected


# Rank span less than 5 tests
@pytest.mark.parametrize("card_list, expected", [
    (['2C', '3H', '4C', '5S', '6H'], True),
    (['5H', '6S', '7C', '8H', '9S'], True),
    (['10S', 'JS', 'QH', 'KD', 'AS'], True),
    (['9S', '9C', 'JD', 'JS', 'JH'], True),
    (['2C', 'AH', 'KH', '9H', '8C'], False),
    (['2H', '3D', '4C', '5C', '7C'], False),
    (['8S', 'JC', 'QH', 'KD', 'AD'], False),
    (['6H', 'QC', '3D', '5S', '5H'], False)
])
def test_hand_rank_span_is_less_than_five(hand, card_list, expected):
    """ Test difference between the highest and lowest
    rank values in hand is less than 5 (possible straight) """
    hand.add_cards(card_list)
    assert hand.rank_span_is_less_than_five() == expected


# Straight tests
@pytest.mark.parametrize("card_list, expected", [
    (['10H', 'JH', 'QH', 'KH', 'AH'], True),
    (['2C', '3D', '4H', '5S', '6C'], True),
    (['7C', '8D', '9D', '10D', 'JD'], True),
    (['9S', '10C', 'JS', 'QH', 'KS'], True),
    (['7H', '9C', 'JS', 'QD', 'KH'], False),
    (['2C', '5C', '8C', 'JC', 'AC'], False),
    (['2S', '2D', '2H', '5S', '5D'], False),
    (['2H', '5C', '8D', '9S', 'AH'], False)
])
def test_hand_is_straight(hand, card_list, expected):
    """ Test hand is straight (all consecutive ranks) """
    hand.add_cards(card_list)
    assert hand.is_straight() == expected


# Flush tests
@pytest.mark.parametrize("card_list, expected", [
    (['JH', '2H', '4H', '9H', 'AH'], True),
    (['JC', '4C', '7C', 'QC', 'AC'], True),
    (['AD', '3D', '4D', '9D', '6D'], True),
    (['JS', '2S', '4S', '9S', 'AS'], True),
    (['JC', '2H', '4H', '9H', 'AH'], False),
    (['JH', '4S', '7C', 'QC', 'AC'], False),
    (['AS', '3S', '4S', '3D', '6D'], False),
    (['JH', '2C', '4D', '9S', 'AH'], False)
])
def test_hand_is_flush(hand, card_list, expected):
    """ Test hand is flush (all cards same suit) """
    hand.add_cards(card_list)
    assert hand.is_flush() == expected


# Full house tests
@pytest.mark.parametrize("card_list, expected", [
    (['JH', 'JC', 'JS', 'AC', 'AH'], True),
    (['2C', '2S', '4C', '4H', '4S'], True),
    (['6D', '6C', '8D', '8S', '8H'], True),
    (['9S', 'JH', 'JS', '9D', '9C'], True),
    (['8H', '8C', 'JS', 'JD', 'KH'], False),
    (['2C', '2S', '2H', 'JC', 'AC'], False),
    (['AS', 'AD', '3H', '5S', '9D'], False),
    (['2H', '5C', '8D', '9S', 'AH'], False)
])
def test_hand_is_full_house(hand, card_list, expected):
    """ Test hand is full house (has 3-of-a-kind and
    a pair) """
    hand.add_cards(card_list)
    assert hand.is_full_house() == expected


# 4-of-a-kind tests
@pytest.mark.parametrize("card_list, expected", [
    (['JH', 'JS', 'JC', 'JD', 'AH'], True),
    (['2C', '2D', '2H', '2S', 'AC'], True),
    (['AD', '3D', '3H', '3S', '3C'], True),
    (['JS', 'QS', 'QC', 'QD', 'QH'], True),
    (['JC', 'JH', 'JS', '9H', 'AH'], False),
    (['4H', '4S', '7C', 'QC', 'AC'], False),
    (['AS', '3S', '4S', '3D', '6D'], False),
    (['JH', '2C', '4D', '9S', 'AH'], False)
])
def test_hand_is_four_of_a_kind(hand, card_list, expected):
    """ Test hand has 4-of-a-kind """
    hand.add_cards(card_list)
    assert hand.is_four_of_a_kind() == expected


# Straight flush tests
@pytest.mark.parametrize("card_list, expected", [
    (['10H', 'JH', 'QH', 'KH', 'AH'], True),
    (['2C', '3C', '4C', '5C', '6C'], True),
    (['6D', '7D', '8D', '9D', '10D'], True),
    (['9S', '10S', 'JS', 'QS', 'KS'], True),
    (['9H', '10C', 'JS', 'QD', 'KH'], False),
    (['2C', '5C', '8C', 'JC', 'AC'], False),
    (['2S', '2D', '2H', '5S', '5D'], False),
    (['2H', '5C', '8D', '9S', 'AH'], False)
])
def test_hand_is_straight_flush(hand, card_list, expected):
    """ Test hand is straight flush (all consecutive ranks
    and same suit) """
    hand.add_cards(card_list)
    assert hand.is_straight_flush() == expected


# Royal flush tests
@pytest.mark.parametrize("card_list, expected", [
    (['10H', 'JH', 'QH', 'KH', 'AH'], True),
    (['10C', 'JC', 'QC', 'KC', 'AC'], True),
    (['10D', 'JD', 'QD', 'KD', 'AD'], True),
    (['10S', 'JS', 'QS', 'KS', 'AS'], True),
    (['9H', '10H', 'JH', 'QH', 'KH'], False),
    (['9C', 'JH', 'QD', 'KS', 'AD'], False),
    (['2S', '3S', '4S', '5S', '6S'], False),
    (['JH', '2C', '4D', '9S', 'AH'], False)
])
def test_hand_is_royal_flush(hand, card_list, expected):
    """ Test hand is royal flush (all consecutive ranks,
    same suit, ace high) """
    hand.add_cards(card_list)
    assert hand.is_royal_flush() == expected


# Category and tie breaking helpers tests
@pytest.mark.parametrize("card_list, expected", [
    (['10H', 'JH', 'QH', 'KH', 'AH'], 'royal flush'),
    (['10C', 'JC', 'QC', 'KC', 'AC'], 'royal flush'),
    (['10D', 'JD', 'QD', 'KD', 'AD'], 'royal flush'),
    (['10S', 'JS', 'QS', 'KS', 'AS'], 'royal flush'),

    (['2C', '3C', '4C', '5C', '6C'], 'straight flush: 6 high'),
    (['5H', '6H', '7H', '8H', '9H'], 'straight flush: 9 high'),
    (['8D', '9D', '10D', 'JD', 'QD'], 'straight flush: queen high'),
    (['7S', '8S', '9S', '10S', 'JS'], 'straight flush: jack high'),

    (['AD', 'AC', 'AS', 'AH', '6D'], 'four of a kind: aces with 6 kicker'),
    (['AD', 'JC', 'JS', 'JH', 'JD'], 'four of a kind: jacks with ace kicker'),
    (['2D', '2C', '2S', '2H', '4D'], 'four of a kind: 2s with 4 kicker'),
    (['KD', '6C', '6S', '6H', '6D'], 'four of a kind: 6s with king kicker'),

    (['QS', 'QC', 'QH', '9S', '9H'], 'full house: queens full of 9s'),
    (['JH', 'JS', 'JD', 'KS', 'KD'], 'full house: jacks full of kings'),
    (['2S', '2C', '10H', '10S', '10D'], 'full house: 10s full of 2s'),
    (['3S', 'QC', '3H', 'QS', '3C'], 'full house: 3s full of queens'),

    (['2H', '5H', 'AH', '9H', '7H'], 'flush: ace 9 7 5 2'),
    (['3C', '9C', 'JC', '4C', '8C'], 'flush: jack 9 8 4 3'),
    (['6D', '2D', '4D', '7D', '5D'], 'flush: 7 6 5 4 2'),
    (['QS', '3S', '7S', '2S', 'JS'], 'flush: queen jack 7 3 2'),

    (['6C', '7H', '8S', '9S', '10C'], 'straight: 10 high'),
    (['10C', 'JH', 'QD', 'KS', 'AC'], 'straight: ace high'),
    (['2S', '3H', '4S', '5S', '6S'], 'straight: 6 high'),
    (['7D', '8S', '9D', '10C', 'JS'], 'straight: jack high'),

    (['6H', '6S', '6C', 'QC', 'KH'], 'three of a kind: 6s with king queen kickers'),
    (['3H', 'AS', 'KC', 'KS', 'KH'], 'three of a kind: kings with ace 3 kickers'),
    (['9H', '9S', '6C', '9C', '5H'], 'three of a kind: 9s with 6 5 kickers'),
    (['JH', '8S', 'AS', 'AC', 'AH'], 'three of a kind: aces with jack 8 kickers'),

    (['AS', 'AC', '4S', '4D', '6D'], 'two pair: aces and 4s with 6 kicker'),
    (['3H', '3C', 'JS', 'JD', '2D'], 'two pair: jacks and 3s with 2 kicker'),
    (['QS', '5C', '3S', 'QD', '5D'], 'two pair: queens and 5s with 3 kicker'),
    (['9S', '9C', '2S', '2D', 'KD'], 'two pair: 9s and 2s with king kicker'),

    (['JH', 'JD', '4D', '9S', 'AH'], 'one pair: jacks with ace 9 4 kickers'),
    (['JH', 'QD', '4D', '4S', 'AH'], 'one pair: 4s with ace queen jack kickers'),
    (['10H', '10D', '3D', '9S', '6H'], 'one pair: 10s with 9 6 3 kickers'),
    (['2H', '2D', '3D', '4S', '5S'], 'one pair: 2s with 5 4 3 kickers'),

    (['2H', '5D', '8C', '9S', 'AH'], 'high card: ace 9 8 5 2'),
    (['2H', '3D', '4C', '5S', '7H'], 'high card: 7 5 4 3 2'),
    (['3H', '5D', '7C', '10S', 'JH'], 'high card: jack 10 7 5 3'),
    (['2H', '5D', 'JC', 'QS', 'KH'], 'high card: king queen jack 5 2'),

])
def test_hand_find_category(hand, card_list, expected):
    """ Test find_category method returns the expected
    category (best hand) with the correct tie breaking info """
    hand.add_cards(card_list)
    assert hand.find_category() == expected
