from Game import Game
from Human import Human
from Ai import Ai

if __name__ == "__main__":
    print("\n\n     ---===   Nine Mens Morris   ===---\n\n")

    game = Game()
    player1 = Human('W', game)
    player2 = Ai('B', game)
    game.set_igraci(player1, player2)
    game.postavi_figure()