
import pygame
import random

from settings import (
    TILE_SIZE,
    FLOOR_COLOR,
    WALL_COLOR,
    COLS,
    ROWS
)

# 0 = Floor
# 1 = Wall

GAME_MAP = [
    "11111111111111111111111",
    "10000000000000000000001",
    "10001110000001110000001",
    "10000000000000000000001",
    "10111000111000111000001",
    "10000000000000000000001",
    "10000011100011100000001",
    "10000000000000000000001",
    "10001110000001110000001",
    "10000000000000000000001",
    "11111111111111111111111",
]


def draw_floor(screen, x, y, tile_size):
    rect = pygame.Rect(x, y, tile_size, tile_size)

    # Dark pixel-art floor
    pygame.draw.rect(screen, (27, 30, 39), rect)

    # Subtle tile variation
    random.seed(x + y * 100)

    for _ in range(4):
        px = x + random.randint(4, tile_size - 8)
        py = y + random.randint(4, tile_size - 8)

        pygame.draw.rect(
            screen,
            (35, 39, 48),
            (px, py, 3, 3)
        )

    # Floor tile border
    pygame.draw.rect(
        screen,
        (20, 23, 30),
        rect,
        1
    )


def draw_wall(screen, x, y, tile_size):
    rect = pygame.Rect(x, y, tile_size, tile_size)

    # Base wall color
    pygame.draw.rect(screen, (45, 49, 61), rect)

    # Top highlight
    pygame.draw.line(
        screen,
        (85, 91, 105),
        (x, y),
        (x + tile_size, y),
        3
    )

    # Wall brick pattern
    pygame.draw.rect(
        screen,
        (58, 63, 77),
        (x + 4, y + 6, tile_size - 8, 12)
    )

    pygame.draw.rect(
        screen,
        (35, 39, 49),
        (x + 4, y + 22, tile_size - 8, 12)
    )

    # Dark border
    pygame.draw.rect(
        screen,
        (20, 23, 30),
        rect,
        2
    )


def draw_map(screen):

    for row_index, row in enumerate(GAME_MAP):

        for col_index, tile in enumerate(row):

            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if tile == "1":
                draw_wall(
                    screen,
                    x,
                    y,
                    TILE_SIZE
                )

            else:
                draw_floor(
                    screen,
                    x,
                    y,
                    TILE_SIZE
                )
