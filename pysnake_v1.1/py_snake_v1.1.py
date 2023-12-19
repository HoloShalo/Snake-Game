import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)  # New color
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # New color

# User's color choices
snake_colors = [PURPLE, ORANGE]
bg_colors = [WHITE, BLACK]  # Set initial background color to white
food_colors = [GREEN, RED]
snake_color_index = 0
bg_color_index = 0
food_color_index = 0

# Snake
snake = [(0, 0)]
snake_direction = (1, 0)

# Food
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Score
score = 0

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Fonts
font = pygame.font.Font(None, 36)

# Function to display text on the screen
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to reset the game
def reset_game():
    global snake, snake_direction, food, score
    snake = [(0, 0)]
    snake_direction = (1, 0)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0

# Game states
START = 0
PLAYING = 1
PAUSED = 2  # New game state for the paused state
END = 3
SETTINGS = 4
game_state = START

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == START or game_state == END:
                if event.key == pygame.K_RETURN:  # Press 'ENTER' to start the game
                    reset_game()
                    game_state = PLAYING
                elif event.key == pygame.K_s:  # Press 's' to open settings
                    game_state = SETTINGS
            elif game_state == PLAYING:
                if event.key == pygame.K_ESCAPE:  # Press 'ESC' to pause the game
                    game_state = PAUSED
                elif event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)
            elif game_state == PAUSED:
                if event.key == pygame.K_RETURN:  # Press 'ENTER' to resume the game
                    game_state = PLAYING
            elif game_state == SETTINGS:
                if event.key == pygame.K_i:
                    # Change snake color
                    snake_color_index = (snake_color_index + 1) % len(snake_colors)
                elif event.key == pygame.K_o:
                    # Change background color
                    bg_color_index = (bg_color_index + 1) % len(bg_colors)
                elif event.key == pygame.K_p:
                    # Change food color
                    food_color_index = (food_color_index + 1) % len(food_colors)
                elif event.key == pygame.K_s:
                    # Save and exit
                    game_state = START

    if game_state == PLAYING:
        # Move snake
        x, y = snake[0]
        x += snake_direction[0]
        y += snake_direction[1]

        # Check for collisions
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT or (x, y) in snake[1:]:
            game_state = END

        # Check if snake eats food
        if (x, y) == food:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            score += 1
        else:
            snake.pop()

        # Update snake
        snake.insert(0, (x, y))

        # Draw everything
        screen.fill(bg_colors[bg_color_index])
        for segment in snake:
            pygame.draw.rect(screen, snake_colors[snake_color_index], (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, food_colors[food_color_index], (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw score
        draw_text(f"Score: {score}", WHITE if bg_colors[bg_color_index] == BLACK else BLACK, 10, 10)

    elif game_state == START:
        # Draw start screen
        screen.fill(bg_colors[bg_color_index])
        draw_text("Snake Game", WHITE if bg_colors[bg_color_index] == BLACK else BLACK, WIDTH // 4, HEIGHT // 4)
        draw_text("Press ENTER to start the game", WHITE if bg_colors[bg_color_index] == BLACK else BLACK, WIDTH // 4, HEIGHT // 2)
        draw_text("Press 's' to open the settings page", WHITE if bg_colors[bg_color_index] == BLACK else BLACK, WIDTH // 4, HEIGHT // 1.5)

    elif game_state == END:
        # Draw end screen
        screen.fill(bg_colors[bg_color_index])
        draw_text("Game Over", WHITE if bg_colors[bg_color_index] == BLACK else BLACK, WIDTH // 4, HEIGHT // 4)
        draw_text(f"Your Score: {score}", WHITE if bg_colors[bg_color_index] == BLACK else BLACK, WIDTH // 4, HEIGHT // 2)
        draw_text("Press ENTER to try again", WHITE if bg_colors[bg_color_index] == BLACK else BLACK, WIDTH // 4, HEIGHT // 1.5)

    elif game_state == PAUSED:
        # Draw pause screen
        screen.fill(bg_colors[bg_color_index])
        draw_text("Game Paused", WHITE if bg_colors[bg_color_index] == BLACK else BLACK, WIDTH // 4, HEIGHT // 4)
        draw_text("Press ENTER to resume", WHITE if bg_colors[bg_color_index] == BLACK else BLACK, WIDTH // 4, HEIGHT // 2)

    elif game_state == SETTINGS:
        # Draw settings page
        screen.fill(WHITE)
        draw_text("Settings", BLACK, WIDTH // 4, HEIGHT // 4)
        draw_text("Press 'i' to change snake color", BLACK, WIDTH // 4, HEIGHT // 2)
        draw_text("Press 'o' to change background color", BLACK, WIDTH // 4, HEIGHT // 1.5)
        draw_text("Press 'p' to change food color", BLACK, WIDTH // 4, HEIGHT // 1.25)
        draw_text("Press 's' to save and exit", BLACK, WIDTH // 4, HEIGHT)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(12 + score)  # Increase speed as the score goes up
