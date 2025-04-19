city_map = [
    ['R', '.', '.', 'T', '.', '.', 'C'],
    ['.', 'T', '.', 'T', '.', 'T', '.'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['T', '.', 'T', 'T', '.', 'T', '.'],
    ['.', '.', '.', '.', '.', '.', '.']
]

import heapq, time

ROWS, COLS = len(city_map), len(city_map[0])

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_position(grid, symbol):
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i][j] == symbol:
                return (i, j)
    return None

def neighbors(pos):
    i, j = pos
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < ROWS and 0 <= nj < COLS and city_map[ni][nj] != 'T':
            yield (ni, nj)

def a_star(start, goal):
    frontier = [(manhattan(start, goal), 0, start, [start])]
    visited = set()
    nodes_visited = 0

    while frontier:
        f, g, current, path = heapq.heappop(frontier)
        nodes_visited += 1

        if current == goal:
            return path, nodes_visited

        if current in visited:
            continue
        visited.add(current)

        for neighbor in neighbors(current):
            if neighbor not in visited:
                new_g = g + 1
                h = manhattan(neighbor, goal)
                heapq.heappush(frontier, (new_g + h, new_g, neighbor, path + [neighbor]))

    return None, nodes_visited

def gbfs(start, goal):
    frontier = [(manhattan(start, goal), start, [start])]
    visited = set()
    nodes_visited = 0

    while frontier:
        h, current, path = heapq.heappop(frontier)
        nodes_visited += 1

        if current == goal:
            return path, nodes_visited

        if current in visited:
            continue
        visited.add(current)

        for neighbor in neighbors(current):
            if neighbor not in visited:
                heapq.heappush(frontier, (manhattan(neighbor, goal), neighbor, path + [neighbor]))

    return None, nodes_visited

def print_path(grid, path):
    new_grid = [row.copy() for row in grid]
    for r, c in path:
        if new_grid[r][c] == '.':
            new_grid[r][c] = '*'
    for row in new_grid:
        print(' '.join(row))

start = find_position(city_map, 'R')
goal = find_position(city_map, 'C')

# GBFS
start_time = time.time()
gbfs_path, gbfs_nodes = gbfs(start, goal)
gbfs_time = (time.time() - start_time) * 1000

# A*
start_time = time.time()
astar_path, astar_nodes = a_star(start, goal)
astar_time = (time.time() - start_time) * 1000

# Output
print("=== GBFS Result ===")
print_path(city_map, gbfs_path)
print(f"Visited Nodes: {gbfs_nodes}, Time: {gbfs_time:.3f} ms\n")

print("=== A* Result ===")
print_path(city_map, astar_path)
print(f"Visited Nodes: {astar_nodes}, Time: {astar_time:.3f} ms\n")

print("=== Comparison Summary ===")
print(f"A* {'lebih cepat' if astar_time < gbfs_time else 'lebih lambat'} dan {'lebih efisien' if astar_nodes < gbfs_nodes else 'kurang efisien'} dibandingkan GBFS.")
