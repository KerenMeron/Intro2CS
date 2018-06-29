#########################################################
# FILE: math_print.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex1 2015-2016
# DESCRIPTION: prints several requested math operations
#########################################################

import math

def task_1():
    '''
    prints the golden ratio constant
    '''
    print((1 +math.sqrt(5)) /2)


def task_2():
    '''
    prints 5 squared (25)
    '''
    print(5**2)


def task_3():
    '''
    prints the length of the hypotenuse of a triangle with sides of lengths 4 and 5
    '''
    print(math.sqrt(math.pow(4,2) + math.pow(5,2)))


def task_4():
    '''
    prints the value of pi
    '''
    print(math.pi)


def task_5():
    '''
    prints the value of e
    '''
    print(math.e)


def task_6():
    '''
    prints a string of the surface area of 10 squares, each with a different side length from 1-10.
    '''
    areas = ''
    for i in range(1,11):
        areas += str(i**2)
        areas += ' '
    areas = areas[0:len(areas)-1:]
    print (areas)

