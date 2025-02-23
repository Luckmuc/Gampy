import pygame
import sys
import random

pygame.init()

# Farben und Abmessungen
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)

WIDTH, HEIGHT = 300, 300
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 15
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = 'X'
game_over = False

# Definiere ein benutzerdefiniertes Event für den Bot
BOT_EVENT = pygame.USEREVENT + 1

def draw_grid():
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE), LINE_WIDTH)

def draw_moves():
    font = pygame.font.Font(None, 100)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            move = board[row][col]
            if move:
                text = font.render(move, True, RED if move == 'X' else BLUE)
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE / 2, row * CELL_SIZE + CELL_SIZE / 2))
                screen.blit(text, text_rect)

def check_winner():
    global game_over
    # Zeilen prüfen
    for row in range(GRID_SIZE):
        if board[row][0] == board[row][1] == board[row][2] != '':
            game_over = True
            return board[row][0]
    # Spalten prüfen
    for col in range(GRID_SIZE):
        if board[0][col] == board[1][col] == board[2][col] != '':
            game_over = True
            return board[0][col]
    # Diagonalen prüfen
    if board[0][0] == board[1][1] == board[2][2] != '':
        game_over = True
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        game_over = True
        return board[0][2]
    return None

def reset_game():
    global board, current_player, game_over
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = 'X'
    game_over = False
    pygame.time.set_timer(BOT_EVENT, 0)

def bot_move():
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == '']
    if empty_cells:
        return random.choice(empty_cells)
    return None

def draw_restart_button():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2), (BUTTON_WIDTH, BUTTON_HEIGHT))
    
    # Überprüfen, ob die Maus über dem Button schwebt
    if button_rect.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    # Button-Text anzeigen
    font = pygame.font.Font(None, 30)
    text = font.render("Restart", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

clock = pygame.time.Clock()
while True:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Spielerzug per Mausklick (nur wenn Spieler dran ist)
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == 'X':
            mouse_x, mouse_y = event.pos
            row, col = mouse_y // CELL_SIZE, mouse_x // CELL_SIZE
            if board[row][col] == '':
                board[row][col] = 'X'
                if not check_winner():
                    current_player = 'O'
                    pygame.time.set_timer(BOT_EVENT, 500)  # Bot-Zug verzögert um 500ms
        # Bot-Zug beim benutzerdefinierten Event
        elif event.type == BOT_EVENT and not game_over and current_player == 'O':
            move = bot_move()
            if move:
                row, col = move
                board[row][col] = 'O'
                check_winner()
                current_player = 'X'
            pygame.time.set_timer(BOT_EVENT, 0)  # Timer zurücksetzen
        # Neustart mit Button-Klick
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = event.pos
            button_rect = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2), (BUTTON_WIDTH, BUTTON_HEIGHT))
            if button_rect.collidepoint((mouse_x, mouse_y)):
                reset_game()

    draw_grid()
    draw_moves()

    if game_over:
        draw_restart_button()

    pygame.display.flip()
    clock.tick(30)
