import pygame

from settings import TILE_SIZE
from map import GAME_MAP


class Player:

    def __init__(self, x, y):

        self.size = 24

        self.rect = pygame.Rect(
            x,
            y,
            self.size,
            self.size
        )

        self.speed = 3

    def move(self, dx, dy):

        # Horizontal movement
        self.rect.x += dx
        self.check_collision("horizontal")

        # Vertical movement
        self.rect.y += dy
        self.check_collision("vertical")

    def check_collision(self, direction):

        for row_index, row in enumerate(GAME_MAP):

            for col_index, tile in enumerate(row):

                if tile == "1":

                    wall = pygame.Rect(
                        col_index * TILE_SIZE,
                        row_index * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )

                    if self.rect.colliderect(wall):

                        if direction == "horizontal":

                            if self.rect.x < wall.x:
                                self.rect.right = wall.left
                            else:
                                self.rect.left = wall.right

                        elif direction == "vertical":

                            if self.rect.y < wall.y:
                                self.rect.bottom = wall.top
                            else:
                                self.rect.top = wall.bottom

    def update(self):

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed

        self.move(dx, dy)

    def draw(self, screen):

        x = self.rect.x
        y = self.rect.y

        # Shadow
        pygame.draw.rect(
            screen, (10, 10, 15),
            (x + 3, y + 20, 20, 5)
        )

        # Boots
        pygame.draw.rect(
            screen, (20, 22, 30),
            (x + 4, y + 18, 6, 5)
        )

        pygame.draw.rect(
            screen, (20, 22, 30),
            (x + 15, y + 18, 6, 5)
        )

        # Body
        pygame.draw.rect(
            screen, (35, 45, 75),
            (x + 4, y + 9, 17, 11)
        )

        # Hood
        pygame.draw.rect(
            screen, (20, 28, 50),
            (x + 5, y + 2, 15, 10)
        )

        pygame.draw.rect(
            screen, (55, 70, 110),
            (x + 7, y + 1, 11, 3)
        )

        # Face
        pygame.draw.rect(
            screen, (190, 150, 115),
            (x + 9, y + 6, 8, 4)
        )

        # Mask
        pygame.draw.rect(
            screen, (15, 20, 30),
            (x + 8, y + 8, 10, 3)
        )

        # Belt
        pygame.draw.rect(
            screen, (180, 170, 100),
            (x + 5, y + 15, 15, 2)
        )