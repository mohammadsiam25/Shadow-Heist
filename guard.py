
import pygame

from settings import TILE_SIZE
from pathfinding import find_path
from vision import can_see_player


class Guard:

    def __init__(self, x, y):

        self.size = 26
        self.speed = 2
        
        self.path_goal = None
        self.move_target = None
        
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

        # Recalculate path when goal changes
        if target != self.path_goal:
            self.path = find_path(
                self.get_grid_position(),
                target
            )

            self.path_goal = target
            self.move_target = None

        if not self.path:
            return

        # Remove current tile from path
        if len(self.path) > 1 and self.move_target is None:
            self.path.pop(0)

        remaining_distance = self.speed

        # Allow movement across multiple tiles in one update
        while self.path and remaining_distance > 0:

            row, col = self.path[0]

            target_x = col * TILE_SIZE + TILE_SIZE // 2
            target_y = row * TILE_SIZE + TILE_SIZE // 2

            destination = pygame.Vector2(target_x, target_y)
            current = pygame.Vector2(self.rect.center)

            direction = destination - current
            distance = direction.length()

            if distance == 0:
                self.path.pop(0)
                self.move_target = None
                continue

            self.facing = direction.normalize()

            if distance <= remaining_distance:

                self.rect.center = (target_x, target_y)

                remaining_distance -= distance

                self.path.pop(0)
                self.move_target = None

            else:

                direction.scale_to_length(remaining_distance)

                current += direction

                self.rect.center = (
                    round(current.x),
                    round(current.y)
                )

                remaining_distance = 0


    
    def update(self, player):

        visible = can_see_player(self, player)

        # Player detected
        if visible:
            if self.state != "CHASE":
                self.path = []
                self.path_goal = None

            self.state = "CHASE"

            self.last_seen = (
                player.rect.centery // TILE_SIZE,
                player.rect.centerx // TILE_SIZE
            )

            self.search_timer = 0

        # PATROL
        if self.state == "PATROL":

            target = self.patrol_points[self.patrol_index]

            self.move_to(target)

            target_x = target[1] * TILE_SIZE + TILE_SIZE // 2
            target_y = target[0] * TILE_SIZE + TILE_SIZE // 2

            if self.rect.center == (target_x, target_y):

                self.patrol_index = (
                    self.patrol_index + 1
                ) % len(self.patrol_points)

                self.path = []
                self.path_goal = None
                self.move_target = None

        # CHASE
        elif self.state == "CHASE":

            if visible and self.last_seen:
                self.move_to(self.last_seen)

            else:
                self.state = "SEARCH"
                self.search_timer = 0

                self.path = []
                self.path_goal = None
                self.move_target = None

        # SEARCH
        elif self.state == "SEARCH":

            self.search_timer += 1

            if self.last_seen:
                self.move_to(self.last_seen)

            if self.search_timer >= self.search_duration:

                self.state = "RETURN"

                self.path = []
                self.path_goal = None
                self.move_target = None

        # RETURN
        elif self.state == "RETURN":

            target = self.patrol_points[0]

            self.move_to(target)

            target_x = target[1] * TILE_SIZE + TILE_SIZE // 2
            target_y = target[0] * TILE_SIZE + TILE_SIZE // 2

            if self.rect.center == (target_x, target_y):

                self.state = "PATROL"
                self.patrol_index = 0

                self.path = []
                self.path_goal = None
                self.move_target = None

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
