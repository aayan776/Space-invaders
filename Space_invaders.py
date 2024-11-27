import pygame
import random
import math
import time
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.display.set_icon("ufo.jpg")
pygame.display.set_icon(icon)
#Load assets
backgrounds = ['background1.jpg', 'background2.jpg', 'background3.jpg']
enemy_images = ['alien1.png', 'alien2.png', 'alien3.png', ]
#Player
player_img = pygame.image.load('spaceship.png')
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0
player_speed = 5
#Bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"
#Mechanics
score_value = 0
lives = 3
#Font
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10
over_font = pygame.font.Font('freesansbold.ttf', 64)
#Level
level = 1
max_level = len(backgrounds)
#Fuction
def show_score(x,y):
    score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))
def show_level_screen(level):
    level_text = over_font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (300, 250))
    pygame.display.update()
    time.sleep(2)
def game_over_text():
    over_text = over_font.render("Game Over!", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
def player(x,y):
    screen.blit(player_img, (x,y))
def enemy(x,y,i):
    screen.blit(enemy_images[i], (x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27
#Initialize enemy
def initialize_enemy(level):
    enemy_images = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    number_of_enemies = level * 3
    for i in range(number_of_enemies):
        enemy_images.append(pygame.image.load(random.choice(enemy_images)))
        enemy_x.append(random.randint(0, 735))
        enemy_y.append(random.randint(50, 150))
        enemy_x_change.append(2 + level)
        enemy_y_change.append((30 + (level * 2)))
    return enemy_images, enemy_x, enemy_y, enemy_x_change, enemy_y_change
#Initialize first level enemies
background = pygame.image.load(backgrounds[level - 1])
enemy_images, enemy_x, enemy_y, enemy_x_change, enemy_y_change = initialize_enemy(level)
#Game loop
running = True
while running:
    