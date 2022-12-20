import argparse

from player import HumanPlayer, RandomPlayer
from MHIOUAH_badre import *
from bis import AIPlayer2
from ui_game import UIGame


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--p1', default='player 1')
    parser.add_argument('--p2', default='player 2')
    args = parser.parse_args()

    player1 = AIPlayer()
    player1.name = 'joueur1'
    player2 = AIPlayer2()
    player2.name = 'joueur2'

    game = UIGame(player1, player2)

