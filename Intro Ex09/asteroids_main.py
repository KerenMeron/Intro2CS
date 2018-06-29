##################################################################
# FILE: ex9.py
# WRITER: Keren Meron, keren.meron, 200039626
#         and  Eldan Chodorov , eldan , 201335965
# EXERCISE: intro2cs ex9 2015-2016
# DESCRIPTION: Contains 'main' function and GameRunner Class,
#               for execution of the 'Asteroids' game.
##################################################################

from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from constants import *

class GameRunner:
    '''
    This class holds all information for the game object.
    An object has attributes such as screen size, ship, list of asteroids
    and list of torpedos in the game. Includes a game round function
    which loops over and over until game is over.
    '''

    def __init__(self, asteroids_amnt):
        '''
        Initializes all of the containers needed for this class to work.
        Creates and registers and list of asteroids. Creates an instance of
        the Screen class, for the graphic interface, and a Ship instance.
        Initializes specific screen size properties.
        param asteroids_amnt(int): number of astroids to be created.
        '''

        self._screen = Screen()
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self.__asteroids_list = []
        self.__torpedo_list = []
        self.__ship = Ship()
        self.__width = Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X
        self.__height = Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y
        self.__asteroids_list = [Asteroid(self.__ship.get_pos_vel(HORZ)[0],
                        self.__ship.get_pos_vel(VERT)[0], first_move=True)
                                 for i in range(asteroids_amnt)]

        for asteroid in self.__asteroids_list:
            self._screen.register_asteroid(asteroid, asteroid.get_size())

    def run(self):
        '''Opens screen for user and calls to do loop in game.'''
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        '''Sets of timer for loop and calls game loop.'''
        self._game_loop()
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        '''
        Game run. Process as follows:
        1. Sets score on screen.
        2. Checks if user has pressed keys, and if so implements action.
        3. Moves all objects in game.
        4. Checks for collisions between asteroids and other object, and
            responds accordingly.
        5. Draws all objects on screen.
        6. Checks lives of torpedos and ship, and ends them if necessary.
        7. Checks for game over, and if so, exits.
        '''

        self._screen.set_score(self.__ship.get_points())
        self.input_checker()
        self.move()
        self.intersections()
        self.draw_objects()
        self.torpedo_update(LIFE_CHECK)
        self.game_end()

    def input_checker(self):
        '''
        Checks if user has pressed left, right, up (acceleration)
        or space (fire torpedos, if not passed max torpedos allowed in game).
        Implements action accordingly.
        '''

        if self._screen.is_left_pressed():
            self.__ship.set_direction(False)

        if self._screen.is_right_pressed():
            self.__ship.set_direction(True)

        if self._screen.is_up_pressed():
            self.__ship.acceleration()

        if self._screen.is_space_pressed():
            if len(self.__torpedo_list) < MAX_TORPEDOS:
                self.fire_torpedo()

    def fire_torpedo(self):
        '''
        Registers a new torpedo and adds to torpedo list of game.
        Torpedo created receives the position, velocity and direction of ship.
        '''


        pos_vel_x = self.__ship.get_pos_vel(HORZ)
        pos_vel_y = self.__ship.get_pos_vel(VERT)
        direc = self.__ship.get_direction()
        radian = self.__ship.deg_to_rad()

        new_torpedo = Torpedo(pos_vel_x, pos_vel_y, direc, radian)
        self.__torpedo_list.append(new_torpedo)
        self._screen.register_torpedo(new_torpedo)

    def torpedo_update(self, reason_for_check=COLLISION, dead_torpedos=None):
        '''
        Checks if torpedos life is over, and if so unregisters and
        removes torpedo. Life can be over from collision with asteroid,
        or if life expectancy is over.
        param reason_for_check(boolean): True(collision) or False(life check).
        param dead_torpedos(list): Torpedoes to remove.
        '''

        if reason_for_check == LIFE_CHECK:
            dead_torpedos = []
            for torpedo in self.__torpedo_list:
                if torpedo.is_dead():
                    dead_torpedos.append(torpedo)

        for torpedo in dead_torpedos:
            if torpedo in self.__torpedo_list:
                self._screen.unregister_torpedo(torpedo)
                self.__torpedo_list.remove(torpedo)

    def asteroid_update(self, dead_asteroids, new_asteroids=None):
        '''
        After asteroid collision, adds to asteroids list and registers
        new asteroids formed, and removes and unregisters dead asteroids.
        param dead_astroids(list): Asteroids to remove from game.
        param new_asteroids(list): Asteroids to add to game.
        '''

        if new_asteroids:
            for asteroid in new_asteroids:
                if asteroid not in self.__asteroids_list:
                    self._screen.register_asteroid(asteroid,
                                                   asteroid.get_size())
                    self.__asteroids_list.append(asteroid)

        for asteroid in dead_asteroids:
            if asteroid in self.__asteroids_list:
                self._screen.unregister_asteroid(asteroid)
                self.__asteroids_list.remove(asteroid)


    def ship_update(self):
        '''When ship hits asteroid, removes a life from ship and displays
        message to user.'''

        self.__ship.set_life()
        self._screen.show_message(LIFE_REDUCTION_TITLE, LIFE_REDUCTION_MSG)
        self._screen.remove_life()
        self.game_end()

    def new_asteroids(self, asteroid, torpedo):
        '''
        Creates and returns two different instances of Asteroid.
        Each new asteroid will receive the attributes of a previous asteroid.
        The asteroids will only differ by their opposite directions.
        param asteroid(Asteroid): The previous asteroid which has split.
        '''

        size = asteroid.get_size()
        direc = asteroid.get_direction()

        pos_vel_x = asteroid.new_pos_vel(HORZ, torpedo)
        pos_vel_y = asteroid.new_pos_vel(VERT, torpedo)
        asteroid_1 = Asteroid(pos_vel_x, pos_vel_y, direc, size - REDUCE_LIFE)

        pos_vel_x = asteroid.new_pos_vel(HORZ, torpedo, True)
        pos_vel_y = asteroid.new_pos_vel(VERT, torpedo, True)
        direc = (direc + HALF_CYCLE) % CYCLE
        asteroid_2 = Asteroid(pos_vel_x, pos_vel_y, direc, size - REDUCE_LIFE)

        return asteroid_1, asteroid_2

    def intersections(self):
        '''
        For all Asteroids in game, checks if there has been an intersection
        with a ship or with any of the torpedos in game.
        If collided with a ship: removes asteroid and removes life from ship.
        If collided with a torpedo: removes torpedo and asteroid, and if
        asteroid has life left, creates two smaller asteroids instead. Also
        adds points to ship.
        '''

        new_asteroids, dead_asteroids, dead_torpedos = [], [], []
        for asteroid in self.__asteroids_list:

                for torpedo in self.__torpedo_list:
                    if asteroid.has_intersection(torpedo) and \
                                    asteroid not in dead_asteroids:


                        dead_asteroids.append(asteroid)
                        if asteroid.get_size() > MIN_AST_SIZE:
                            aster1, aster2 = self.new_asteroids(asteroid,
                                                                torpedo)
                            new_asteroids.extend((aster1, aster2))
                        if torpedo not in dead_torpedos:
                            dead_torpedos.append(torpedo)
                        self.__ship.set_points(asteroid.get_size())
                        self.asteroid_update(dead_asteroids, new_asteroids)
                        self.torpedo_update(COLLISION, dead_torpedos)

                if asteroid.has_intersection(self.__ship) and \
                                    asteroid not in dead_asteroids:
                    dead_asteroids.append(asteroid)
                    self.asteroid_update(dead_asteroids, new_asteroids)
                    self.ship_update()


    def move(self):
        '''
        For all objects in game (ship, torpedos and asteroids),
        sets a new position, according to each object's direction and speed.
        '''

        obj_list = self.__asteroids_list + self.__torpedo_list
        obj_list.append(self.__ship)

        for obj in obj_list:
            old_pos_vel_x = obj.get_pos_vel(HORZ)
            old_pos_vel_y = obj.get_pos_vel(VERT)

            new_pos_x = (old_pos_vel_x[1] + old_pos_vel_x[0] -
                         self.screen_min_x)% self.__width + self.screen_min_x
            new_pos_y = (old_pos_vel_y[1] + old_pos_vel_y[0] -
                         self.screen_min_y)% self.__height + self.screen_min_y

            obj.set_new_pos(new_pos_x, new_pos_y)

    def draw_objects(self):
        '''Draws all objects (ship, torpedos and asteroids) on board.'''

        self._screen.draw_ship(self.__ship.get_pos_vel(HORZ)[0],
                self.__ship.get_pos_vel(VERT)[0], self.__ship.get_direction())

        for asteroid in self.__asteroids_list:
            self._screen.draw_asteroid(asteroid,
                asteroid.get_pos_vel(HORZ)[0], asteroid.get_pos_vel(VERT)[0])

        for torpedo in self.__torpedo_list:
            self._screen.draw_torpedo(torpedo, torpedo.get_pos_vel(HORZ)[0],
                        torpedo.get_pos_vel(VERT)[0], torpedo.get_direction())

    def game_end(self):
        '''
        End game if one of the following occurs:
        1. All asteroids have been blown up.
        2. Ship reaches zero life.
        3. User pressed 'q' key.
        '''

        game_end = False
        if len(self.__asteroids_list) < MIN_ASTS_IN_GAME :
            game_end = True
            msg = GAME_WIN_MSG
        elif self.__ship.get_life() <= MIN_SHIP_LIFE:
            game_end = True
            msg = GAME_LOSE_MSG
        elif self._screen.should_end():
            game_end = True
            msg = GAME_EXIT_MSG

        if game_end:
            self._screen.show_message(GAME_OVER_TITLE, msg)
            self._screen.end_game()
            sys.exit()

def main(amnt):
    '''Run game with parameter amnt of initial number of asteroids in game.'''
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main( int( sys.argv[1] ) )
    else:
        main( DEFAULT_ASTEROIDS_NUM )
