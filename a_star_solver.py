import matplotlib.pyplot as plt
import heapq
import random
import pygame
import sys

ROWS = 16
COLS = 13
# Constants for visualization
CELL_SIZE = 30
SCREEN_WIDTH = COLS * CELL_SIZE
SCREEN_HEIGHT = ROWS * CELL_SIZE
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

class MineStalker:
    def __init__(self, start, goal, mines):
        self.start = start
        self.goal = goal
        self.mines = set(mines)

    def is_valid_position(self, position, heuristic_func=None):
        x, y = position
        if position in self.mines:
            return False  # Game over if the position contains a mine

        if heuristic_func:
            adjacent_positions = self.get_adjacent_positions(position)
            mine_density = self.get_mine_density(position)
            
            get_heuristic = lambda pos: heuristic_func(pos)
            adjacent_heuristics = [get_heuristic(pos) for pos in adjacent_positions]
            max_heuristic = max(adjacent_heuristics)
            if heuristic_func(position) > max_heuristic:
                return False
            if mine_density > 0.5:
                return False

        return True

    def get_adjacent_positions(self, position):
        x, y = position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        adjacent_positions = [(x + dx, y + dy) for dx, dy in directions]
        return [pos for pos in adjacent_positions if 0 <= pos[0] < ROWS and 0 <= pos[1] < COLS]

    def heuristic_density_based(self, current):
        return abs(current[0] - self.goal[0]) + abs(current[1] - self.goal[1]) + self.get_mine_density(current)
    
    def get_mine_density(self, position):
        x, y = position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        adjacent_positions = [(x + dx, y + dy) for dx, dy in directions]
        adjacent_mines = [pos for pos in adjacent_positions if pos in self.mines]
        return len(adjacent_mines) / len(adjacent_positions)

    def astar_search(self):
        open_set = [(0, self.start)]
        came_from = {}
        g_score = {self.start: 0}

        while open_set:
            current_cost, current_position = heapq.heappop(open_set)

            if current_position == self.goal:
                path = self.reconstruct_path(came_from, current_position)
                return path

            for neighbor in self.get_adjacent_positions(current_position):
                if not self.is_valid_position(neighbor, self.heuristic_density_based):
                    continue  # Skip positions with adjacent mines or high mine density

                tentative_g_score = g_score[current_position] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    priority = tentative_g_score + self.heuristic_density_based(neighbor)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current_position

        return None

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

def draw_game(grid, path):
    plt.figure(figsize=(COLS, ROWS))
    plt.imshow(grid, cmap='gray', origin='lower', interpolation='nearest')

    for i in range(len(path) - 1):
        plt.plot([path[i][1], path[i + 1][1]], [path[i][0], path[i + 1][0]], color='blue', linewidth=2)

    plt.title("Mine Stalker - A* Search")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.show()

def estimate_states_generated(path):
    return len(path)

# Initialize pygame
pygame.init()

class MineStalkerVisualizer:
    def __init__(self, mine_stalker_game):
        self.mine_stalker_game = mine_stalker_game
        self.path_density_based = mine_stalker_game.astar_search()
        self.states_generated_density_based = estimate_states_generated(self.path_density_based)
        

        self.grid = [[1] * COLS for _ in range(ROWS)]
        for mine in mine_stalker_game.mines:
            self.grid[mine[0]][mine[1]] = 0

        self.current_step = 0

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mine Stalker - A* Search")

    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = COLOR_WHITE if self.grid[row][col] == 1 else COLOR_BLACK
                pygame.draw.rect(self.screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_path(self):
        for i in range(len(self.path_density_based) - 1):
            pygame.draw.line(self.screen, COLOR_BLUE,
                             (self.path_density_based[i][1] * CELL_SIZE + CELL_SIZE // 2,
                              self.path_density_based[i][0] * CELL_SIZE + CELL_SIZE // 2),
                             (self.path_density_based[i + 1][1] * CELL_SIZE + CELL_SIZE // 2,
                              self.path_density_based[i + 1][0] * CELL_SIZE + CELL_SIZE // 2), 5)

    def draw_mine(self, mine):
        pygame.draw.rect(self.screen, COLOR_RED,
                         (mine[1] * CELL_SIZE, mine[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def run_visualization(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(COLOR_WHITE)
            self.draw_grid()

            if self.current_step < len(self.path_density_based):
                current_position = self.path_density_based[self.current_step]
                pygame.draw.circle(self.screen, COLOR_BLUE,
                                   (current_position[1] * CELL_SIZE + CELL_SIZE // 2,
                                    current_position[0] * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2)

                for mine in self.mine_stalker_game.mines:
                    self.draw_mine(mine)

                pygame.display.flip()
                self.current_step += 1
                clock.tick(2)  # Adjust the speed of visualization (1 frame per second)
            else:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    start_position = (15, 6)  # Bottom row, middle column
    goal_position = (0, 6)    # Top row, middle column
    # Generate random mines
    mines = []
    mines_count = 20
    for _ in range(mines_count):
        while True:
            mine = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
            if mine != start_position and mine != goal_position and mine not in mines:
                mines.append(mine)
                break
            
    mine_stalker_game = MineStalker(start_position, goal_position, mines)
    visualizer = MineStalkerVisualizer(mine_stalker_game)
    visualizer.run_visualization()
