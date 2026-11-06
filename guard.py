
import pygame

from settings import TILE_SIZE
from pathfinding import find_path
from vision import can_see_player


class Guard:

    def __init__(self, x, y):

        self.size = 26
        self.speed = 2
        
        # Guard facing direction
        self.facing = pygame.Vector2(1, 0)

        self.rect = pygame.Rect(
            x, y, self.size, self.size
        )

        # Align guard with grid
        col = self.rect.centerx // TILE_SIZE
        row = self.rect.centery // TILE_SIZE

        self.rect.center = (
            col * TILE_SIZE + TILE_SIZE // 2,
            row * TILE_SIZE + TILE_SIZE // 2
        )

        # FSM states
        self.state = "PATROL"

        self.path = []
        self.path_timer = 0

        # Patrol route: (row, col)
        self.patrol_points = [
            (2, 16),   # Start
            (2, 20),   # Move Right
            (7, 20),   # Move Down
            (7, 16),   # Move Left
        ]

        self.patrol_index = 0

        # Last known player position
        self.last_seen = None

        # Search timer
        self.search_timer = 0
        self.search_duration = 180

    def get_grid_position(self):

        row = self.rect.centery // TILE_SIZE
        col = self.rect.centerx // TILE_SIZE

        return (row, col)

    def move_to(self, target):

        self.path_timer += 1

        if self.path_timer >= 20 or not self.path:

            self.path_timer = 0

            self.path = find_path(
                self.get_grid_position(),
                target
            )

        if len(self.path) > 1:

            row, col = self.path[1]

            target_x = col * TILE_SIZE + TILE_SIZE // 2
            target_y = row * TILE_SIZE + TILE_SIZE // 2

            current = pygame.Vector2(self.rect.center)
            destination = pygame.Vector2(target_x, target_y)

            direction = destination - current
            distance = direction.length()

            if distance > 0:
                self.facing = direction.normalize()

            if distance <= self.speed:

                self.rect.center = (target_x, target_y)
                self.path.pop(0)

            elif distance > 0:

                direction.normalize_ip()
                current += direction * self.speed

                self.rect.center = (
                    round(current.x),
                    round(current.y)
                )

    def update(self, player):

        # Vision system
        if can_see_player(self, player):

            self.state = "CHASE"

            self.last_seen = (
                player.rect.centery // TILE_SIZE,
                player.rect.centerx // TILE_SIZE
            )

            self.search_timer = 0

        # FSM
        if self.state == "PATROL":

            target = self.patrol_points[self.patrol_index]

            self.move_to(target)

            if self.get_grid_position() == target:

                self.patrol_index = (
                    self.patrol_index + 1
                ) % len(self.patrol_points)

                self.path = []

        elif self.state == "CHASE":

            if self.last_seen:
                self.move_to(self.last_seen)

            # Player lost
            if not can_see_player(self, player):

                self.state = "SEARCH"
                self.search_timer = 0
                self.path = []

        elif self.state == "SEARCH":

            self.search_timer += 1

            if self.last_seen:
                self.move_to(self.last_seen)

            if self.search_timer >= self.search_duration:

                self.state = "RETURN"
                self.path = []

        elif self.state == "RETURN":

            target = self.patrol_points[0]

            self.move_to(target)

            if self.get_grid_position() == target:

                self.state = "PATROL"
                self.patrol_index = 0
                self.path = []

    def draw(self, screen):

        x = self.rect.x
        y = self.rect.y

        # Shadow
        pygame.draw.rect(
            screen, (10, 10, 15),
            (x + 2, y + 21, 23, 5)
        )

        # Boots
        pygame.draw.rect(
            screen, (25, 25, 30),
            (x + 3, y + 19, 8, 5)
        )

        pygame.draw.rect(
            screen, (25, 25, 30),
            (x + 15, y + 19, 8, 5)
        )

        # Armor
        pygame.draw.rect(
            screen, (90, 25, 35),
            (x + 3, y + 9, 21, 12)
        )

        # Armor highlight
        pygame.draw.rect(
            screen, (145, 40, 50),
            (x + 5, y + 10, 16, 3)
        )

        # Helmet
        pygame.draw.rect(
            screen, (45, 48, 60),
            (x + 4, y + 2, 19, 10)
        )

        pygame.draw.rect(
            screen, (90, 95, 110),
            (x + 6, y + 1, 15, 3)
        )

        # Face mask
        pygame.draw.rect(
            screen, (20, 20, 25),
            (x + 7, y + 7, 13, 4)
        )

        # Eyes
        pygame.draw.rect(
            screen, (255, 60, 60),
            (x + 8, y + 8, 3, 2)
        )

        pygame.draw.rect(
            screen, (255, 60, 60),
            (x + 16, y + 8, 3, 2)
        )

        # AI State label
        font = pygame.font.Font(None, 18)

        text = font.render(
            self.state,
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (x - 8, y - 18)
        )
