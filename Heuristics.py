class Heuristics:
    """
    Calculations for heuristic evaluation. Result is linear function.

    Attributes:
        game_instance (Game): game object
    """
    def __init__(self, game_instance):
        """
        Args:
            game_instance (Game): game object
        """
        self._game_instance = game_instance
    
    def _closed_morris(self, mark1, mark2, last_move):
        """
        Returns 1 if player1 closed a morris, -1 if player2 did, 0 if no one closed the morris in the last move.

        Args:
            mark1 (char): Player1 mark
            mark2 (char): Player2 mark
            last_move (int): last occupied position
        Return:
            1 if player1 closed the morris
            -1 if player2 closed the morris
            0 if no one closed the morris
        """
        possible_morrises = self._game_instance._possible_morrises
        table = self._game_instance._table

        for i, j, k in possible_morrises:
            if i == last_move or j == last_move or k == last_move:
                if table[i] == table[j] == table[k] == mark1:
                    return 1
                elif table[i] == table[j] == table[k] == mark2:
                    return -1
        
        return 0

    def _num_of_closed_morrises(self, mark):
        """
        Counting number of closed morrises.

        Args:
            mark (char): player mark
        Return:
            num_morrises (int): number of closed morrises
        """
        possible_morrises = self._game_instance._possible_morrises
        table = self._game_instance._table
        num_morrises = 0

        for i, j, k in possible_morrises:
            if table[i] == table[j] == table[k] == mark:
                num_morrises += 1
                
        return num_morrises

    def _num_of_blocked_figures(self, mark):
        """
        Finds positions of figures with passed mark and return number of blocked figures.

        Args:
            mark (char): player mark
        Return:
            num_of_blocked (int): number of blocked figures
        """
        table = self._game_instance._table
        positions = []

        for i in range(len(table)):
            if table[i] == mark:
                positions.append(i)

        num_of_blocked = self._find_num_of_blocked_figures(positions)
        return num_of_blocked

    def _find_num_of_blocked_figures(self, positions):
        """
        Helper method for _num_of_blocked_figures. This method counts number of blocked figures from
        passed positions array.

        Args:
            positions (int[]): positions of one players figures
        Return:
            num_of_blocked (int): number of blocked figures
        """
        move_positions = self._game_instance._possible_routes
        num_of_blocked = 0

        for i in positions:
            blocked = True
            for j in move_positions[i]:
                if self._game_instance._table[j] == 'X':
                    blocked = False
                    break
            
            if blocked:
                num_of_blocked += 1

        return num_of_blocked

    def _num_of_figures(self, mark):
        """
        Counts number of figures with passed mark.

        Args:
            mark (char): players mark
        Return:
            num_of_figures (int): number of figures
        """
        table = self._game_instance._table
        num_of_figures = 0

        for i in table:
            if i == mark:
                num_of_figures += 1

        return num_of_figures

    def _blocked_possible_morris(self, mark1, mark2):
        """
        Counts number of blocked opponents morrises.

        Args:
            mark1 (char): player1 mark
            mark2 (char): player2 mark
        Return:
            num_of_blocked (int): number of blocked opponents morrises
        """
        possible_morrises = self._game_instance._possible_morrises
        table = self._game_instance._table
        num_of_blocked = 0

        for i, j, k in possible_morrises:
            if (table[i] == table[j] == mark2 and table[k] == mark1) or (table[i] == table[k] == mark2 and table[j] == mark1) or (table[j] == table[k] == mark2 and table[i] == mark1):
                num_of_blocked += 1

        return num_of_blocked

    def _occupied_two_positions(self, mark):
        """
        Counts number of 2 piece configurations.

        Args:
            mark (char): player mark
        Return:
            num_of_confs (int): number of 2 piece configurations
        """
        possible_morrises = self._game_instance._possible_morrises
        table = self._game_instance._table
        num_of_confs = 0

        for i, j, k in possible_morrises:
            if (table[i] == table[j] == mark and table[k] == 'X') or (table[i] == table[k] == mark and table[j] == 'X') or (table[j] == table[k] == mark and table[i] == 'X'):
                num_of_confs += 1

        return num_of_confs

    def _possible_double_morris(self, mark):
        """
        Counts number of possible double morrises.

        Args:
            mark (char): player mark
        Return:
            num_of_morrises (int): number of double morrises
        """
        morrises = self._game_instance._possible_morrises
        table = self._game_instance._table
        possible_morrises = []

        for i, j, k in morrises:
            if (table[i] == table[j] == mark and table[k] == 'X') or (table[i] == table[k] == mark and table[j] == 'X') or (table[j] == table[k] == mark and table[i] == 'X'):
                possible_morrises.append((i, j, k))

        num_of_morrises = self._find_double_morrises(possible_morrises)
        return num_of_morrises

    def _double_morris(self, mark):
        """
        Counts double morrises.

        Args:
            mark (char): player mark
        Return:
            number of double morrises
        """
        morrises = self._game_instance._possible_morrises
        table = self._game_instance._table
        players_morrises = []

        for i, j, k in morrises:
            if table[i] == table[j] == table[k] == mark:
                players_morrises.append((i, j, k))

        return self._find_double_morrises(players_morrises)

    def _find_double_morrises(self, possible_morrises):
        """
        Helper method for finding double morrises that share one same figure.

        Args:
            possible_morrises (array of (i,j,k)): positions of possible morrises that player has
        Return:
            num_of_morrises (int): number of morrises
        """
        num_of_morrises = 0

        if len(possible_morrises) > 1:
            for i in range(len(possible_morrises) - 1):
                for j in range(i + 1, len(possible_morrises)):
                    if possible_morrises[i][0] in possible_morrises[j] or possible_morrises[i][1] in possible_morrises[j] or possible_morrises[i][2] in possible_morrises[j]:
                        num_of_morrises += 1
        
        return num_of_morrises

    def _game_over(self, mark1, mark2):
        """
        Calls game over method from Game class, and determines who is winner.

        Args:
            mark1 (char): player1 mark
            mark2 (char): player2 mark
        Return:
            1 if player1 won
            -1 if player2 won
            0 if draw
        """
        if self._game_instance.check_if_game_over():
            if self._game_instance._winner == mark1:
                return 1
            elif self._game_instance._winner == mark2:
                return -1

        return 0

    def heuristics_placing(self, last_move, mark1, mark2):
        """
        Calculates heuristic function for phase 1.

        Args:
            last_move (int): last occupied position
            mark1 (char): player1 mark
            mark2 (char): player2 mark
        Return:
            h (int): final score of game state
        """
        # Evaluation function for Phase 1 = 18 * (1) + 26 * (2) + 1 * (3) + 9 * (4) + 10 * (5) + 7 * (6)
        h = 0
        h += 18 * self._closed_morris(mark1, mark2, last_move)
        h += 26 * (self._num_of_closed_morrises(mark1) - self._num_of_closed_morrises(mark2))
        h += self._num_of_blocked_figures(mark2) - self._num_of_blocked_figures(mark1) # ili 4
        h += 9 * (self._num_of_figures(mark1) - self._num_of_figures(mark2))
        h += 10 * (self._occupied_two_positions(mark1) - self._occupied_two_positions(mark2))
        h += 7 * (self._possible_double_morris(mark1) - self._possible_double_morris(mark2)) # TODO proveri

        return h

    def heuristics_moving(self, last_move, mark1, mark2):
        """
        Calculates heuristic function for phase 2.

        Args:
            last_move (int): last occupied position
            mark1 (char): player1 mark
            mark2 (char): player2 mark
        Return:
            h (int): final score of game state
        """
        # Evaluation function for Phase 2 = 14 * (1) + 43 * (2) + 10 * (3) + 11 * (4) + 8 * (7) + 1086 * (8)
        h = 0
        h += 14 * self._closed_morris(mark1, mark2, last_move)
        h += 43 * (self._num_of_closed_morrises(mark1) - self._num_of_closed_morrises(mark2))
        h += 10 * (self._num_of_blocked_figures(mark2) - self._num_of_blocked_figures(mark1)) # ili 6
        h += 11 * (self._num_of_figures(mark1) - self._num_of_figures(mark2))
        h += 8 * (self._double_morris(mark1) - self._double_morris(mark2))
        h += 1086 * self._game_over(mark1, mark2)

        return h

    def heuristics_eat_figure(self, mark1, mark2):
        """
        Calculates heuristic function for "eating" figures.

        Args:
            mark1 (char): player1 mark
            mark2 (char): player2 mark
        Return:
            h (int): final score of game state
        """
        h = 0
        h += 43 * (self._num_of_closed_morrises(mark1) - self._num_of_closed_morrises(mark2))
        h += 10 * (self._num_of_blocked_figures(mark2) - self._num_of_blocked_figures(mark1))
        h += 11 * (self._num_of_figures(mark1) - self._num_of_figures(mark2))
        h += 8 * (self._double_morris(mark1) - self._double_morris(mark2))
        h += 1086 * self._game_over(mark1, mark2)

        return h