#################################################
# FILE: convert_spoon__to_cup.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex2 2015-2016
# DESCRIPTION: Converts units from spoon to cup
#################################################

CONVERSION_CONST = 3.5

def convert_spoon_to_cup(spoons):
    '''Converts from spoon value to cup value.
    Conversion: 1 cup = 3.5 spoons.
    Returns amount in spoons.'''

    cups = spoons / CONVERSION_CONST
    return cups



