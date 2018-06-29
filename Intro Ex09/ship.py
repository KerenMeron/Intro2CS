#############################################################
# FILE: ex9.py
# WRITER: Keren Meron, keren.meron, 200039626
#         and  Eldan Chodorov , eldan , 201335965
# EXERCISE: intro2cs ex9 2015-2016
# DESCRIPTION: Contains Ship class for 'Asteroids' game.
#############################################################


from math import cos, sin, pi
from random import randrange
from screen import Screen as SC
from constants import *


class Ship:
    '''This class holds all information for the ship object.
    The class has attributes position, velocity, direction, life, etc.
    The class holds functions such as getters and setters for the attributes.
    '''

    def __init__(self):
        '''Initializes all of the containers needed for this class to work.
        Ship gets a random position at beginning of game.
        Direction is given in degrees.'''

        self.__pos_vel_x = (randrange(SC.SCREEN_MIN_X, SC.SCREEN_MAX_X),
                                                        MIN_VEL_SHIP)
        self.__pos_vel_y = (randrange(SC.SCREEN_MIN_Y, SC.SCREEN_MAX_Y),
                                                        MIN_VEL_SHIP)
        self.__direction = INIT_DIREC
        self.__life = INIT_SHIP_LIFE
        self.__points = INIT_SHIP_PTS
        self.__radius = SHIP_RADIUS

    def get_pos_vel(self, axis):
        '''
        Returns tuple of ship's position and velocity of requested axis.
        param axis(string): HORZ OR VERT.
        '''

        if axis == HORZ:
            return self.__pos_vel_x
        elif axis == VERT:
            return self.__pos_vel_y

    def get_direction(self):
        '''Returns ship's direction (in degrees).'''
        return self.__direction

    def get_radius(self):
        '''Returns ship's radius.'''
        return self.__radius

    def get_life(self):
        '''Return's ship's life.'''
        return self.__life

    def set_direction(self, input_direction):
        '''
        Sets a new direction to ship.
        param input_direction(int): degrees value.
        '''

        if input_direction:
            self.__direction = (self.__direction - DEGREES) % CYCLE
        else:
            self.__direction = (self.__direction + DEGREES) % CYCLE

    def set_life(self):
        '''Sets ship's life by reducing from it.'''
        self.__life -= REDUCE_LIFE

    def set_new_pos(self, new_pos_x, new_pos_y):
        '''
        Sets ship's new horizontal and vertical position.
        param new_pos_x(int): HORZ coordinate.
        param new_pos_y(int): VERT coordinate.
        '''

        self.__pos_vel_x = (new_pos_x, self.__pos_vel_x[1])
        self.__pos_vel_y = (new_pos_y, self.__pos_vel_y[1])

    def deg_to_rad(self):
        '''Return's ship's direction converted from degrees to radians.'''
        radian = self.__direction * (pi/HALF_CYCLE)
        return radian

    def acceleration(self):
        '''Sets ship's horizontal and vertical velocity according to an
        acceleration formula.'''

        radian = self.deg_to_rad()
        new_speed_x = self.__pos_vel_x[1] + cos(radian)
        new_speed_y = self.__pos_vel_y[1] + sin(radian)

        self.__pos_vel_x = (self.__pos_vel_x[0], new_speed_x)
        self.__pos_vel_y = (self.__pos_vel_y[0], new_speed_y)

    def get_points(self):
        '''Returns number points ship currently has.'''
        return self.__points

    def set_points(self, size):
        '''
        Adds points to ship, when torpedo hits asteroid. Allots points
        according to asteroid's size when hit.
        param size(int): size of asteroid.
        '''

        if size == AST_SIZE_3:
            self.__points += ADD_PTS_1
        elif size == AST_SIZE_2:
            self.__points += ADD_PTS_2
        else:
            self.__points += ADD_PTS_3
