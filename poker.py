#!/usr/bin/python3

"""
This module can model a poker hand and analyze it to determine
the best possible category.
"""

import json
import sys

# Valid suits
SUITS = ('H', 'C', 'D', 'S')

# Card ranks in ascending order
RANK_ORDER_ASC = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

# Card ranks in descending order
RANK_ORDER_DESC = ('A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2')

# Card rank names
RANK_NAMES = {'2': '2', '3': '3', '4': '4', '5': '5',
              '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
              'J': 'jack', 'Q': 'queen', 'K': 'king', 'A': 'ace'}


class Card(object):
    """ Models a poker card. Stores card rank and suit.

    Args:
        string (str): Name string representing card

    Attributes:
        rank (str): Card rank (e.g. - 'J')
        suit (str): Card suit (e.g. - 'H')
    """

    def __init__(self, string):
        """ Accepts a string input to create card """
        self.rank = ''
        self.suit = ''
        assert isinstance(string, str), 'Card object input must be type string'
        assert string[-1] in SUITS, string + ' is not a valid card'
        self.suit = string[-1]
        if '10' in string:  # special handling for ten card due to string length
            assert len(string) == 3, string + ' is not a valid card'
            assert string[0:-1] in RANK_ORDER_ASC, string + ' is not a valid card'
            self.rank = string[0:-1]
        else:  # all non-ten value cards
            assert len(string) == 2, string + ' is not a valid card'
            assert string[0] in RANK_ORDER_ASC, string + ' is not a valid card'
            self.rank = string[0]

    def __repr__(self):
        return '{}'.format(self.rank + self.suit)


class PokerHand(object):
    """ Models a poker hand. Stores list of Card instances, the count of each
        rank, and the count of each suit.

    Essential methods:
        add_cards: Loads poker hand with cards
        find_category: Analyzes hand and returns category with tie breaking
                       details

    Args:
        none (method "add_cards" loads hand with cards)

    Attributes:
        rank_counts (dict): Stores the count of each card rank present in hand
        suit_counts (dict): Stores the count of each card suit present in hand
        cards (list): List of Card objects that are contained in hand
    """

    def __init__(self):
        """ Initializes an empty poker hand. """
        self.rank_counts = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0,
                            '7': 0, '8': 0, '9': 0, '10': 0, 'J': 0,
                            'Q': 0, 'K': 0, 'A': 0}
        self.suit_counts = {'H': 0, 'C': 0, 'D': 0, 'S': 0}
        self.cards = []

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__,
                               self.cards)

    def add_cards(self, card_string_list):
        """ Creates Card instance for each card_string in input list. Adds
            card instances to model attribute "cards" and sorts by rank
            ascending.

        Args:
            card_string_list (list): list of strings representing poker cards
        """
        assert isinstance(card_string_list, list), 'Input type must be list/array'
        assert len(set(card_string_list)) == 5, 'Input array must contain 5 unique cards'
        for card_string in card_string_list:
            card = Card(card_string)
            self.cards.append(card)
            self.rank_counts[card.rank] += 1
            self.suit_counts[card.suit] += 1
        self.cards = sorted(self.cards,
                            key=lambda card: (RANK_ORDER_ASC.index(card.rank)))

    def find_category(self):
        """ Finds the best hand available, checking from highest to lowest ranked
            categories.
        Returns:
            The category and any tie breaking details.
            (e.g. - "two pair: jacks and 4s with a 9 kicker")
        """
        if self.is_royal_flush():
            category = 'royal flush'
        elif self.is_straight_flush():
            category = 'straight flush: ' + self.find_max_rank() + ' high'
        elif self.is_four_of_a_kind():
            category = 'four of a kind: ' + self.find_four_card_rank() + 's ' + \
                       'with ' + self.find_single_card_ranks() + ' kicker'
        elif self.is_full_house():
            category = 'full house: ' + self.find_three_card_rank() + 's ' + \
                       'full of ' + self.find_pair_ranks() + 's'
        elif self.is_flush():
            category = 'flush: ' + self.find_single_card_ranks()
        elif self.is_straight():
            category = 'straight: ' + self.find_max_rank() + ' high'
        elif self.has_three_of_a_kind():
            category = 'three of a kind: ' + self.find_three_card_rank() + 's ' + \
                       'with ' + self.find_single_card_ranks() + ' kickers'
        elif self.has_two_pair():
            pair_ranks = self.find_pair_ranks().split(' ')
            category = 'two pair: ' + pair_ranks[0] + 's and ' + pair_ranks[-1] + \
                       's ' + 'with ' + self.find_single_card_ranks() + ' kicker'
        elif self.has_one_pair():
            category = 'one pair: ' + self.find_pair_ranks() + 's with ' + \
                       self.find_single_card_ranks() + ' kickers'
        else:
            category = 'high card: ' + self.find_single_card_ranks()
        return category

    def has_one_pair(self):
        """ Returns: True if hand contains at least 1 pair """
        return 2 in self.rank_counts.values()

    def has_two_pair(self):
        """ Returns: True if hand contains 2 pairs """
        return list(self.rank_counts.values()).count(2) == 2

    def has_three_of_a_kind(self):
        """ Returns: True if hand contains a 3-of-a-kind """
        return 3 in self.rank_counts.values()

    def has_all_unique_ranks(self):
        """ Returns: True if hand has all unique ranks """
        return all(i < 2 for i in self.rank_counts.values())

    def rank_span_is_less_than_five(self):
        """ Returns: True if the difference between the highest and
            lowest rank values is less than 5 (possible straight) """
        present_ranks = [card.rank for card in self.cards]
        rank_values = []
        for rank in present_ranks:
            rank_values.append(RANK_ORDER_ASC.index(rank))
        rank_span = max(rank_values) - min(rank_values)
        return rank_span < 5

    def is_straight(self):
        """ Returns: True if hand is straight (all consecutive ranks) """
        return (self.has_all_unique_ranks()) and \
               (self.rank_span_is_less_than_five())

    def is_flush(self):
        """ Returns: True if hand is flush
            (all cards same suit) """
        return 5 in self.suit_counts.values()

    def is_full_house(self):
        """ Returns: True if hand is full house (has 3-of-a-kind and a pair) """
        return (self.has_three_of_a_kind()) and \
               (self.has_one_pair())

    def is_four_of_a_kind(self):
        """ Returns: True if hand has 4-of-a-kind """
        return 4 in self.rank_counts.values()

    def is_straight_flush(self):
        """ Returns: True if hand is a straight flush
            (all consecutive ranks and same suit) """
        return (self.is_flush()) and \
               (self.is_straight())

    def is_royal_flush(self):
        """ Returns: True if hand is a royal flush
            (all consecutive ranks, same suit, ace high) """
        return (self.is_flush()) and \
               (self.is_straight()) and \
               (self.rank_counts['A'] == 1)

    def find_max_rank(self):
        """ Returns: Maximum card rank present in hand (e.g. - 'A') """
        return RANK_NAMES[self.cards[-1].rank]  # assumes cards are sorted

    def find_four_card_rank(self):
        """ Returns: Card rank of 4-of-a-kind or None if not found. """
        for rank in self.rank_counts:
            if self.rank_counts[rank] == 4:
                card_rank = rank
                return RANK_NAMES[card_rank]
        return None

    def find_three_card_rank(self):
        """ Returns: Card rank of 3-of-a-kind or None if not found. """
        for rank in self.rank_counts:
            if self.rank_counts[rank] == 3:
                card_rank = rank
                return RANK_NAMES[card_rank]
        return None

    def find_pair_ranks(self):
        """ Returns: A string of the card rank(s) of the pair(s) in hand
            sorted by rank descending and separated by spaces
            or if not found returns None. """
        pair_ranks = []
        for rank in self.rank_counts:
            if self.rank_counts[rank] == 2:  # a pair for that rank exists
                pair_ranks.append(rank)
        if pair_ranks:  # list is not empty
            return ' '.join([RANK_NAMES[rank] for rank in sorted_ranks_desc(pair_ranks)])
        return None

    def find_single_card_ranks(self):
        """ Returns: A string of the card rank(s) of the solo cards in hand
            sorted by rank descending, separated by spaces """
        single_ranks = []
        for rank in self.rank_counts:
            if self.rank_counts[rank] == 1:
                single_ranks.append(rank)
        return ' '.join([RANK_NAMES[rank] for rank in sorted_ranks_desc(single_ranks)])


