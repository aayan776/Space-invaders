import pygame
import random
import math
import time
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.jpg")
pygame.display.set_icon(icon)
#Load assets
backgrounds = ['background1.jpg', 'background2.jpg', 'background3.jpg']
enemy_images = ['alien1.png', 'alien2.png', 'alien3.png', ]
#Player
player_img = pygame.image.load('spaceship.png')
player_img = pygame.transform.scale(player_img,  (80, 80))
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0
player_speed = 5
#Bullet
bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (32, 32))
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
def show_lives(x,y):
    life_text = font.render("Lives: " + str(lives), True, (255, 255, 255))
    screen.blit(life_text, (x, y + 40))
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
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27
#Initialize enemy
def initialize_enemy(level):
    enemy_img = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    number_of_enemies = level * 3
    for i in range(number_of_enemies):
        raw_enemy = pygame.image.load(random.choice(enemy_images))
        resized_enemy = pygame.transform.scale(raw_enemy, (32, 32))
        enemy_img.append(resized_enemy)
        enemy_x.append(random.randint(0, 735))
        enemy_y.append(random.randint(50, 150))
        enemy_x_change.append(1 + level * 0.5)
        enemy_y_change.append(10 + level)
    return enemy_img, enemy_x, enemy_y, enemy_x_change, enemy_y_change
#Initialize first level enemies
background = pygame.image.load(backgrounds[level - 1])
enemy_img, enemy_x, enemy_y, enemy_x_change, enemy_y_change = initialize_enemy(level)
#Game loop
running = True
while running:
    #RGB background
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Movement keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_UP:
                player_y_change = player_speed
            if event.key == pygame.K_DOWN:
                player_y_change = -player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_x_change = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                player_y_change = 0
    #Player movement
    player_x += player_x_change
    player_y += player_y_change
    player_x = max(0, min(player_x, 736))
    player_y = max(400, min(player_y, 536))
    #Enemy movement
    all_enemies_defeated = True
    for i in range(len(enemy_img)):
        if enemy_y[i] > 440:
            lives -= 1
            enemy_y[i] = random.randint(50, 150)
            if lives <= 0:
                game_over_text()
                running = False
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= 736:
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change[i]
        #Collision detection
        Collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if Collision:
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        if enemy_y[i] < 600:
            all_enemies_defeated = False
        enemy(enemy_x[i], enemy_y[i], i)
    #Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    #Check if level is cleared
    if all_enemies_defeated:
        level += 1
        if level > max_level:
            print("You win!")
            running = False
        else:
            show_level_screen(level)
            background = pygame.image.load(backgrounds[level - 1])
            enemy_img, enemy_x, enemy_y, enemy_x_change, enemy_y_change = initialize_enemy(level)
    player(player_x, player_y)
    show_score(text_x, text_y)
    show_lives(text_x, text_y)
    pygame.display.update()
