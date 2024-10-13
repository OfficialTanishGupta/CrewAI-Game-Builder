import pygame
import sys
import random

# Define constants for the screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define player size
PLAYER_SIZE = 50
PROJECTILE_SIZE = 5
ENEMY_SIZE = 50

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 2 * PLAYER_SIZE
        self.speed = 5

    def move(self, direction):
        if direction == "UP" and self.y > 0:
            self.y -= self.speed
        elif direction == "DOWN" and self.y < SCREEN_HEIGHT - PLAYER_SIZE:
            self.y += self.speed
        elif direction == "LEFT" and self.x > 0:
            self.x -= self.speed
        elif direction == "RIGHT" and self.x < SCREEN_WIDTH - PLAYER_SIZE:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, PROJECTILE_SIZE, PROJECTILE_SIZE))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, ENEMY_SIZE, ENEMY_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player()
    projectiles = []
    enemies = [Enemy(random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), 0) for _ in range(5)]
    score = 0
    game_over = False

    while not game_over:
        screen.fill(BLACK)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("LEFT")
        if keys[pygame.K_RIGHT]:
            player.move("RIGHT")
        if keys[pygame.K_UP]:
            player.move("UP")
        if keys[pygame.K_DOWN]:
            player.move("DOWN")
        if keys[pygame.K_SPACE]:
            projectiles.append(Projectile(player.x + PLAYER_SIZE // 2, player.y))

        # Enemy movement
        for enemy in enemies:
            enemy.move()
            if enemy.y >= SCREEN_HEIGHT:
                enemy.y = 0
                enemy.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)

        # Projectile movement
        for projectile in projectiles:
            projectile.move()

        # Check for collisions between projectiles and enemies
        for enemy in enemies[:]:
            for projectile in projectiles[:]:
                if enemy.x < projectile.x < enemy.x + ENEMY_SIZE and \
                   enemy.y < projectile.y < enemy.y + ENEMY_SIZE:
                    enemies.remove(enemy)
                    projectiles.remove(projectile)
                    score += 1

        # Check if player hit an enemy
        for enemy in enemies:
            if enemy.x < player.x < enemy.x + ENEMY_SIZE and \
               enemy.y < player.y < enemy.y + ENEMY_SIZE:
                game_over = True

        # Draw player, enemies, and projectiles
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)

        pygame.display.flip()
        clock.tick(30)  # Set FPS

    print(f"Game over! Your final score is: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()
