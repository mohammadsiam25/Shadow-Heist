
import math
import pygame

from settings import TILE_SIZE
from map import GAME_MAP


VISION_RANGE = 220
VISION_ANGLE = 90

RAY_COUNT = 45
RAY_STEP = 4

WALL_COLOR = (255, 35, 35, 65)
EDGE_COLOR = (255, 50, 50, 120)


def can_see_player(guard, player):
    start = pygame.Vector2(guard.rect.center)
    end = pygame.Vector2(player.rect.center)

    direction = end - start
    distance = direction.length()

    if distance > VISION_RANGE or distance == 0:
        return False

    direction.normalize_ip()

    facing = pygame.Vector2(guard.facing)

    if facing.length() == 0:
        facing = pygame.Vector2(1, 0)

    facing.normalize_ip()

    dot = max(-1.0, min(1.0, facing.dot(direction)))
    angle = math.degrees(math.acos(dot))

    if angle > VISION_ANGLE / 2:
        return False

    # Check walls between guard and player
    steps = max(int(distance), 1)

    for i in range(1, steps):
        point = start + direction * i

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
    # Cache cone surface to avoid recreating it every frame
    if not hasattr(guard, "vision_surface"):
        guard.vision_surface = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

    cone_surface = guard.vision_surface
    cone_surface.fill((0, 0, 0, 0))

    center = pygame.Vector2(guard.rect.center)

    facing = pygame.Vector2(guard.facing)

    if facing.length() == 0:
        facing = pygame.Vector2(1, 0)

    facing.normalize_ip()

    base_angle = math.atan2(facing.y, facing.x)
    half_angle = math.radians(VISION_ANGLE / 2)

    points = [center]

    # Cast rays inside the vision angle
    for i in range(RAY_COUNT + 1):
        angle = (
            base_angle
            - half_angle
            + (2 * half_angle) * i / RAY_COUNT
        )

        direction = pygame.Vector2(
            math.cos(angle),
            math.sin(angle)
        )

        endpoint = center + direction * VISION_RANGE

        # Stop ray at the first wall
        for distance in range(1, VISION_RANGE, RAY_STEP):
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

    if len(points) >= 3:
        pygame.draw.polygon(
            cone_surface,
            WALL_COLOR,
            points
        )

        pygame.draw.polygon(
            cone_surface,
            EDGE_COLOR,
            points,
            2
        )

    # Keep vision overlay out of wall tiles
    for row in range(len(GAME_MAP)):
        for col in range(len(GAME_MAP[row])):
            if GAME_MAP[row][col] == "1":
                wall_rect = pygame.Rect(
                    col * TILE_SIZE,
                    row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                cone_surface.fill(
                    (0, 0, 0, 0),
                    wall_rect
                )

    screen.blit(cone_surface, (0, 0))
