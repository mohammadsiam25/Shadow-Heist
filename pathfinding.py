
import heapq

from map import GAME_MAP


def heuristic(a, b):
    """Manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(node):

    row, col = node

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    neighbors = []

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if (
            0 <= new_row < len(GAME_MAP)
            and 0 <= new_col < len(GAME_MAP[0])
        ):

            if GAME_MAP[new_row][new_col] == "0":
                neighbors.append((new_row, new_col))

    return neighbors


def find_path(start, goal):

    if start == goal:
        return [start]

    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {}

    g_score = {start: 0}

    f_score = {
        start: heuristic(start, goal)
    }

    while open_list:

        current_f, current = heapq.heappop(open_list)

        if current == goal:

            path = [current]

            while current in came_from:
                current = came_from[current]
                path.append(current)

            path.reverse()

            return path

        for neighbor in get_neighbors(current):

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                f_score[neighbor] = (
                    tentative_g + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_list,
                    (f_score[neighbor], neighbor)
                )

    return []
