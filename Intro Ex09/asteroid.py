#############################################################
# FILE: ex9.py
# WRITER: Keren Meron, keren.meron, 200039626
#         and  Eldan Chodorov , eldan , 201335965
# EXERCISE: intro2cs ex9 2015-2016
# DESCRIPTION: Contains Asteroid class for 'Asteroids' game.
#############################################################

from random import randrange, choice
from screen import Screen as SC
from math import sqrt
from constants import *

class Asteroid:
    '''
    This class holds all information for the asteroid object.
    The asteroid as attributes of position, velocity, direction, etc.
    Contains several functions such as:
    - getters and setters for attributes
    - checking whether astroid has intersected with another object
    '''

    def __init__(self, pos_vel_x=0, pos_vel_y=0, direc=0,
                    size=INITIAL_AST_SIZE, first_move=False):
        '''
        Initializes all of the containers needed for this class to work.
        Initializes differently for asteroids randomly created at beginning
        of game, and for asteroids created from a torpedo hit.
        If created at game start: will randomly assign location and speed,
        as long as different from those of ship's.
        param pos_vel_x(int): HORZ coordinate.
                            If first move, is given ship's coordinate.
        param pos_vel_y(int): VERT coordinate.
                            If first move, is given ship's coordinate.
        param direc(int): direction in degrees.
        param size(int): size value for asteroid.
        param first_move(boolean): reports reason for asteroid creation.
        '''

        if first_move:
            random_range_horz = [i for i in range(SC.SCREEN_MIN_X,
                                        SC.SCREEN_MAX_X) if i != pos_vel_x]
            random_range_vert = [i for i in range(SC.SCREEN_MIN_Y,
                                        SC.SCREEN_MAX_Y) if i != pos_vel_y]
            self.__pos_vel_x = (choice(random_range_horz),
                                randrange(MIN_VEL_AST, MAX_VEL))
            self.__pos_vel_y = (choice(random_range_vert),
                                randrange(MIN_VEL_AST, MAX_VEL))
            self.__direction = randrange(INIT_DIREC, CYCLE)

        else:
            self.__pos_vel_x = pos_vel_x
            self.__pos_vel_y = pos_vel_y
            self.__direction = direc

        self.__size = size
        self.__radius = self.__size * SIZE_CONST - NORM_FACTOR


    def get_pos_vel(self, axis):
        '''
        Returns a tuple of the position and velocity for requested axis.
        param axis(string): HORZ or VERT.
        '''

        if axis == HORZ:
            return self.__pos_vel_x
        elif axis == VERT:
            return self.__pos_vel_y

    def set_new_pos(self, pos_x, pos_y):
        '''
        Updates the asteroid's position.
        param pos_x(int): HORZ coordinate.
        param pos_y(int): VERT coordinate.
        '''

        self.__pos_vel_x = (pos_x, self.__pos_vel_x[1])
        self.__pos_vel_y = (pos_y, self.__pos_vel_x[1])

    def get_size(self):
        '''Returns the size of the asteroid.'''
        return self.__size

    def get_direction(self):
        '''Returns the asteroid's direction.'''
        return self.__direction

    def has_intersection(self, obj):
        '''
        Checks if the asteroid has intersected with another object,
        Returns True or False accordingly.
        param obj(instance): an instance of either Ship, Asteroid or Torpedo.
        '''

        distance = sqrt((obj.get_pos_vel(HORZ)[0] - self.__pos_vel_x[0])**2
                    + (obj.get_pos_vel(VERT)[0] - self.__pos_vel_y[0])**2)

        if distance <= self.__radius + obj.get_radius():
            return True
        else:
            return False

    def new_pos_vel(self, axis, torpedo, duplicate=False):
        '''
        Calculates the new velocity of a new formed asteroid.
        Returns a tuple with old position and new velocity for requested axis.
        param axis(string): HORZ or VERT.
        param torpedo(Torpedo): an instance of Torpedo, which hit asteroid.
        param duplicate(boolean): If True, then calculates for the second
                asteroid being formed, and the direction and velocity will be
                opposite to those of the first asteroid.
        '''

        new_vel = (torpedo.get_pos_vel(axis)[1] + self.get_pos_vel(axis)[1]) \
                  / (sqrt((self.get_pos_vel(HORZ)[1])**2 +
                         (self.get_pos_vel(VERT)[1])**2))
        if duplicate:
            new_vel *= ASTR2_FACTOR

        return self.get_pos_vel(axis)[0], new_vel
