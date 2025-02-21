import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Initialisierung
pygame.init()

# Fenstergröße
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Subway Surfers 3D')

# Kamera- und Charakterparameter
player_x, player_y, player_z = 0, 0, 5
player_speed = 0.1
jumping = False
jump_height = 0.0
gravity = 0.02
jump_strength = 0.3

# Setup der Perspektive
gluPerspective(45, (screen_width / screen_height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Funktion, um den Spieler als Würfel zu zeichnen
def draw_player():
    glBegin(GL_QUADS)
    # Vorderseite
    glColor3f(1, 0, 0)
    glVertex3f(-0.25, -0.25, 0.25)
    glVertex3f(0.25, -0.25, 0.25)
    glVertex3f(0.25, 0.25, 0.25)
    glVertex3f(-0.25, 0.25, 0.25)

    # Rückseite
    glVertex3f(-0.25, -0.25, -0.25)
    glVertex3f(-0.25, 0.25, -0.25)
    glVertex3f(0.25, 0.25, -0.25)
    glVertex3f(0.25, -0.25, -0.25)

    # Oben
    glVertex3f(-0.25, 0.25, -0.25)
    glVertex3f(-0.25, 0.25, 0.25)
    glVertex3f(0.25, 0.25, 0.25)
    glVertex3f(0.25, 0.25, -0.25)

    # Unten
    glVertex3f(-0.25, -0.25, -0.25)
    glVertex3f(0.25, -0.25, -0.25)
    glVertex3f(0.25, -0.25, 0.25)
    glVertex3f(-0.25, -0.25, 0.25)

    # Rechts
    glVertex3f(0.25, -0.25, -0.25)
    glVertex3f(0.25, 0.25, -0.25)
    glVertex3f(0.25, 0.25, 0.25)
    glVertex3f(0.25, -0.25, 0.25)

    # Links
    glVertex3f(-0.25, -0.25, -0.25)
    glVertex3f(-0.25, -0.25, 0.25)
    glVertex3f(-0.25, 0.25, 0.25)
    glVertex3f(-0.25, 0.25, -0.25)
    glEnd()

# Funktion, um einen Zug zu zeichnen (einfacher Block)
def draw_train(x_position):
    glPushMatrix()
    glTranslatef(x_position, 0, 0)
    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    for z in [-0.5, 0.5]:
        for y in [-0.25, 0.25]:
            glVertex3f(-1, y, z)
            glVertex3f(1, y, z)
            glVertex3f(1, -y, z)
            glVertex3f(-1, -y, z)
    glEnd()
    glPopMatrix()

# Hauptspiel-Loop
def game_loop():
    global player_x, player_y, player_z, jumping, jump_height
    run = True
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # Bewegungssteuerung
        if keys[K_a]:
            player_x -= player_speed
        if keys[K_d]:
            player_x += player_speed
        if keys[K_w]:
            player_z -= player_speed
        if keys[K_s]:
            player_z += player_speed

        # Sprungsteuerung
        if keys[K_SPACE] and not jumping:
            jumping = True
            jump_height = 0.3

        if jumping:
            player_y += jump_height
            jump_height -= gravity
            if player_y <= 0:
                jumping = False
                player_y = 0

        # Kamera-Position
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)
        glRotatef(20, 1, 0, 0)  # Kamera leicht nach unten gerichtet
        glTranslatef(0.0, 0.0, 5)

        # Szene zeichnen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Zeichne Züge
        draw_train(-3)
        draw_train(3)

        # Zeichne Spieler
        draw_player()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Spiel starten
game_loop()
