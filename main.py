import pygame
import sys
from collections import deque
import heapq


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
mode = "BFS"



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

def reset_search():
    if mode == "BFS":
        return bfs_generator(), None
    else:
        return astar_generator(), None


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

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

def astar_generator():
    open_set = []
    heapq.heappush(open_set, (0, start))

    g_score = {start: 0}
    parent = {}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        visited.add(current)

        yield visited, parent, current

        if current == goal:
            break

        row, col = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dr, col + dc
            neighbor = (r, c)

            if 0 <= r < ROWS and 0 <= c < COLS:
                if maze[r][c] == 1:
                    continue

                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float("inf")):
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

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





visited = set()
parent = {}
final_path = []
search_done = False

search_gen, parent = reset_search()
path = []


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "BFS"
                search_gen, parent = reset_search()
                visited = set()
                final_path = []
                search_done = False

            if event.key == pygame.K_a:
                mode = "ASTAR"
                search_gen, parent = reset_search()
                visited = set()
                final_path = []
                search_done = False

    screen.fill((255, 255, 255))

    if not search_done:
        try:
            visited, parent, _ = next(search_gen)
        except StopIteration:
            search_done = True
            final_path = reconstruct_path(parent)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "BFS"
                search_gen, parent = reset_search()
                path = []

            if event.key == pygame.K_a:
                mode = "ASTAR"
                search_gen, parent = reset_search()
                path = []

    draw_grid()
    draw_visited(visited)
    draw_path(final_path)

    pygame.display.update()
    clock.tick(15)
