import pygame
import random
import math
import os

# Initialize pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Shooter Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Load and Scale Background Image
background = pygame.image.load('images/background3.png') if os.path.exists('images/background3.png') else None
if background:
    background = pygame.transform.scale(background, (800, 600))

# Player
player_img = pygame.image.load('images/ship.png') if os.path.exists('images/ship.png') else None
player_x = 370
player_y = 480
player_x_change = 0
player_speed = 3  # Adjusted player speed
player_width = 64
player_height = 64
if player_img:
    player_img = pygame.transform.scale(player_img, (player_width, player_height))

def player(x, y):
    if player_img:
        screen.blit(player_img, (x, y))
    else:
        pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height))

# Enemy
enemy_img = pygame.image.load('images/enemy_ship.png') if os.path.exists('images/enemy_ship.png') else None
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)
enemy_x_change = 1.2  # Further reduced enemy speed for balance
enemy_y_change = 40
enemy_width = 64
enemy_height = 64
if enemy_img:
    enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))

def enemy(x, y):
    if enemy_img:
        screen.blit(enemy_img, (x, y))
    else:
        pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height))

# Bullet
bullet_img = pygame.image.load('images/bullet.png') if os.path.exists('images/bullet.png') else None
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 5  # Slower bullet speed
bullet_state = "ready"  # "ready" means bullet is not on screen, "fire" means it's moving
bullet_width = 10
bullet_height = 20
if bullet_img:
    bullet_img = pygame.transform.scale(bullet_img, (bullet_width, bullet_height))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    if bullet_img:
        screen.blit(bullet_img, (x + 16, y + 10))
    else:
        pygame.draw.rect(screen, BLACK, (x + 16, y, bullet_width, bullet_height))

# Collision Detection
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

def show_score():
    score = font.render(f"Score: {score_value}", True, BLACK)
    screen.blit(score, (10, 10))

# Level Selection
def select_level():
    global enemy_x_change
    print("Select Difficulty: 1. Easy 2. Medium 3. Hard")
    difficulty = input("Enter difficulty level (1/2/3): ")
    if difficulty == '1':
        enemy_x_change = 1  # Very slow for easy
    elif difficulty == '2':
        enemy_x_change = 1.5  # Slightly faster
    elif difficulty == '3':
        enemy_x_change = 2  # Moderate for hard
    else:
        enemy_x_change = 1.5  # Default to medium if invalid input

# Game Loop
select_level()
running = True
while running:
    # Draw the background first
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE and bullet_state == "ready":  # Fire bullet when space is pressed and bullet is ready
                bullet_x = player_x  # Get the current x-coordinate of the player
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy movement
    enemy_x += enemy_x_change
    if enemy_x <= 0:
        enemy_x_change = abs(enemy_x_change)
        enemy_y += enemy_y_change
    elif enemy_x >= 736:
        enemy_x_change = -abs(enemy_x_change)
        enemy_y += enemy_y_change

    # Bullet movement
    if bullet_y <= 0:  # Reset bullet when it reaches the top
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Collision detection
    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if collision:
        bullet_y = 480
        bullet_state = "ready"
        score_value += 1
        # Respawn the enemy
        enemy_x = random.randint(0, 736)
        enemy_y = random.randint(50, 150)

    # Draw player and enemy
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)

    # Display score
    show_score()

    # Update screen
    pygame.display.update()
