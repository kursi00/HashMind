import pygame
import sys
import math

from a1_partd import overflow
from a1_partc import Queue
from player1 import PlayerOne
from player2 import PlayerTwo 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5
MAX_TIME_FOR_MOVE = 1000  # 1 second for AI to make a move

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((1200, 800))
pygame.font.init()
font = pygame.font.Font(None, 36)
bigfont = pygame.font.Font(None, 108)

# Load sprites
p1spritesheet = pygame.image.load('blue.png')
p2spritesheet = pygame.image.load('pink.png')

p1_sprites = [p1spritesheet.subsurface(pygame.Rect(32 * i, 0, 32, 32)) for i in range(8)]
p2_sprites = [p2spritesheet.subsurface(pygame.Rect(32 * i, 0, 32, 32)) for i in range(8)]

# Dropdown Menu for player selection
class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.current_option = 0

    def draw(self, window):
        pygame.draw.rect(window, BLACK, self.rect, 2)
        text = font.render(self.options[self.current_option], True, BLACK)
        window.blit(text, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        return self.current_option

# Difficulty Slider for controlling AI depth
class DifficultySlider:
    def __init__(self, x, y, width, height, min_depth, max_depth):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.current_depth = (min_depth + max_depth) // 2

    def draw(self, window):
        pygame.draw.rect(window, BLACK, self.rect, 2)
        fill_width = ((self.current_depth - self.min_depth) / (self.max_depth - self.min_depth)) * self.rect.width
        pygame.draw.rect(window, GRAY, (self.rect.x, self.rect.y, fill_width, self.rect.height))
        text = font.render(f"Depth: {self.current_depth}", True, BLACK)
        window.blit(text, (self.rect.x + 5, self.rect.y - 30))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            position_percentage = (event.pos[0] - self.rect.x) / self.rect.width
            self.current_depth = round(self.min_depth + position_percentage * (self.max_depth - self.min_depth))

    def get_depth(self):
        return self.current_depth

# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, window):
        pygame.draw.rect(window, BLACK, self.rect, 2)
        text_surface = font.render(self.text, True, BLACK)
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        window.blit(text_surface, (text_x, text_y))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# Game Board class with game state management
class Board:
    def __init__(self, width, height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height - 1][self.width - 1] = -1
        self.turn = 0

    def get_board(self):
        return [row.copy() for row in self.board]

    def add_piece(self, row, col, player):
        if self.valid_move(row, col, player):
            self.board[row][col] += player
            self.turn += 1
            return True
        return False

    def valid_move(self, row, col, player):
        return (0 <= row < self.height and 0 <= col < self.width and 
                (self.board[row][col] == 0 or self.board[row][col] / abs(self.board[row][col]) == player))

    def check_win(self):
        if self.turn > 0:
            num_p1, num_p2 = 0, 0
            for row in self.board:
                for cell in row:
                    if cell > 0:
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif cell < 0:
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if num_p1 == 0:
                return -1
            if num_p2 == 0:
                return 1
        return 0

    def do_overflow(self, q):
        oldboard = [row.copy() for row in self.board]
        numsteps = overflow(self.board, q)
        if numsteps != 0:
            self.set(oldboard)
        return numsteps

    def set(self, newboard):
        self.board = [row.copy() for row in newboard]

    def draw(self, window, frame):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE + Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    sprite = self.p1_sprites if self.board[row][col] > 0 else self.p2_sprites
                    cpos, rpos = col * CELL_SIZE + X_OFFSET, row * CELL_SIZE + Y_OFFSET
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE // 2 - 16
                        rpos += CELL_SIZE // 2 - 16
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2 - 16
                    elif abs(self.board[row][col]) == 3:
                        rpos += 8
                    elif abs(self.board[row][col]) == 4:
                        rpos += 8
                    window.blit(sprite[math.floor(frame)], (cpos, rpos))

# Main game variables
player1_dropdown = Dropdown(900, 50, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Human', 'AI'])
difficulty_slider = DifficultySlider(900, 400, 200, 50, 2, 6)
restart_button = Button(900, 460, 200, 50, 'Restart')

current_player = 0
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)
running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_row = -1
grid_col = -1
choice = [None, None]
start_time = pygame.time.get_ticks()
frame = 0

# Reset game function
def reset_game():
    global board, current_player, has_winner, overflow_boards, overflowing, numsteps, choice
    board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)
    current_player = 0
    has_winner = False
    overflow_boards = Queue()
    overflowing = False
    numsteps = 0
    choice = [None, None]

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif restart_button.is_clicked(event):
            reset_game()
        else:
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)
            difficulty_slider.handle_event(event)
            choice[0] = player1_dropdown.get_choice()
            choice[1] = player2_dropdown.get_choice()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    win = board.check_win()
    if win != 0:
        has_winner = True
        winner = 1 if win == -1 else 2

    if not has_winner:
        if overflowing:
            if not overflow_boards.is_empty():
                if repeat_step == FULL_DELAY:
                    next_board = overflow_boards.dequeue()
                    board.set(next_board)
                    repeat_step = 0
                else:
                    repeat_step += 1
            else:
                overflowing = False
                current_player = (current_player + 1) % 2
        else:
            if choice[current_player] == 1:
                grid_row, grid_col = bots[current_player].get_play(board.get_board())
                if not board.valid_move(grid_row, grid_col, current_player):
                    has_winner = True
                    winner = ((current_player + 1) % 2) + 1
                else:
                    make_move = True
            elif board.valid_move(grid_row, grid_col, current_player):
                make_move = True

            if make_move:
                board.add_piece(grid_row, grid_col, current_player)
                numsteps = board.do_overflow(overflow_boards)
                if numsteps != 0:
                    overflowing = True
                    repeat_step = 0
                else:
                    current_player = (current_player + 1) % 2
                grid_row, grid_col = -1, -1

    window.fill(WHITE)
    board.draw(window, frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))
    frame = (frame + 0.5) % 8
    player1_dropdown.draw(window)
    player2_dropdown.draw(window)
    difficulty_slider.draw(window)
    restart_button.draw(window)

    timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
    window.blit(timer_text, (900, 750))

    if has_winner:
        text = bigfont.render(f"Player {winner} wins!", True, BLACK)
        window.blit(text, (300, 250))
    else:
        status_text = font.render(f"Player {current_player + 1}'s turn", True, BLACK)
        window.blit(status_text, (X_OFFSET, 750))

    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
