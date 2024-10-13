import pygame
import random

pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Screen dimensions (smaller size)
screen_width = 400
screen_height = 300

# Snake and food sizes (scaled down)
snake_block = 10
food_block = 10

# Game initialization
game_over = False
game_close = False

# Snake initial position and movement
snake_list = []
snake_length = 1
snake_speed = 12
snake_x = screen_width / 2
snake_y = screen_height / 2
snake_x_change = 0
snake_y_change = 0

# Food initial position
food_x = random.randrange(0, screen_width - food_block, 10)
food_y = random.randrange(0, screen_height - food_block, 10)

# Score
score = 0

# Game screen
game_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake in Box Game')

# Load background image
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Function to display score
def display_score(score):
    font = pygame.font.SysFont(None, 30)
    value = font.render(f"Score: {score}", True, black)
    game_display.blit(value, [10, 10])

# Game Loop
while not game_over:
    while game_close:
        game_display.fill(white)
        font_style = pygame.font.SysFont(None, 40)
        message = font_style.render('You Lost! Press Q-Quit or C-Play Again', True, red)
        game_display.blit(message, [screen_width / 6, screen_height / 3])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = True
                    game_close = False
                if event.key == pygame.K_c:
                    # Reset game variables
                    snake_list = []
                    snake_length = 1
                    snake_x = screen_width / 2
                    snake_y = screen_height / 2
                    snake_x_change = 0
                    snake_y_change = 0
                    food_x = random.randrange(0, screen_width - food_block, 10)
                    food_y = random.randrange(0, screen_height - food_block, 10)
                    score = 0
                    game_close = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_x_change = -snake_block
                snake_y_change = 0
            elif event.key == pygame.K_RIGHT:
                snake_x_change = snake_block
                snake_y_change = 0
            elif event.key == pygame.K_UP:
                snake_y_change = -snake_block
                snake_x_change = 0
            elif event.key == pygame.K_DOWN:
                snake_y_change = snake_block
                snake_x_change = 0

    if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
        game_close = True
    snake_x += snake_x_change
    snake_y += snake_y_change

    # Draw background
    game_display.blit(background, [0, 0])

    # Draw food
    pygame.draw.rect(game_display, red, [food_x, food_y, food_block, food_block])

    # Snake movement logic
    snake_head = [snake_x, snake_y]
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    for block in snake_list[:-1]:
        if block == snake_head:
            game_close = True

    # Draw snake
    for block in snake_list:
        pygame.draw.rect(game_display, black, [block[0], block[1], snake_block, snake_block])

    # Check if the snake eats food
    if snake_x == food_x and snake_y == food_y:
        food_x = random.randrange(0, screen_width - food_block, 10)
        food_y = random.randrange(0, screen_height - food_block, 10)
        snake_length += 1
        score += 10

    # Display the updated score
    display_score(score)

    pygame.display.update()

    pygame.time.Clock().tick(snake_speed)

pygame.quit()
