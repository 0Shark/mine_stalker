import pygame
import random

# Constants
WIDTH, HEIGHT = 13, 16
CELL_SIZE = 40
NUM_BOMBS = 8

# Colors
WHITE = (128, 128, 128)
RED = (128, 128, 128)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CURRENT_BLOCK_COLOR = (255, 0, 0)  # Red for the current block

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
pygame.display.set_caption('Mined-Out')

# Function to initialize the grid with bombs
def initialize_grid():
    grid = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    bomb_positions = random.sample(range(WIDTH * HEIGHT), NUM_BOMBS)

    for position in bomb_positions:
        row = position // WIDTH
        col = position % WIDTH
        grid[row][col] = 'B'

    return grid

# Function to calculate the adjacent mines count for each cell
def calculate_adjacent_mines(grid, row, col):
    directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]
    count = 0

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < HEIGHT and 0 <= new_col < WIDTH and grid[new_row][new_col] == 'B':
            count += 1

    return count

# Function to display the grid
# Function to display the grid
def display_grid(grid, player_row, player_col, visited):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            color = WHITE
            if cell == 'B':
                pygame.draw.circle(screen, WHITE, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
            elif visited[i][j]:
                color = BLUE
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the player
    if not visited[player_row][player_col]:
        pygame.draw.circle(screen, CURRENT_BLOCK_COLOR, (player_col * CELL_SIZE + CELL_SIZE // 2, player_row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


# Main game loop
grid = initialize_grid()
player_row, player_col = HEIGHT - 1, WIDTH // 2
visited = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_col > 0:
                player_col -= 1
            elif event.key == pygame.K_RIGHT and player_col < WIDTH - 1:
                player_col += 1
            elif event.key == pygame.K_UP and player_row > 0:
                player_row -= 1
            elif event.key == pygame.K_DOWN and player_row < HEIGHT - 1:
                player_row += 1

    # Check for bomb detection
    if grid[player_row][player_col] == 'B':
        print("Game Over! You hit a bomb.")
        running = False

    # Mark the visited block
    visited[player_row][player_col] = True

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the grid and player
    display_grid(grid, player_row, player_col, visited)

    # Display adjacent mines count at the player's position
    mines_count = calculate_adjacent_mines(grid, player_row, player_col)
    font = pygame.font.Font(None, 36)
    text = font.render(f"{mines_count} Mines", True, YELLOW)
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Check if the player reached the top row in the middle if odd number of columns
    if player_row == 0 and player_col == WIDTH // 2:
        print("Congratulations! You reached the top row in the middle.")
        running = False

    # Add a delay for visibility
    pygame.time.delay(500)

# Quit Pygame
pygame.quit()
