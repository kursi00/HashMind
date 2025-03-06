# Main Author: Ahmed Kursi
# Main Reviewer: Ahmed Kursi


from a1_partd import get_overflow_list, overflow
from a1_partc import Queue

# This function duplicates and returns the board. You may find this useful
def copy_board(board):
        # Initialize an empty list for the new board copy
        current_board = []
        height = len(board)
        # Loop through each row of the board and create a copy of each row
        for i in range(height):
            current_board.append(board[i].copy())
        return current_board
        
# Function to evaluate the board state for a given player
def evaluate_board(board, player):
        # Score if the player wins
    winningPoint = 100
        # Score if the player loses
    losingPoint = -100
        # Score if the game is a draw
    drawPoint = 0
        # Temporary value holder
    value = 0
        # Total sum of all cell values
    total = 0
        # Sum of player's cell values
    gem = 0
        
    # Loop through each cell in the board    
    for row in board:
        for cell in row:
                # Ignore empty cells
            if cell != 0:
                    # Calculate absolute value for easier summing
                if cell < 0:
                    value = -cell                 
                else:
                    value = cell
                total += value
                    # Add to gem count if cell belongs to the current player
                if player == 1 and cell > 0:
                    gem += value
                if player == -1 and cell < 0:
                    gem += value
                        
    # Determine win, loss, or draw conditions                    
    if gem == total:
        return winningPoint
    if gem == 0:
        return losingPoint
    if total == 0:
        return drawPoint
    # Calculate score as a percentage of control over the board
    score = (gem * 100) // total
    return score

class Node:
    def __init__(self, board, depth, player, tree_height = 4):
        # A node should have a board representing the game at the time of the move is done
        self.board = board
        # Depth is to determine where it is min's or max's turn at the point where node reached
        self.depth = depth
        # Player is who played the node
        self.player = player
        # After the node is played, there are possible outcomes the opponent could play, which the references are stored in this array
        self.children = []
        # The score is to store the min or max of the children, which will add up to determine the end game score
        self.score = None
        # The move of the player at the time node is played
        self.move = None
            
# Game Tree class
class GameTree:
    def __init__(self, board, player, tree_height = 4):
        # Store the starting player
        self.player = player
        # Create a copy of the initial board
        self.board = copy_board(board)
        # Initialize the root node with the starting board and player
        self.root = Node(board, 0, player)
        # Set the height of the game tree
        self.tree_height = tree_height
        # Build the game tree up to the specified height
        self.build_tree(self.root, tree_height)
            
    # Builds the game tree up to the specified height
    def build_tree(self, node, height):
         # Stop branching if max height is reached
        if height == 0:
            return

        # Traverse the board to find playable moves
        for i in range(len(node.board)):
            for j in range(len(node.board[0])):
                # If the cell is playable for the current player
                if node.board[i][j] == 0 or node.board[i][j] * node.player > 0:
                    # Create a copy of the board with the player's move
                    new_board = copy_board(node.board)
                    new_board[i][j] += node.player
                    # Check for overflow and apply it if necessary
                    if get_overflow_list(new_board):
                            a_queue = Queue()
                            a_queue.enqueue(new_board)
                            overflow(new_board, a_queue)
                            new_board = a_queue.dequeue()
                     # Create a child node for the opponent's turn
                    child_node = Node(new_board, node.depth + 1, -node.player)
                    # Record the move that generated this child node
                    child_node.move = (i, j)
                    # Add the child node to the current node's children
                    node.children.append(child_node)
                    # Recursively build the tree for the child node
                    self.build_tree(child_node, height - 1)

    # Minimax function to evaluate the best score for the player
    def minimax(self, node):
        # If no children, evaluate and set the score for this node
        if not node.children:
            node.score = evaluate_board(node.board, node.player)
            return node.score
        # Maximizer's turn (player's turn at even depths)
        if node.depth % 2 == 0:  
  
            node.score = max(self.minimax(child) for child in node.children)
            return node.score
        # Minimizer's turn (opponent's turn at odd depths)
        else:  
            # Choose the minimum score from child nodes
            node.score = min(self.minimax(child) for child in node.children)
            return node.score
    # Returns the best move for the player based on Minimax
    def get_move(self):
        best_score = float('-inf')
        best_move = None
        # Search and find the best move in children with minimax algorithm
        for child in self.root.children:
            score = self.minimax(child)
            if score > best_score:
                best_score = score
                best_move = child.move
        return best_move
   
    # This function clears the nodes in the tree one by one
    def clear_tree(self):
         self.delete_nodes(self.root)
         
    # Helper function for deleting nodes one by one starting from the children
    # It accepts node as the root
    def delete_nodes(self, node):
        if not node:
            return
        for child in node.children:
            self.delete_nodes(child)
        del node
