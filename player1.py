from a2_partb import GameTree

class PlayerOne:

    def __init__(self, name = "P1 Bot"):
        self.name = name
        
    def get_name(self):
        return self.name

    def get_play(self, board):
        tree = GameTree(board, 1)
        (row,col) = tree.get_move()
        return (row,col)