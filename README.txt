# Instructions
This program is written in Python 3 (tested with v3.5.1), which must be installed on computer to run it. To run the program, open the terminal in the project folder and type in "python __main__.py". 


# Testing
Testing is implemented with the pytest module, which can be installed with pip (package manager for Python). One way to install pip on OSX is to run "sudo easy_install pip". Once you have pip, pytest may be installed by running "pip install -U pytest" in the terminal. Read more about pytest here:  https://docs.pytest.org/en/latest/contents.html#

To run the tests simply open the terminal in the project folder and type in "pytest". This will run all files in the folder or subfolders of the form "*_test.py" or "test_*.py". Test files for this program include "test_card.py" and "test_poker_hand.py". 


## "test_card.py"
Tests pertaining to the modeling of a playing card.


## "test_poker_hand.py"
Tests pertaining to the modeling of a poker hand and the methods and functions associated to find the best category and tie breaking details. 