# Rank sorting helper function
def sorted_ranks_desc(list_of_ranks):
    """ Sorts input list of ranks by rank descending
        (helper for tie breaking kicker details)
    Args:
        list_of_ranks (list): List of card ranks (e.g. - ['K', '9' 'J'])
    Returns:
        A list of card ranks sorted by rank descending (e.g. - ['K', 'J', '9'] """
    return sorted(list_of_ranks, key=lambda rank: RANK_ORDER_DESC.index(rank))


# Functions for main()
def get_user_input():
    """ Prompts user for input, if blank --> system exit
    Returns: user_input (string): Raw user input string
    """
    user_input = input('\nEnter a JSON array of 5 cards ' +
                       '(e.g. - ["10S", "10H", "QH", "QS", "QD"]) ' +
                       'or press enter to quit: \n')
    if user_input == "":
        sys.exit()
    else:
        return user_input


def load_json_array(user_input):
    """ Attempts to read user input as a list of poker cards
    Args:
        user_input (JSON array): List of poker cards
    Returns:
        card_list (list): List of poker cards represented as strings
    Raises:
        ValueError: Could not decode JSON input
        AssertionError: Decoded JSON but it is not of type list
    """
    try:
        card_list = json.loads(user_input)
    except ValueError:  # includes json.decoder.JSONDecodeError
        print('\nDecoding JSON array failed. JSON array must be ' +
              'be bounded by brackets and include double quoted elements ' +
              '(e.g. - ["10H", "JH", "QH", "KH", "AH"]).\n\n')
        sys.exit()
    try:
        assert isinstance(card_list, list)
    except AssertionError:
        print('\nValid JSON, but not an array. JSON array must be ' +
              'be bounded by brackets and include double quoted elements ' +
              '(e.g. - ["10H", "JH", "QH", "KH", "AH"]).\n\n')
        sys.exit()
    return card_list


def build_hand_and_analyze(card_list):
    """ Attempts to build PokerHand from input list of cards and
        print the best category
    Args:
        card_list (list): List of poker cards represented as strings
    Raises:
        AssertionError: An error occurred in creating the PokerHand instance
    """
    try:
        hand = PokerHand()
        hand.add_cards(card_list)
        print(hand.find_category(), '\n')
    except AssertionError as error_msg:
        print(error_msg, '\n')
