from Heuristics import Heuristics 

class Ai:
    """
    Class for handling computers inputs. Minimax algorithm + Alpha Beta pruning.

    Attributes:
        mark (char): players mark
        num_of_figures (int): number of figures
        _game_instance (Game): game object
        _opponent_mark (char): opponents mark
        _num_of_left_over_figures (int): number of figures to place on table
        DEPTH (int): depth for minimax tree
    """

    def __init__(self, mark, game_instance):
        """
        Args:
            mark (char): players (AI) mark
            game_instance (Game): game object
        """
        self.mark = mark
        self.num_of_figures = 9
        self._game_instance = game_instance
        self._opponent_mark = 'B' if mark == 'W' else 'W'
        self._he = Heuristics(game_instance)
        self._num_of_left_over_figures = 9
        self.DEPTH = 3

    def _find_opponents_mark(self, mark):
        """
        Returns opponents mark based on another players mark.
        """
        if mark == self.mark:
            return self._opponent_mark
        else:
            return self.mark

    def _minimax_phase1(self, depth, alpha, beta, mark):
        """
        Minimax algorithm + Alpha beta pruning for phase 1. Recursive.

        Args:
            depth (int): depth of minimax tree
            alpha (int): alpha value for alpha-beta pruning
            beta (int): beta value for alpha-beta pruning
            mark (char): players mark
        Return:
            (int): value of current game state
        """
        free_positions = self._game_instance.find_free_positions()
        position_to_eat = None
        opponents_mark = self._find_opponents_mark(mark)

        for i in free_positions:
            self._game_instance.place_figure_on_table(mark, i)
            
            if self.check_closed_morris(mark, i):
                position_to_eat = self._eat_figure(opponents_mark)
                if position_to_eat != None:
                    self._game_instance.free_position(position_to_eat)
            
            if depth == 0:
                heuristics = self._he.heuristics_placing(i, self.mark, self._opponent_mark)
                self._game_instance.free_position(i)

                if position_to_eat != None:
                    self._game_instance.place_figure_on_table(opponents_mark, position_to_eat)

                return heuristics
            else: 
                vrednost = self._minimax_phase1(depth - 1, alpha, beta, opponents_mark)
                self._game_instance.free_position(i)

                if position_to_eat != None:
                    self._game_instance.place_figure_on_table(opponents_mark, position_to_eat)

                if mark == self.mark:
                    if vrednost > alpha:
                        alpha = vrednost
                    if alpha >= beta:
                        return beta
                else:
                    if vrednost < beta:
                        beta = vrednost
                    if beta <= alpha: 
                        return alpha  

        if mark == self.mark:
            return alpha
        else:
            return beta

    def place_figure(self):
        """
        Finds best move for Ai to place the figure on the table by calling minimax algorithm for every free position.

        Return:
            position (int): best position on table to place figure
        """
        a = -10000
        free_positions = self._game_instance.find_free_positions()
        moves = []

        for i in free_positions:
            self._game_instance.place_figure_on_table(self.mark, i)

            vrednost = self._minimax_phase1(self.DEPTH, -10000, 10000, self._opponent_mark)
            self._game_instance.free_position(i)
            
            if vrednost > a:
                a = vrednost
                moves = [i]
            elif vrednost == a:
                moves.append(i)
            
        import random
        position = random.choice(moves)

        print("\n[AI] I placed figure on ", position)
        self._num_of_left_over_figures -= 1
        return position

    def _check_if_blocked(self, position):
        """
        Checks if passed position of figure is blocked so it can't be moved anywhere else. Returns true/false.
        """
        routes = self._game_instance._possible_routes

        for i in routes[position]:
            if self._game_instance._table[i] == 'X':
                return False

        return True
    
    def _find_possible_positions(self, old_positions):
        """
        Return array of positions where figure on old_position can be moved.

        Args:
            old_position (int): old_position of figure to be moved somewhere
        Return:
            possible_positions (int[]): array of posible positions
        """
        routes = self._game_instance._possible_routes
        possible_positions = []

        for i in routes[old_positions]:
            if self._game_instance._table[i] == 'X':
                possible_positions.append(i)

        return possible_positions

    def _minimax_phase2(self, depth, alpha, beta, mark):
        """
        Minimax algorithm + Alpha beta pruning for phase 2. Recursive.

        Args:
            depth (int): depth of minimax tree
            alpha (int): alpha value for alpha-beta pruning
            beta (int): beta value for alpha-beta pruning
            mark (char): players mark
        Return:
            (int): value of current game state
        """
        occupied_positions = self._game_instance.find_occupied_positions(mark)
        position_to_eat = None
        opponents_mark = self._find_opponents_mark(mark)

        for i in occupied_positions:
            if self._check_if_blocked(i):
                continue
            
            possible_positions = self._find_possible_positions(i)

            for j in possible_positions:
                self._game_instance.free_position(i)
                self._game_instance.place_figure_on_table(mark, j)

                if self.check_closed_morris(mark, j):
                    position_to_eat = self._eat_figure(opponents_mark)
                    if position_to_eat != None:
                        self._game_instance.free_position(position_to_eat)

                if depth == 0:
                    heuristics = self._he.heuristics_moving(j, self.mark, self._opponent_mark)
                    self._game_instance.free_position(j)
                    self._game_instance.place_figure_on_table(mark, i)

                    if position_to_eat != None:
                        self._game_instance.place_figure_on_table(opponents_mark, position_to_eat)

                    return heuristics
                else:
                    vrednost = self._minimax_phase2(depth - 1, alpha, beta, opponents_mark)
                    self._game_instance.free_position(j)
                    self._game_instance.place_figure_on_table(mark, i)

                    if position_to_eat != None:
                        self._game_instance.place_figure_on_table(opponents_mark, position_to_eat)

                    if mark == self.mark:
                        if vrednost > alpha:
                            alpha = vrednost
                        if alpha >= beta:
                            return beta
                    else:
                        if vrednost < beta:
                            beta = vrednost
                        if beta <= alpha:
                            return alpha

        if mark == self.mark:
            return alpha
        else:
            return beta

    def move_figure(self):
        """
        Finds best move for Ai to move the figure on the table by calling minimax algorithm for every figure.

        Return:
            move_position (int): best position on table to move figure
        """
        a = -10000
        occupied_positions = self._game_instance.find_occupied_positions(self.mark)
        move_position = None
        old_position = None

        for i in occupied_positions:
            if self._check_if_blocked(i):
                continue

            possible_positions = self._find_possible_positions(i)

            for j in possible_positions:
                self._game_instance.free_position(i)
                self._game_instance.place_figure_on_table(self.mark, j)

                value = self._minimax_phase2(self.DEPTH, -10000, 10000, self._opponent_mark)

                self._game_instance.free_position(j)
                self._game_instance.place_figure_on_table(self.mark, i)

                if value > a:
                    a = value
                    move_position = j
                    old_position = i
                
        print("\n[AI] I moved figure from " + str(old_position) + " to " + str(move_position))
        self._game_instance.move_player(self.mark, old_position, move_position)
        return move_position

    def check_closed_morris(self, mark, last_position):
        """
        Checks if a player closed morris in the last move.

        Args:
            mark (char): player mark
            last_position (int): last position
        Return:
            (bool): returns if morris is closed or not
        """
        for i, j, k in self._game_instance._possible_morrises:
            if i == last_position or j == last_position or k == last_position:
                if self._game_instance._table[i] == self._game_instance._table[j] == self._game_instance._table[k] and self._game_instance._table[i] == mark:
                    return True

        return False

    def _find_opponents_positions(self, opponent_mark):
        """
        Returns array of opponents positions on the table.
        """
        table = self._game_instance._table
        opponent_positions = []

        for i in range(0, len(table)):
            if table[i] == opponent_mark and not self.check_closed_morris(opponent_mark, i):
                opponent_positions.append(i)

        return opponent_positions

    def _eat_figure(self, opponents_mark):
        """
        Runs heuristics for possible figures to eat and chooses which one to eat.

        Args:
            opponents_mark (char): opponents mark
        Return:
            positions (int): best position to eat
        """
        opponents_positions = self._find_opponents_positions(opponents_mark)
        max_score = None
        position = None

        for i in opponents_positions:
            self._game_instance.free_position(i)
            score = self._he.heuristics_eat_figure(self.mark, self._opponent_mark)
            self._game_instance.place_figure_on_table(opponents_mark, i)

            if max_score == None or score > max_score:
                max_score = score
                position = i
            
        return position

    def eat_figure(self):
        """
        Eats figure from table.

        Return:
            position (int): position to eat figure or -1 if there is not any figure to eat
        """
        positions = self._eat_figure(self._opponent_mark)
        print("\n[AI] I ate figure from " + str(positions))

        if positions == None:
            return -1

        return positions