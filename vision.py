
import math
import pygame

from settings import TILE_SIZE
from map import GAME_MAP


VISION_RANGE = 220
VISION_ANGLE = 90


def can_see_player(guard, player):

    start = pygame.Vector2(guard.rect.center)
    end = pygame.Vector2(player.rect.center)

    direction = end - start
    distance = direction.length()

    if distance > VISION_RANGE or distance == 0:
        return False

    direction.normalize_ip()

    facing = guard.facing.normalize()

    dot = max(-1.0, min(1.0, facing.dot(direction)))
    angle = math.degrees(math.acos(dot))

    if angle > VISION_ANGLE / 2:
        return False

    # Line-of-sight raycast
    steps = max(int(distance), 1)

    for i in range(1, steps):

        point = start + direction * (i / steps)

        col = int(point.x // TILE_SIZE)
        row = int(point.y // TILE_SIZE)

        if (
            row < 0
            or row >= len(GAME_MAP)
            or col < 0
            or col >= len(GAME_MAP[0])
        ):
            return False

        if GAME_MAP[row][col] == "1":
            return False

    return True


def draw_vision_cone(screen, guard):

    center = pygame.Vector2(guard.rect.center)
    facing = guard.facing

    if facing.length() == 0:
        facing = pygame.Vector2(1, 0)

    facing = facing.normalize()

    base_angle = math.atan2(facing.y, facing.x)
    half_angle = math.radians(VISION_ANGLE / 2)

    cone_surface = pygame.Surface(
        screen.get_size(),
        pygame.SRCALPHA
    )

    points = [center]

    # Cast rays across the cone
    ray_count = 90

    for i in range(ray_count + 1):

        angle = (
            base_angle - half_angle
            + (2 * half_angle) * i / ray_count
        )

        direction = pygame.Vector2(
            math.cos(angle),
            math.sin(angle)
        )

        endpoint = center + direction * VISION_RANGE

        # Raycast: stop at first wall
        for distance in range(1, VISION_RANGE, 3):

            point = center + direction * distance

            col = int(point.x // TILE_SIZE)
            row = int(point.y // TILE_SIZE)

            if (
                row < 0
                or row >= len(GAME_MAP)
                or col < 0
                or col >= len(GAME_MAP[0])
            ):
                endpoint = point
                break

            if GAME_MAP[row][col] == "1":

                endpoint = point
                break

        points.append(endpoint)

    # Draw vision cone
    pygame.draw.polygon(
        cone_surface,
        (255, 35, 35, 65),
        points
    )

    pygame.draw.polygon(
        cone_surface,
        (255, 50, 50, 120),
        points,
        2
    )

    # Remove cone overlay from wall tiles
    for row_index, row in enumerate(GAME_MAP):

        for col_index, tile in enumerate(row):

            if tile == "1":

                wall_rect = pygame.Rect(
                    col_index * TILE_SIZE,
                    row_index * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                pygame.draw.rect(
                    cone_surface,
                    (0, 0, 0, 0),
                    wall_rect
                )

    screen.blit(cone_surface, (0, 0))
