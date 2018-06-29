#############################################################
# FILE: game.py
# WRITER: Keren Meron, keren.meron, 200039626
# EXERCISE: intro2cs ex8 2015-2016
# DESCRIPTION: class of 'game' as part of a battleship game
#############################################################

############################################################
# Imports
############################################################
import game_helper as gh

############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a board and a user which
    tries to guess the locations of the ships by guessing their coordinates.
    """

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board
        :param ships: A list of ships that participate in the game.
        :return: A new Game object.
        """
        self.__board_size = board_size
        self.__ships = ships
        self.__bombs_dict = dict()


    def __play_one_round(self):
        """
         The function runs one round of the game:
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits
             and terminated ships)
        :return: none.
        """

        hit_list = list()
        curr_round_hits = list()
        not_hit_list = list()

        user_coord = gh.get_target(self.__board_size)
        self.__bombs_dict[user_coord] = 4

        curr_round_hits, hit_list, not_hit_list = self.move_ship(self.__ships,
                        curr_round_hits, hit_list, not_hit_list, user_coord)
        self.update_bombs()
        print(gh.board_to_string(self.__board_size, curr_round_hits,
                                 self.__bombs_dict, hit_list, not_hit_list))
        terminated_count = self.remove_terminated_ships()
        gh.report_turn(len(curr_round_hits), terminated_count)


    def update_bombs(self):
        '''Removes a life from each bomb, and removes dead bombs.'''

        for bomb in self.__bombs_dict:
            self.__bombs_dict[bomb] -= 1
        self.remove_dead_bombs()

    def move_ship(self, ships, cur_round_hits, hit_list, not_hit_list, coord):
        '''Moves ships. Updates hits from current round and updates
        ships cells states. Returns: list of hits in current round,
        list of hit cells, list of cells not hit.'''

        for ship in self.__ships:
            ship.move()
            curr_round_hits = self.update_hits(ship, cur_round_hits, coord)
            hit_list, not_hit_list = self.cells_hit_or_not(ship, hit_list,
                                        not_hit_list, cur_round_hits)

        return cur_round_hits, hit_list, not_hit_list

    def update_hits(self, ship, curr_round_hits, user_coord):
        '''Checks if any ship was hit by either old or new bomb, and if yes
        updates the current hit list accordingly. Kills life of bomb which has
        hit so that it will be diminished.
        Returns curr_round_hits list.'''

        #if hit from new bomb
        if ship.hit(user_coord):
                    curr_round_hits.append(user_coord)
                    self.__bombs_dict[user_coord] = 1

        #if moved ship hit old bomb
        for coord in ship.coordinates():
            if coord not in ship.damaged_cells() and \
                    self.check_new_hit(coord, ship):
                self.__bombs_dict[coord] = 1
                if coord not in curr_round_hits:
                    curr_round_hits.append(coord)

        return curr_round_hits

    def cells_hit_or_not(self, ship, hit_list, not_hit_list, curr_round_hits):
        '''Allocates all ship cells either to hit list or to not hit list.
        Returns hit_list and not_hit_list.'''

        for coord in ship.coordinates():
            if ship.cell_status(coord) and coord not in curr_round_hits:
                hit_list.append(coord)
            else:
                not_hit_list.append(coord)
        return hit_list, not_hit_list

    def remove_terminated_ships(self):
        '''Checks if a ship is terminated (all cells have been bombed).
        If terminated, removes the ship from game.
        Returns number of ships terminated.'''

        ships_to_terminate = []
        terminated_count = 0
        for ship in self.__ships:
            if ship.terminated():
                terminated_count += 1
                ships_to_terminate.append(ship)

        for i in ships_to_terminate:
            self.__ships.remove(i)

        return terminated_count

    def __repr__(self):
        """
        Return a string representation of the board's game.
        :return: A tuple converted to string. The tuple should contain:
            1. Board's size.
            2. A dictionary of the bombs found on the board
                 {(pos_x, pos_y) : remaining turns}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        rep_tpl = (self.__board_size, self.__bombs_dict, self.__ships)
        return str(rep_tpl)

    def check_new_hit(self, coord, ship):
        '''Checks if a cell ship has been hit by a bomb that was placed in
        previous turns. If yes, returns True, otherwise None.
        If yes, adds cell to ship's hits list.'''

        if coord in self.__bombs_dict and self.__bombs_dict[coord] < 4:
            ship.add_hit(coord)
            return True

    def remove_dead_bombs(self):
        '''Removes bombs with expired (zero) life from bomb_dict.'''

        remove = [bomb for bomb in self.__bombs_dict
                  if self.__bombs_dict[bomb] == 0]
        for bomb in remove:
            del self.__bombs_dict[bomb]

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        completion.
        Initializes ship's orientation and coordinates.
        Plays rounds until all ships have been terminated.
        :return: None
        """

        gh.report_legend()

        for ship in self.__ships:
            ship.set_orientation()

        ship_coords = [ship.coordinates() for ship in self.__ships]
        ship_coords = [i for lst in ship_coords for i in lst]

        print(gh.board_to_string(self.__board_size, [], {}, [], ship_coords))

        while self.__ships:
            self.__play_one_round()

        gh.report_gameover()


############################################################
# An example usage of the game
############################################################
if __name__=="__main__":
    game = Game(5, gh.initialize_ship_list(4, 2))
    game.play()
