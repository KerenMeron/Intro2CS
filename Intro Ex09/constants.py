#######################################################################
# FILE: ex9.py
# WRITER: Keren Meron, keren.meron, 200039626
#         and  Eldan Chodorov , eldan , 201335965
# EXERCISE: intro2cs ex9 2015-2016
# DESCRIPTION: Static file for defining constants 'Asteroids' game.
#######################################################################

#General:
HORZ = "x"
VERT = "y"
REDUCE_LIFE = 1
CYCLE = 360
HALF_CYCLE = 180
INIT_DIREC = 0

#torpedo:
ACCEL_FACT = 2
INIT_TORP_LIFE = 200
TORP_RADIUS = 4
MIN_TORP_LIFE = 0
MAX_TORPEDOS = 15

#ship:
INIT_SHIP_LIFE = 3
DEGREES = 7
INIT_SHIP_PTS = 0
SHIP_RADIUS = 1
MIN_VEL_SHIP = 0
AST_SIZE_3 = 3
AST_SIZE_2 = 2
ADD_PTS_1 = 20
ADD_PTS_2 = 50
ADD_PTS_3 = 100

#asteroid:
INITIAL_AST_SIZE = 3
MIN_AST_SIZE = 1
SIZE_CONST = 10
NORM_FACTOR = 5
RIGHT = True
LEFT = False
MAX_VEL = 4
MIN_VEL_AST = 1
ASTR2_FACTOR = -1

#asteroids_main:
DEFAULT_ASTEROIDS_NUM = 5
MIN_ASTS_IN_GAME = 1
MIN_SHIP_LIFE = 0
LIFE_REDUCTION_TITLE = 'SHIP HIT ALERT'
LIFE_REDUCTION_MSG = "You've been hit! Try again..."
GAME_END_MSG = "oh no...game over!"
GAME_OVER_TITLE = 'GAME OVER'
GAME_WIN_MSG = 'No more asteroids left in game:\n\tYOU WIN!'
GAME_LOSE_MSG = 'Ship has reached 0 life - YOU LOSE :('
GAME_EXIT_MSG = 'Exiting game...'
LIFE_CHECK = True
COLLISION = False