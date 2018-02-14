#!/usr/bin/python3

"""
This test module contains tests on the helper functions
used in the __main__ function.
"""

import pytest
from poker import load_json_array, sorted_ranks_desc


# Valid JSON array tests
@pytest.mark.parametrize("valid_json_array, expected", [
    ('[]', []),
    ('["e"]', ['e']),
    ('["hi", "there", "3"]', ['hi', 'there', '3']),
    ('["10H", "JH", "QH", "KH", "AH"]', ['10H', 'JH', 'QH', 'KH', 'AH']),
    ('["2C", "JS", "2H", "5S", "10D"]', ['2C', 'JS', '2H', '5S', '10D']),
    ('["9S", "2H", "6D", "KH", "4C"]', ['9S', '2H', '6D', 'KH', '4C']),
    ('["3D", "6H", "9S", "JD", "8S"]', ['3D', '6H', '9S', 'JD', '8S'])
])
def test_load_valid_json_array(valid_json_array, expected):
    """ Test valid json array get imported successfully """
    card_list = load_json_array(valid_json_array)
    assert card_list == expected


# Invalid JSON array tests (valid JSON)
@pytest.mark.parametrize("invalid_json_array", [
    '{}',  # empty dict
    '"JH"',  # string
    '"aadlfjdlafkj"',  # string
    '{"key":["2C", "JS", "2H", "5S", "10D"]}',  # array in a dict
])
def test_load_valid_json_non_array(invalid_json_array):
    """ Test invalid json array raises system exit """
    with pytest.raises(SystemExit):
        load_json_array(invalid_json_array)


# Invalid JSON tests
@pytest.mark.parametrize("invalid_json_array", [
    "['3D', '6H', '9S', 'JD', '8S']",  # double and single quotes reversed
])
def test_load_invalid_json(invalid_json_array):
    """ Test invalid json array raises system exit """
    with pytest.raises(SystemExit):
        load_json_array(invalid_json_array)


# Rank sorting desc tests
@pytest.mark.parametrize("list_of_ranks, expected", [
    (['9', '10', 'J', 'Q', 'A'], ['A', 'Q', 'J', '10', '9']),
    (['3', '6', '4', 'Q', 'J'], ['Q', 'J', '6', '4', '3']),
    (['10', 'K', '2', '5'], ['K', '10', '5', '2']),
    (['2', '4', '6', '8'], ['8', '6', '4', '2']),
    (['A', '6', 'J'], ['A', 'J', '6']),
    (['3', 'K', '10'], ['K', '10', '3']),
    (['9', 'Q'], ['Q', '9']),
    (['8', '3'], ['8', '3'])
])
def test_sorted_ranks_desc(list_of_ranks, expected):
    """ Test sorted_ranks_desc helper function properly
    sorts ranks by rank descending """
    assert sorted_ranks_desc(list_of_ranks) == expected
