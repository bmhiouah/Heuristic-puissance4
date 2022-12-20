from player import Player
from copy import deepcopy
import sys
from random import *


evaluationTable = [[0 for i in range(7)] for j in range(6)]



evaluationTable2=[[5 ,  9  , 12  ,12,  11 , 9  , 5 ],  
[6   ,10  ,8   ,16  ,11 , 8  , 8],   
[8   ,11  ,10 , 13 , 9  , 11 , 6],
[5   ,10  ,9   ,15  ,10  ,6  , 7],
[4  , 10 , 9   ,15 , 10  ,7  , 7],
[6   ,9   ,12 , 10 , 11 , 6   ,8]]
def pow4_lignes(i,j):
    nbre_de_gain=0
    for k in range(4):
        if   -1<j-k<7 and -1<j-k+3<7:
            nbre_de_gain += 1

    return nbre_de_gain


def pow4_colonnes(i,j):
    nbre_de_gain=0
    for k in range(4):
        if   -1<i-k<6 and -1<i-k+3<6:
            nbre_de_gain += 1

    return nbre_de_gain

def pow4_diag_desc(i,j):
    nbre_de_gain=0
    for k in range(4):
        if (-1<i-k<6 and -1<j-k<7) and (-1<i-k+3<6 and -1<j-k+3<7):
            nbre_de_gain +=1
    return nbre_de_gain


def pow4_diag_mont(i,j):
    nbre_de_gain = 0
    for k in range(4):
        if (-1<i+k<6 and -1<j-k<7) and (-1<i+k-3<6 and -1<j-k+3<7 ):
            nbre_de_gain += 1
    return nbre_de_gain


for i in range(6):
    for j in range(7):
        evaluationTable[i][j] = (pow4_colonnes(i,j) + pow4_diag_desc(i,j) + pow4_diag_mont(i,j) + pow4_lignes(i,j))

        #j'ai utilisé la ligne suivante afin de trouver une heuristic capable de battre l'heuristic classic 
        #elle est censé gagné si elle joue en premier
        #evaluationTable2[i][j] = (pow4_colonnes(i,j) + pow4_diag_desc(i,j) + pow4_diag_mont(i,j) + pow4_lignes(i,j))+ randint(0,3)
            
    #     print(evaluationTable2[i][j], end = "")
    #     for i in range(4 -len(str(evaluationTable2[i][j]))):
    #         print(" ", end = "")
    # print("")
           






class AIPlayer(Player):
    """This player should implement a heuristic along with a min-max and alpha
    beta search to """

    def __init__(self):
        super().__init__()
        self.name = "Barbare Sauvage" 

    
    def getColumn(self, board):
        return self.alphabeta(board)

    
#vous pouvez changer le chiffre 4 qui indique la profondeur à laquelle votre
#IA va aller dans l'arbre de jeu.
    def alphabeta(self, board, profondeurmax=4):


        def heuristic(board,color):
            """
                Evalue un plateau de jeu en retournant un entier.
                board: le plateau de jeu
                color: le joueur pour qui on calcule le meilleur coup (Max)
                        soit -1, soit +1
            """
            # TODO(student): implement this!
            # il est attendu que la fonction renvoie un entier
            # une grande valeur étant plutôt favorable pour Max
            if board.winner == color:
                return 10000 #mettez la valeur max de votre heuristique ici
            elif board.winner == -color:
                return -10000 #mettez la valeur min de votre heuristique ici
            elif board.isFull():
                #pas de gagnant, mais la grille est pleine (match nul)
                return 0
            else:
                ############################################################################
                #l'idée de cet heuristique est baser sur une table d'évalution
                #la table est construite ci-dessus
                #l'idée de construction est qu'une case (i,j) a d'autant plus de valeur qu'elle est impliqué dans
                #des possibles puissance 4
                #c'est une heuristique très logique et j'imagine que je ne serais pas le seul à l'utiliser
                #quand elle joue contre elle même en 'joueur 2' elle gagne 
                #c'est pour cette raison qu'elle change pas
                #sinon 
                #############################################################################
                if color == -1:
                    sum = 0
                    for i in range(6):
                        for j in range(7):
                            if (board[i,j] == color):
                                sum += evaluationTable[i][j]
                            else:
                                if (board[i,j] == -color):
                                    sum -= evaluationTable[i][j]
                    if board[5,3] == -1:
                        return sum 
                    else:
                        return sum - 5
                else:
                    sum = 0
                    for i in range(6):
                        for j in range(7):
                            if (board[i,j] == color):
                                sum += evaluationTable2[i][j]
                            else:
                                if (board[i,j] == -color):
                                    sum -= evaluationTable2[i][j]
                    if board[5,3] == 1:
                        return sum
                    else:
                        return sum - 5



#Ne pas toucher les fonctions qui suivent svp        
        def maxvalue(board, alpha, beta, hauteur):
            #terminal test
            if hauteur>=profondeurmax or board.winner!=None or board.isFull():
                return heuristic(board, self.color)
            v = -sys.maxsize
            for action in board.getPossibleColumns():
                boardcopy = deepcopy(board)
                boardcopy.play(self.color, action)
                v = max(v, minvalue(boardcopy, alpha, beta, hauteur+1))
                if v>=beta:
                    return v
                alpha = max(alpha,v)
            return v

        def minvalue(board, alpha, beta, hauteur):
            if hauteur>=profondeurmax or board.winner!=None or board.isFull():
                return heuristic(board, self.color)
            v = sys.maxsize
            for action in board.getPossibleColumns():
                boardcopy = deepcopy(board)
                boardcopy.play(-self.color, action)
                v = min(v, maxvalue(boardcopy, alpha, beta, hauteur+1))
                if v<=alpha:
                    return v
                beta = min(beta,v)
            return v

        meilleur_score = -sys.maxsize
        beta = sys.maxsize
        coup = None
        possibleplays = board.getPossibleColumns()
        if len(possibleplays)==0:
            raise Error("Il ne devrait pas y avoir 0 coup à jouer")
        elif len(possibleplays)==1:
            return possibleplays[0]
        else:
            for action in possibleplays:
                boardcopy = deepcopy(board)
                boardcopy.play(self.color, action)
                v = minvalue(boardcopy, meilleur_score, beta, 1)
                if v>meilleur_score:
                    meilleur_score = v
                    coup = action

            return coup
            
