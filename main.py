import pygame
import sys
from collections import deque

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze BFS Animation")

clock = pygame.time.Clock()

# 0 = empty, 1 = wall
maze = [
    [0,0,0,1,0,0,0,0,0,0],
    [1,1,0,1,0,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,1,0,0,0,0,0],
    [0,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,0,0]
]

start = (0, 0)
goal = (9, 9)

# ---------- DRAW FUNCTIONS ----------

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = (255, 255, 255)
            if maze[row][col] == 1:
                color = (0, 0, 0)

            pygame.draw.rect(
                screen,
                color,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen,
                (200, 200, 200),
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1
            )

def draw_visited(visited):
    for row, col in visited:
        pygame.draw.rect(
            screen,
            (173, 216, 230),  # light blue
            (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

def draw_path(path):
    for row, col in path:
        pygame.draw.rect(
            screen,
            (255, 255, 0),  # yellow
            (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

# ---------- BFS LOGIC ----------

def bfs_generator():
    queue = deque([start])
    visited = set([start])
    parent = {}

    while queue:
        current = queue.popleft()
        yield visited, parent, current

        if current == goal:
            break

        row, col = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if maze[r][c] == 0 and (r, c) not in visited:
                    visited.add((r, c))
                    parent[(r, c)] = current
                    queue.append((r, c))

    return parent

def reconstruct_path(parent):
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return []
    path.append(start)
    return path[::-1]

# ---------- ANIMATION STATE ----------

bfs_steps = bfs_generator()
visited = set()
parent = {}
final_path = []
search_done = False

# ---------- GAME LOOP ----------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))

    if not search_done:
        try:
            visited, parent, _ = next(bfs_steps)
        except StopIteration:
            search_done = True
            final_path = reconstruct_path(parent)

    draw_grid()
    draw_visited(visited)
    draw_path(final_path)

    pygame.display.update()
    clock.tick(15)
