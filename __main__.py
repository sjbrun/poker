#!/usr/bin/python3

from poker import *

"""
This program takes a 5-card hand as a JSON array and outputs the best category
along with any tie breaking information that is necessary.  For example: 

    Input:  ["JH", "4C", "4S", "JC", "9H"]
    Output: "two pair: jacks and 4s with a 9 kicker"

If input is invalid, appropriate error messages will be displayed regarding:
    - invalid JSON input
    - incorrect input type (non-array)
    - length of hand is not equal to 5 cards
    - duplicate cards in hand
    - invalid cards
"""

def main():
    user_input = get_user_input()
    card_list = load_json_array(user_input)
    build_hand_and_analyze(card_list)

if __name__ == '__main__':
    main()