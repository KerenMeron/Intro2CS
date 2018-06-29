#############################################################
# FILE: ship.py
# WRITER: Keren Meron, keren.meron, 200039626
# EXERCISE: intro2cs ex8 2015-2016
# DESCRIPTION: class of 'ship' as part of a battleship game
#############################################################

############################################################
# Imports
############################################################
from copy import deepcopy
from ship_helper import direction_repr_str

############################################################
# Class definition
############################################################
class Direction:
    """Class representing a direction in 2D world."""
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    NOT_MOVING = 0

    VERTICAL = (UP, DOWN)
    HORIZONTAL = (LEFT, RIGHT)

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

    MOVE = 1

############################################################
# Class definition
############################################################



class Ship:
    """
    A class representing a ship in Battleship game.
    A ship is 1-dimensional object that could be laid in either horizontal or
    vertical alignment. A ship sails on its vertical\horizontal axis back and
    forth until reaching the board's boarders and then changes its direction
    to the opposite (left <--> right, up <--> down).
    If a ship is hit in one of its coordinates, it ceases its movement in all
    future turns.
    A ship that had all her coordinates hit is considered terminated.
    """



    def __init__(self, pos, length, direction, board_size):
        """
        A constructor for a Ship object
        :param pos: A tuple representing The ship's head's (x, y) position
        :param length: Ship's length
        :param direction: Initial direction in which the ship is sailing
        :param board_size: Board size in which the ship is sailing
        """
        self.__pos = pos
        self.__length = length
        self.__direction = direction
        self.__board_size = board_size
        self.__hit_coords = set()  #ship's coordinates that have been hit
        self.__orientation = 5  #set to horizonta/vertical when game starts


    def set_orientation(self):
        '''Sets orientation to either vertical or horizontal, according
        to direction. Does this at beginning of game, in order to keep hit
        ship's orientation when not moving.'''

        if self.direction() in Direction.VERTICAL:
            self.__orientation = Direction.VERTICAL
        elif self.direction() in Direction.HORIZONTAL:
            self.__orientation = Direction.HORIZONTAL


    def __repr__(self):
        """
        Return a string representation of the ship.
        :return: A tuple converted to string. The tuple's content should be:
            1. A list of all the ship's coordinates.
            2. A list of all the ship's hit coordinates.
            3. Last sailing direction.
            4. The size of the board in which the ship is located.
        """

        coords = self.coordinates()
        hits = self.damaged_cells()
        dirc = direction_repr_str(Direction, self.__direction)
        size = self.__board_size
        return str((coords, hits, dirc, size))

    def move(self):
        """
        Make the ship move one board unit.
        Movement is in the current sailing direction, unless such movement
        would take it outside of the board in which case the shp switches
        direction and sails one board unit in the new direction.
        The ship will not move if one of its coordinates has been hit.
        :return: A direction object representing current movement direction.
        """

        ship_pos = self.__pos
        board = self.__board_size
        ship_len = self.__length
        ship_dir = self.__direction

        if ship_dir == Direction.UP:
            return self.move_up(ship_pos, ship_len, Direction.UP, board)
        elif ship_dir == Direction.DOWN:
            return self.move_down(ship_pos, ship_len, Direction.DOWN, board)
        elif ship_dir == Direction.RIGHT:
            return self.move_right(ship_pos, ship_len, Direction.RIGHT, board)
        elif ship_dir == Direction.LEFT:
            return self.move_left(ship_pos, ship_len, Direction.LEFT, board)
        else:
            return Direction.NOT_MOVING


    def move_right(self, ship_pos, ship_len, ship_dir, board_size):
        '''
        Makes the ship move one board unit to the right.
        If ship is at the edge of the board, the direction is turned 180 deg,
        and the ship is moved one board unit to the left.
        Returns the current direction.
        '''

        if self.check_bounds(ship_pos, ship_len, ship_dir, board_size):
            self.__pos = (ship_pos[0] + Direction.MOVE, ship_pos[1])
            return ship_dir
        else:
            self.__pos = (ship_pos[0] - Direction.MOVE, ship_pos[1])
            self.__direction = Direction.LEFT
            return Direction.LEFT

    def move_left(self, ship_pos, ship_len, ship_dir, board_size):
        '''
        Makes the ship move one board unit to the left.
        If ship is at the edge of the board, the direction is turned 180 deg,
        and the ship is moved one board unit to the right.
        Returns the current direction.
        '''

        if self.check_bounds(ship_pos, ship_len, ship_dir, board_size)== True:
            self.__pos = (ship_pos[0] - Direction.MOVE, ship_pos[1])
            return ship_dir
        else:
            self.__pos = ((ship_pos[0] + Direction.MOVE), ship_pos[1])
            self.__direction = Direction.RIGHT
            return Direction.RIGHT

    def move_up(self, ship_pos, ship_len, ship_dir, board_size):
        '''
        Makes the ship move one board unit upwards.
        If ship is at the edge of the board, the direction is turned 180 deg,
        and the ship is moved one board unit downwards.
        Returns the current direction.
        '''

        if self.check_bounds(ship_pos, ship_len, ship_dir, board_size):
            self.__pos = (ship_pos[0], ship_pos[1] - Direction.MOVE)
            return ship_dir
        else:
            self.__pos = (ship_pos[0], ship_pos[1] + Direction.MOVE)
            self.__direction = Direction.DOWN
            return Direction.DOWN

    def move_down(self, ship_pos, ship_len, ship_dir, board_size):
        '''
        Makes the ship move one board unit downwards.
        If ship is at the edge of the board, the direction is turned 180 deg,
        and the ship is moved one board unit upwards.
        Returns the current direction.
        '''

        if self.check_bounds(ship_pos, ship_len, ship_dir, board_size)== True:
            self.__pos = (ship_pos[0], ship_pos[1] + Direction.MOVE)
            return ship_dir
        else:
            self.__pos = (ship_pos[0], ship_pos[1] - Direction.MOVE)
            self.__direction = Direction.UP
            return Direction.UP

    def check_bounds(self, ship_pos, ship_len, ship_dir, board_size):
        '''Checks if ship is at edge of board in the direction it is moving,
        (if it needs to turn around). Returns False if out of bounds,
        otherwise return True.'''

        bound_check = True

        if ship_dir == Direction.RIGHT:
            if ship_pos[0] + ship_len == board_size:
                bound_check = False
        elif ship_dir == Direction.LEFT:
            if ship_pos[0] == 0:
                bound_check = False
        elif ship_dir == Direction.UP:
            if ship_pos[1] == 0:
                bound_check = False
        else:
            if ship_pos[1] + ship_len == board_size:
                bound_check = False

        return bound_check

    def add_hit(self, coord):
        '''Adds hit coord to ship's list of hit cells.'''
        self.__hit_coords.add(coord)

    def hit(self, coord):
        """
        Inform the ship that a bomb hit a specific coordinate.
        The ship updates its state accordingly.
        If one of the ship's body's coordinate is hit, the ship does not move
        in future turns. If all ship's body's coordinate are hit, the ship is
        terminated and removed from the board.
        :param pos: A tuple representing the (x, y) position of the hit.
        :return: True if the bomb generated a new hit in the ship, False
        otherwise.
        """

        ship_was_hit = False
        if self.__contains__(coord):  #ship was hit
            if coord not in self.__hit_coords:
                self.__hit_coords.add(coord)
                self.__direction = Direction.NOT_MOVING  #hit ship won't move
                ship_was_hit = True

        return ship_was_hit

    def terminated(self):
        '''
        Returns True if all ship's coordinates were hit in previous turns,
        False otherwise.
        '''

        ship_coords = self.coordinates()
        for coord in ship_coords:
            if coord not in self.__hit_coords:
                return False
        return True

    def __contains__(self, pos):
        """
        Check whether the ship is found in a specific coordinate.
        :param pos: A tuple representing the coordinate for check.
        :return: True if one of the ship's coordinates is found in the given
        (x, y) coordinates, False otherwise.
        """
        ship_coords = self.coordinates()
        if pos in ship_coords:
            return True
        else:
            return False

    def coordinates(self):
        """
        Return ship's current positions on board.
        :return: A list of (x, y) tuples representing the ship's current
        position.
        """

        ship_pos = self.__pos
        ship_len = self.__length
        ship_coords = list()
        self.set_orientation()

        if self.__orientation == Direction.HORIZONTAL:
            for x in range(ship_len):
                ship_coords.append((ship_pos[0] + x, ship_pos[1]))
        elif self.__orientation == Direction.VERTICAL:
            for y in range(ship_len):
                ship_coords.append((ship_pos[0], ship_pos[1] + y))

        return ship_coords

    def damaged_cells(self):
        """
        Returns the ship's hit positions.
        :return: A list of tuples representing the (x, y) coordinates of the
         ship which were hit in past turns (If there are no hit coordinates,
         return an empty list). There is no importance to the order of the
         values in the returned list.
        """

        hit_coords_copy = deepcopy(self.__hit_coords)
        hit_coords_copy = [i for i in hit_coords_copy]
        return hit_coords_copy

    def direction(self):
        """
        Return the ship's current sailing direction.
        :return: One of the constants of Direction class :
         [UP, DOWN, LEFT, RIGHT] according to current
         sailing direction or NOT_MOVING if the ship is hit and not moving.
        """
        return self.__direction

    def cell_status(self, pos):
        """
        Return the state of the given coordinate (hit\not hit)
        :param pos: A tuple representing the coordinate to query.
        :return:
            if the given coordinate is not hit : False
            if the given coordinate is hit : True
            if the coordinate is not part of the ship's body : None 
        """

        if self.__contains__(pos):
            if pos in self.damaged_cells():
                return True
            else:
                return False
        else:
            return None

