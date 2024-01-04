from z3 import *
import random

ROWS = 16
COLS = 13
rows, cols = ROWS, COLS

# Z3 variables
P = [[Bool(f'P_{i}_{j}') for j in range(cols)] for i in range(rows)]
M = [[Bool(f'M_{i}_{j}') for j in range(cols)] for i in range(rows)]

#initial and goal positions
initial_position_i, initial_position_j = 15, 6
goal_position_i, goal_position_j = 0, 6

constraints = []

# Each cell must be part of the path or contain a mine, but not both
for i in range(rows):
    for j in range(cols):
        constraints.append(Xor(P[i][j], M[i][j]))

# Randomly assign mines
for i in range(rows):
    for j in range(cols):
        # Probability of a cell containing a mine
        mine_probability = 0.2
        # Add a constraint to include a mine in the cell with the specified probability
        constraints.append(Implies(M[i][j], random.uniform(0, 1) < mine_probability))

# Initial position constraint
constraints.append(P[initial_position_i][initial_position_j])

# Goal position constraint
constraints.append(P[goal_position_i][goal_position_j])

# Checking manhattan distance between current position and goal position so we we know if we are close to the goal
for i in range(rows):
    for j in range(cols):
        manhattan_distance = abs(i - goal_position_i) + abs(j - goal_position_j)
        constraints.append(Implies(P[i][j], manhattan_distance == 1))  # Manhattan distance is 1 for valid moves

# Connectivity constraints
for i in range(rows):
    for j in range(cols):
        neighbors = [(i + dx, j + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if 0 <= i + dx < rows and 0 <= j + dy < cols]
        valid_neighbors = [P[x][y] for x, y in neighbors if is_true(P[x][y])]
        constraints.append(Implies(P[i][j], Or(*valid_neighbors)))

# Mine density constraints
for i in range(rows):
    for j in range(cols):
        mine_density = Sum([If(M[i + dx][j + dy], 1, 0) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if 0 <= i + dx < rows and 0 <= j + dy < cols]) / 9
        constraints.append(Implies(P[i][j], mine_density <= 0.5))  # Mine density should be <= 0.5 for valid moves

# Objective
objective = And(constraints)

# Z3 solver
solver = Solver()
solver.add(objective)

# Check satisfiability
if solver.check() == sat:
    print("SAT")
    model = solver.model()
    print("Path:")
    for i in range(rows):
        for j in range(cols):
            if is_true(model[P[i][j]]):
                print('P', end='')
            elif is_true(model[M[i][j]]):
                print('M', end='')
            else:
                print('.', end='')
        print()
else:
    print("UNSAT")