#HoloShalo_Snake game

import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


snake = [(0, 0)]
snake_direction = (1, 0)


food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))


score = 0


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


font = pygame.font.Font(None, 36)


def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def reset_game():
    global snake, snake_direction, food, score
    snake = [(0, 0)]
    snake_direction = (1, 0)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0


START = 0
PLAYING = 1
END = 2
game_state = START


clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == START or game_state == END:
                reset_game()
                game_state = PLAYING
            elif game_state == PLAYING:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)

    if game_state == PLAYING:
        
        x, y = snake[0]
        x += snake_direction[0]
        y += snake_direction[1]

        
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT or (x, y) in snake[1:]:
            game_state = END

        
        if (x, y) == food:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            score += 1
        else:
            snake.pop()

        
        snake.insert(0, (x, y))

        
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, WHITE, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        
        draw_text(f"Score: {score}", WHITE, 10, 10)

    elif game_state == START:
        
        screen.fill(BLACK)
        draw_text("Snake Game", WHITE, WIDTH // 4, HEIGHT // 4)
        draw_text("Press any key to start", WHITE, WIDTH // 4, HEIGHT // 2)

    elif game_state == END:
        
        screen.fill(BLACK)
        draw_text("Game Over", WHITE, WIDTH // 4, HEIGHT // 4)
        draw_text(f"Your Score: {score}", WHITE, WIDTH // 4, HEIGHT // 2)
        draw_text("Press any key to try again", WHITE, WIDTH // 4, HEIGHT // 1.5)

    
    pygame.display.flip()

    
    clock.tick(12 + score) 
