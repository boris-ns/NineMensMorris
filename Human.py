class Human:
    """
    Class for handling interaction between user and computer.

    Attributes:
        mark (char): User mark
        game_instance (Game): game object
        num_of_figures (int): number of players (users) figures
        opponent_mark (char): opponents mark
        num_left_over_figures (int): number of figures to place on table
    """

    def __init__(self, mark, game_instance):
        """
        Args:
            mark (char): User mark
            game_instance (Game): game object
        """
        self.mark = mark
        self.game_instance = game_instance
        self.num_of_figures = 9
        self.opponent_mark = 'B' if mark == 'W' else 'W'
        self.num_left_over_figures = self.num_of_figures

    def place_figure(self):
        """
        Sets the figure on entered position. Before that checks if it is valid value for position.

        Return:
            position (int): entered position
        """
        while True:
            try:
                position = int(input("\n[{}][{}] enter position: ".format(self.mark, self.num_left_over_figures)))
            except ValueError:
                print("You entered wrong value!")
                continue

            # TODO: Move to Game class
            if self.game_instance.place_figure_on_table(self.mark, position):
                self.num_left_over_figures -= 1
                return position

            print("You can't place figure on ", position)

    def move_figure(self):
        """
        Gets input for old and new position and moves figure to new position.

        Return:
            new_position (int): new position
        """
        while True:
            try:
                old_position = int(input("\n[{}][{}] enter position of figure you want to move: ".format(self.mark, self.num_of_figures)))
                new_position = int(input("[{}] enter new position: ".format(self.mark)))
            except ValueError:
                print("You entered wrong value!")
                continue
            
            if self.game_instance.move_player(self.mark, old_position, new_position):
                return new_position

            print("You can't move figure to  ", new_position)

    def eat_opponents_figure(self):
        """
        Gets input to remove figure from table and returns the position of removed figure.

        Return:
            position (int): position of removed figure
        """
        while True:
            if not self.game_instance.all_in_morris(self.opponent_mark):
                return -1

            try:
                position = int(input("\n[{}] enter position to eat opponents figure: ".format(self.mark)))
            except ValueError:
                print("You entered wrong value!")
                continue

            if self.game_instance.eat_figure(self.mark, position):
                return position

            print("You can't remove figure on position ", position)