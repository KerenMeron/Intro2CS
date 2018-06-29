############################################################################
# FILE: shapes.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex2 2015-2016
# DESCRIPTION: Calculates the area of a circle/rectangle/trapezoid.
############################################################################

import math
PI = math.pi
MESSAGE_INPUT_SHAPE = "Choose shape (1=circle, 2=rectangle, 3=trapezoid): "
CIRCLE = 1
RECTANGLE = 2
TRAPEZOID = 3

def calculate_circle_area(radius):
    '''Calculates and returns the area of a circle with a given radius.'''

    area = PI * (float(radius) ** 2)
    return area

def calculate_rectangle_area(side1, side2):
    '''Calculates and returns the area of a rectangle with given sides.'''

    area = float(side1) * float(side2)
    return area

def calculate_trapezoid_area(base1, base2, height):
    '''Calculates and returns the area of a trapezoid with a given sides.'''

    area = ( (float(base1) + float(base2)) / 2) * float(height)
    return area

def shape_area():
    '''Asks the user to choose a circle/rectangle/trapezoid, and
    calculates the shape's area using the area calculation functions above.
    Returns the shape area.'''

    shape = input(MESSAGE_INPUT_SHAPE)
    if int(shape) == CIRCLE:
        radius = input()
        return calculate_circle_area(radius)
    elif int(shape) == RECTANGLE:
        side1 = input()
        side2 = input()
        return calculate_rectangle_area(side1, side2)
    elif int(shape) == TRAPEZOID:
        base1 = input()
        base2 = input()
        height = input()
        return calculate_trapezoid_area(base1, base2, height)
    else: #number inputed different from 1/2/3
        return None

