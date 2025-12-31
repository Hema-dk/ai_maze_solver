import pygame
import sys
from collections import deque
import heapq
import time

# ---------- INIT ----------
pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS vs A* Maze Solver")

clock = pygame.time.Clock()

# ---------- MAZE ----------
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

# ---------- GLOBAL STATE ----------
mode = "BFS"
visited = set()
parent = {}
final_path = []
search_done = False
nodes_explored = 0
path_length = 0
start_time = None
end_time = None

# ---------- DRAWING ----------
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            color = (255, 255, 255)
            if maze[r][c] == 1:
                color = (0, 0, 0)

            pygame.draw.rect(
                screen,
                color,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen,
                (200, 200, 200),
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1
            )

def draw_visited(visited):
    for r, c in visited:
        pygame.draw.rect(
            screen,
            (173, 216, 230),
            (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

def draw_path(path):
    for r, c in path:
        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

def draw_stats():
    font = pygame.font.SysFont(None, 24)
    elapsed = 0
    if start_time and end_time:
        elapsed = int((end_time - start_time) * 1000)

    text = font.render(
        f"{mode} | Nodes: {nodes_explored} | Path: {path_length} | Time: {elapsed} ms",
        True,
        (0, 0, 0)
    )

    padding = 6
    bg = text.get_rect(topleft=(10, 10))
    bg.inflate_ip(padding * 2, padding * 2)

    pygame.draw.rect(screen, (255, 255, 255), bg)
    pygame.draw.rect(screen, (0, 0, 0), bg, 1)
    screen.blit(text, (10 + padding, 10 + padding))

# ---------- SEARCH ----------
def reset_search():
    global visited, parent, final_path, search_done
    global nodes_explored, path_length, start_time, end_time

    visited = set()
    parent = {}
    final_path = []
    search_done = False
    nodes_explored = 0
    path_length = 0
    start_time = time.time()
    end_time = None

    if mode == "BFS":
        return bfs_generator()
    else:
        return astar_generator()

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

def bfs_generator():
    global nodes_explored

    queue = deque([start])
    visited.add(start)

    while queue:
        current = queue.popleft()
        nodes_explored += 1
        yield current

        if current == goal:
            return

        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if maze[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current
                    queue.append((nr, nc))

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_generator():
    global nodes_explored

    open_set = []
    heapq.heappush(open_set, (0, start))
    g_score = {start: 0}
    visited.clear()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in visited:
            continue

        visited.add(current)
        nodes_explored += 1
        yield current

        if current == goal:
            return

        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0:
                temp_g = g_score[current] + 1
                if temp_g < g_score.get(neighbor, float("inf")):
                    parent[neighbor] = current
                    g_score[neighbor] = temp_g
                    f = temp_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))

# ---------- MAIN LOOP ----------
search_gen = reset_search()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "BFS"
                search_gen = reset_search()
            if event.key == pygame.K_a:
                mode = "ASTAR"
                search_gen = reset_search()

    screen.fill((255, 255, 255))

    if not search_done:
        try:
            next(search_gen)
        except StopIteration:
            search_done = True
            final_path = reconstruct_path(parent)
            path_length = len(final_path)
            end_time = time.time()

    draw_grid()
    draw_visited(visited)
    draw_path(final_path)
    draw_stats()

    pygame.display.update()
    clock.tick(15)
