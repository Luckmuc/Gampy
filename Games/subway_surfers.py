import pygame
import random
import time

# Initialisierung
pygame.init()

# Spiel-Parameter
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Subway Surfers (Simplified)')

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Charakter- und Hindernisparameter
player_width = 50
player_height = 50
player_x = screen_width / 2 - player_width / 2
player_y = screen_height - player_height - 10
player_speed = 5

obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacles = []

# Spiel-Loop
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)

def draw_player(x, y):
    pygame.draw.rect(screen, RED, (x, y, player_width, player_height))

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

def move_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed

def check_collision(player_x, player_y, obstacles):
    for obstacle in obstacles:
        if player_x < obstacle[0] + obstacle_width and player_x + player_width > obstacle[0]:
            if player_y < obstacle[1] + obstacle_height and player_y + player_height > obstacle[1]:
                return True
    return False

def display_score(score):
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

def game_loop():
    global player_x, player_y, obstacles

    running = True
    score = 0
    while running:
        screen.fill(WHITE)

        # Ereignisse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Tastensteuerung
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
            player_y += player_speed

        # Hindernisse erzeugen
        if random.random() < 0.05:
            obstacle_x = random.randint(0, screen_width - obstacle_width)
            obstacles.append([obstacle_x, -obstacle_height])

        # Hindernisse bewegen
        move_obstacles(obstacles)

        # Kollision überprüfen
        if check_collision(player_x, player_y, obstacles):
            running = False

        # Hindernisse entfernen, die außerhalb des Bildschirms sind
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] < screen_height]

        # Anzeige aktualisieren
        draw_player(player_x, player_y)
        draw_obstacles(obstacles)
        display_score(score)

        score += 1
        pygame.display.update()
        clock.tick(60)

# Spiel starten
game_loop()

pygame.quit()
