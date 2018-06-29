#############################################################
# FILE: ex9.py
# WRITER: Keren Meron, keren.meron, 200039626
#         and  Eldan Chodorov , eldan , 201335965
# EXERCISE: intro2cs ex9 2015-2016
# DESCRIPTION: Contains Torpedo class for 'Asteroids' game.
#############################################################

from math import cos, sin
from constants import *

class Torpedo:
    '''This class holds all information for the torpedo object.
    The torpedo has attributes of position, velocity, direction, etc.
    Contains several functions such as getters and setters for attributes
    and a checker whether the torpedo's life is over.
    '''

    def __init__(self, ship_pos_vel_x, ship_pos_vel_y, direction, radian):
        '''
        Initializes all of the containers needed for this class to work.
        Torpedo's position and direction are set same as the ship's.
        param ship_pos_vel_x(int): HORZ coordinate.
        param ship_pos_vel_y(int): VERT coordinate.
        param direction(int): direction in degrees.
        param radian(float): direction in radians.
        '''



        self.__pos_vel_x = (ship_pos_vel_x[0],
                            ship_pos_vel_x[1] + ACCEL_FACT * cos(radian))
        self.__pos_vel_y = (ship_pos_vel_y[0],
                            ship_pos_vel_y[1] + ACCEL_FACT * sin(radian))
        self.__direction = direction
        self.__life = INIT_TORP_LIFE
        self.__radius = TORP_RADIUS

    def get_direction(self):
        '''Returns torpedo's direction.'''
        return self.__direction

    def get_pos_vel(self, axis):
        '''
        Returns a tuple of torpedo's position and velocity for an axis.
        param axis (string): HORZ or VERT, axis for which to calculate.
        '''

        if axis == HORZ:
            return self.__pos_vel_x
        elif axis == VERT:
            return self.__pos_vel_y

    def set_new_pos(self, new_pos_x, new_pos_y):
        '''
        Sets new x and y position for torpedo.
        param new_pos_x(int): HORZ coordinate.
        param new_pos_y: VERT coordinate.
        '''

        self.__pos_vel_x = (new_pos_x, self.__pos_vel_x[1])
        self.__pos_vel_y = (new_pos_y, self.__pos_vel_y[1])
        self.__life -= REDUCE_LIFE

    def is_dead(self):
        '''Returns True if the torpedo's life is over, else returns None.'''
        if self.__life <= MIN_TORP_LIFE:
            return True

    def get_radius(self):
        '''Returns the torpedo's radius.'''
        return self.__radius
