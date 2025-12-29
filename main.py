import pygame
import sys
from collections import deque

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Grid")

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

def bfs():
    queue = deque([start])
    visited = set([start])
    parent = {}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        row, col = current
        neighbors = [
            (row-1, col),
            (row+1, col),
            (row, col-1),
            (row, col+1)
        ]

        for r, c in neighbors:
            if 0 <= r < ROWS and 0 <= c < COLS:
                if maze[r][c] == 0 and (r, c) not in visited:
                    visited.add((r, c))
                    parent[(r, c)] = current
                    queue.append((r, c))

    # reconstruct path
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return []
    path.append(start)
    return path[::-1]

path = bfs()

def draw_path(path):
    for row, col in path:
        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))
    draw_grid()
    draw_path(path)
    pygame.display.update()
    clock.tick(60)
