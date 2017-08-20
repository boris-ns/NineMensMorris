class Game:
    """
    Class for handling game logic

    Attributes:
        _possible_routes (dict): key-current position, value-array for possible moves from current position
        _possible_morrises (set): set of sets with possible morrises to close
        _table (char[]): game table , length=24
        _player1 (Human or Ai): player 1
        _player2 (Human or Ai): player 2
        _winner (char): winner of the game
    """

    _possible_routes = {
        0 : (1, 9),
        1 : (0, 2, 4),
        2 : (1, 14),
        3 : (4, 10),
        4 : (1, 3, 5, 7),
        5 : (4, 13),
        6 : (7, 11),
        7 : (4, 6, 8),
        8 : (7, 12),
        9 : (0, 10, 21),
        10: (3, 9, 11, 18),
        11: (6, 10, 15),
        12: (8, 13, 17),
        13: (5, 12, 14, 20),
        14: (2, 13, 23),
        15: (11, 16),
        16: (15, 17, 19),
        17: (12, 16),
        18: (10, 19),
        19: (16, 18, 20, 22),
        20: (13, 19),
        21: (9, 22),
        22: (19, 21, 23),
        23: (14, 22)
    }

    _possible_morrises = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),
                          (0,9,21), (3,10,18), (6,11,15), (1,4,7), (16,19,22), (8,12,17), (5,13,20), (2,14,23))

    def __init__(self):
        self._free_position = 'X'
        self._table = [self._free_position for i in range(24)]
        self._player1 = None
        self._player2 = None
        self._winner = None

    def find_free_positions(self):
        """
        Finds free positions on the table and returns array with indexes of those positions.
        """
        free_positions = []
        for i in range(len(self._table)):
            if self._table[i] == self._free_position:
                free_positions.append(i)

        return free_positions

    def find_occupied_positions(self, mark):
        """
        Finds positions of passed player mark and returns array with those indexes.
        """
        positions = []
        for i in range(len(self._table)):
            if self._table[i] == mark:
                positions.append(i)

        return positions

    def _check_position(self, position):
        """
        Checks if passed position exists.
        """
        if not 0 <= position < 24:
            return False
        
        return True

    def check_if_closed_morris(self, mark, last_move):
        """
        Checks if player with mark attribute closed a morris with last move.

        Args:
            mark (char): player mark
            last_move (int): last occupied position by player with passed mark
        Return:
            (bool): true if player closed a morris, else false
        """
        for i, j, k in self._possible_morrises:
            if i == last_move or j == last_move or k == last_move:
                if self._table[i] == self._table[j] == self._table[k] and self._table[i] == mark:
                    return True

        return False

    def all_in_morris(self, mark):
        """
        Checks if all figures of player with passed mark are in closed morrises. Returns true/false.
        """
        for i in range(len(self._table)):
            if self._table[i] == mark:
                for j, k, l in self._possible_morrises:
                    if not self._table[j] == self._table[k] == self._table[l] == mark:
                        return True
        
        return False

    def _check_moving_route(self, old_position, new_position):
        """
        Check if figure can move on new_position from old_position. Returns true/false.
        """
        if new_position in self._possible_routes[old_position]:
            return True

        return False

    def _check_if_all_figures_blocked(self, mark):
        """
        Checks if all players figures with passed mark are blocked. Returns true/false.
        """
        positions = []

        for i in range(len(self._table)):
            if self._table[i] == mark:
                positions.append(i)

        blocked = True
        for i in positions:
            blocked = self._check_if_blocked(i)
            if not blocked:
                break

        return blocked

    def _check_if_blocked(self, position):
        """
        Check if passed position is blocked (can't move it anywhere else). Returns true/false.
        """
        for i in self._possible_routes[position]:
            if self._table[i] == 'X':
                return False

        return True

    def check_if_game_over(self):
        """
        Checks if game is finished. Game is finished if one player has all its figures blocked or player has only
                2 figures left. Returns true/false.
        """
        if self._player1.num_of_figures == 2 or self._check_if_all_figures_blocked(self._player1.mark):
            self._winner = self._player2.mark
            return True
        if self._player2.num_of_figures == 2 or self._check_if_all_figures_blocked(self._player1.mark):
            self._winner = self._player1.mark
            return True
        
        return False

    def place_figure_on_table(self, mark, position):
        """
        Places figure on table. Before that checks if it is possible to place figure on passed position.

        Args:
            mark (char): players mark to place on the table
            position (int): position to place figure
        Return:
            (bool): True if figure is placed, False if figure can't be placed on passed position.
        """
        if (not self._check_position(position)) or (self._table[position] != self._free_position):
            return False

        self._table[position] = mark
        return True

    def free_position(self, position):
        """
        Helper method for minimax. Removes figure from passed position.
        """
        self._table[position] = self._free_position

    def move_player(self, mark, old_position, new_position):
        """
        Moves player from old_position to new_position. Returns true if move is successful, else false.
        """
        condition_to_move = not self._check_position(old_position) or not self._check_position(new_position)
        try: # TODO: nadji malo bolji nacin za roveru ako se unese neki bezveze indeks jer ovako dolazi do exceptiona
             # a ruzno izgleda da se svi ovi uslovi stave u 1 if
            condition_position = self._table[old_position] != mark or self._table[new_position] != self._free_position
        except IndexError:
            condition_position = False

        if condition_to_move or condition_position or not self._check_moving_route(old_position, new_position):
             return False

        self._table[old_position] = self._free_position
        self._table[new_position] = mark
        return True

    def eat_figure(self, mark, position):
        """
        Removes figure from the table.

        Args:
            mark (char): mark of player who eats opponents figure
            position (int): position to remove figure from
        Return:
            (bool): true if eating is successful, else false
        """
        if not self._check_position(position) or self._table[position] == mark or self._table[position] == self._free_position:
            return False

        if mark == self._player1.oznaka:
            if self.check_if_closed_morris(self._player2.oznaka, position):
                return False

            self._player2.broj_figura -= 1
        else:
            if self.check_if_closed_morris(self._player1.oznaka, position):
                return False
                
            self._player1.broj_figura -= 1

        self._table[position] = self._free_position
        return True

    def set_players(self, player1, player2):
        """
        Setter for players.
        """
        self._player1 = player1
        self._player2 = player2

    def draw_table(self):
        """
        Draws table to the console.
        """
        table = [
            [self._table[0] + '00', '------------', self._table[1] + '01', '------------', self._table[2] + '02'],
            [' |              |              |'],
            [' |              |              |'],
            [' |   ', self._table[3] + '03', '-------', self._table[4] + '04', '-------', self._table[5] + '05', '   |'],
            [' |    |         |         |    |'],
            [' |    |         |         |    |'],
            [' |    |   ', self._table[6] + '06', '--', self._table[7] + '07', '--', self._table[8] + '08', '   |    |'],
            [' |    |    |         |    |    |'],
            [' |    |    |         |    |    |'],
            [self._table[9] + '09', '--', self._table[10] + '10', '--', self._table[11] + '11', '       ', self._table[12] + '12', '--', self._table[13] + '13', '--', self._table[14] + '14'],
            [' |    |    |         |    |    |'],
            [' |    |    |         |    |    |'],
            [' |    |   ', self._table[15] + '15', '--', self._table[16] + '16', '--', self._table[17] + '17', '   |    |'],
            [' |    |         |         |    |'],
            [' |    |         |         |    |'],
            [' |   ', self._table[18] + '18', '-------', self._table[19] + '19', '-------', self._table[20] + '20', '   |'],
            [' |              |              |'],
            [' |              |              |'],
            [self._table[21] + '21', '------------', self._table[22] + '22', '------------', self._table[23] + '23']
        ]

        for i in table:
            print("     ", end="")
            for j in i:
                print(j, end="")
            print()
    
    def _while_closed_morris(self, pozicija):
        """
        Method that is being called if while player closes the morris.
        """
        if self.check_if_closed_morris(self._player1.mark, pozicija):
            self.draw_table()
            position_eat = self._player1.eat_opponents_figure()
            if position_eat == -1:
                return
            self.eat_figure(self._player1.mark, position_eat)

    def _black_closed_morris(self, position):
        """
        Method that is being called if black player closes the morris.
        """
        if self.check_if_closed_morris(self._player2.mark, position):
            self.draw_table()
            position_eat = self._player2.eat_opponents_figure()
            if position_eat == -1:
                return
            self.eat_figure(self._player2.mark, position_eat)

    def place_figures_phase1(self):
        """
        Phase 1 for the game. Here game starts. This phase lasts maximum 18 moves.
        """
        self.draw_table()

        for move in range(18):
            if move % 2 == 0: # White on the move
                white_position = self._player1.place_figure()
                self.place_figure_on_table(self._player1.mark, white_position)
                self._while_closed_morris(white_position)
            else:              # Black on the move
                black_position = self._player2.place_figure()
                self.place_figure_on_table(self._player2.mark, black_position)
                self._black_closed_morris(black_position)

            self.draw_table()

        self.move_figures_phase2() # Start phase 2

    def move_figures_phase2(self):
        """
        Phase 2 for the game. Moving figures.
        """
        move = 0
        while not self.check_if_game_over():
            if move % 2 == 0: # White on the move
                position = self._player1.move_figure()
                self._while_closed_morris(position)
            else:              # Black on the move
                position = self._player2.move_figure()
                self._black_closed_morris(position)

            self.draw_table()
            move += 1

        self._print_winner()

    def _print_winner(self):
        """
        Prints winner.
        """
        print("\nPobednik je: ", self._winner)