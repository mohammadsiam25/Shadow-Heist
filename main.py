
import pygame
import sys

from settings import FPS, BACKGROUND, TILE_SIZE
from map import draw_map, GAME_MAP
from player import Player
from guard import Guard
from vision import draw_vision_cone

pygame.init()

# Calculate game dimensions
WIDTH = len(GAME_MAP[0]) * TILE_SIZE
MAP_HEIGHT = len(GAME_MAP) * TILE_SIZE
HUD_HEIGHT = 48
HEIGHT = MAP_HEIGHT + HUD_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHADOW HEIST")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 32)
menu_font = pygame.font.Font(None, 38)
small_font = pygame.font.Font(None, 25)

# Game states
PLAYING = "PLAYING"
PAUSED = "PAUSED"
WON = "WON"
FAILED = "FAILED"

game_state = PLAYING


# -----------------------------
# BUTTON SYSTEM
# -----------------------------

def draw_button(text, rect, mouse_pos, color=(50, 60, 85)):

    hover = rect.collidepoint(mouse_pos)

    if hover:
        color = (80, 100, 145)

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        (180, 190, 220),
        rect,
        2,
        border_radius=8
    )

    text_surface = menu_font.render(
        text,
        True,
        (255, 255, 255)
    )

    screen.blit(
        text_surface,
        text_surface.get_rect(center=rect.center)
    )


# -----------------------------
# BUTTON POSITIONS
# -----------------------------

pause_button = pygame.Rect(
    WIDTH - 130,
    MAP_HEIGHT + 8,
    115,
    32
)

button_width = 220
button_height = 48
button_gap = 15

center_x = WIDTH // 2
center_y = MAP_HEIGHT // 2

resume_button = pygame.Rect(
    center_x - button_width // 2,
    center_y - 30,
    button_width,
    button_height
)

restart_button = pygame.Rect(
    center_x - button_width // 2,
    center_y + 30,
    button_width,
    button_height
)

quit_button = pygame.Rect(
    center_x - button_width // 2,
    center_y + 30 + button_height + button_gap,
    button_width,
    button_height
)


# -----------------------------
# RESET GAME
# -----------------------------

def reset_game():

    global player
    global guard
    global objective
    global exit_rect
    global has_objective
    global game_state

    player = Player(48, 48)

    guard = Guard(650, 80)

    objective = pygame.Rect(
        21 * TILE_SIZE,
        5 * TILE_SIZE,
        20,
        20
    )

    exit_rect = pygame.Rect(
        21 * TILE_SIZE,
        9 * TILE_SIZE,
        30,
        30
    )

    has_objective = False

    game_state = PLAYING


reset_game()


# -----------------------------
# MAIN GAME LOOP
# -----------------------------

running = True

while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if game_state == PLAYING:
                    game_state = PAUSED

                elif game_state == PAUSED:
                    game_state = PLAYING

        # Mouse controls
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # Pause button
                if (
                    game_state == PLAYING
                    and pause_button.collidepoint(event.pos)
                ):
                    game_state = PAUSED

                # Pause menu
                elif game_state == PAUSED:

                    if resume_button.collidepoint(event.pos):
                        game_state = PLAYING

                    elif restart_button.collidepoint(event.pos):
                        reset_game()

                    elif quit_button.collidepoint(event.pos):
                        running = False

                # Victory / failure menu
                elif game_state in (WON, FAILED):

                    if restart_button.collidepoint(event.pos):
                        reset_game()

                    elif quit_button.collidepoint(event.pos):
                        running = False

    # -----------------------------
    # GAME UPDATE
    # -----------------------------

    if game_state == PLAYING:

        player.update()
        guard.update(player)

        # Collect objective
        if player.rect.colliderect(objective):

            has_objective = True

        # Exit
        if player.rect.colliderect(exit_rect):

            if has_objective:
                game_state = WON

        # Guard catches player
        if player.rect.colliderect(guard.rect):

            game_state = FAILED

    # -----------------------------
    # DRAW GAME
    # -----------------------------

    screen.fill(BACKGROUND)

    draw_map(screen)

    # Guard vision cone
    draw_vision_cone(screen, guard)

    # Characters
    player.draw(screen)
    guard.draw(screen)

    # Objective
    if not has_objective:

        pygame.draw.rect(
            screen,
            (255, 220, 50),
            objective
        )

    # Exit
    pygame.draw.rect(
        screen,
        (40, 220, 100),
        exit_rect
    )

    # -----------------------------
    # HUD
    # -----------------------------

    pygame.draw.rect(
        screen,
        (12, 15, 25),
        (0, MAP_HEIGHT, WIDTH, HUD_HEIGHT)
    )

    pygame.draw.line(
        screen,
        (65, 75, 100),
        (0, MAP_HEIGHT),
        (WIDTH, MAP_HEIGHT),
        2
    )

    status = (
        "Objective: COLLECTED"
        if has_objective
        else "Objective: NOT COLLECTED"
    )

    status_text = small_font.render(
        status,
        True,
        (50, 255, 120) if has_objective
        else (255, 220, 50)
    )

    screen.blit(
        status_text,
        (15, MAP_HEIGHT + 12)
    )

    # Pause button
    if game_state == PLAYING:

        draw_button(
            "PAUSE",
            pause_button,
            mouse_pos
        )

    # -----------------------------
    # PAUSE MENU
    # -----------------------------

    if game_state == PAUSED:

        overlay = pygame.Surface(
            (WIDTH, MAP_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((5, 8, 18, 220))

        screen.blit(overlay, (0, 0))

        title = menu_font.render(
            "GAME PAUSED",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title,
            title.get_rect(
                center=(center_x, center_y - 100)
            )
        )

        draw_button(
            "RESUME",
            resume_button,
            mouse_pos
        )

        draw_button(
            "RESTART",
            restart_button,
            mouse_pos
        )

        draw_button(
            "QUIT",
            quit_button,
            mouse_pos
        )

    # -----------------------------
    # GAME OVER MENU
    # -----------------------------

    elif game_state in (WON, FAILED):

        overlay = pygame.Surface(
            (WIDTH, MAP_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((5, 8, 18, 230))

        screen.blit(overlay, (0, 0))

        if game_state == WON:

            title_text = "MISSION COMPLETE!"
            title_color = (50, 255, 120)

        else:

            title_text = "MISSION FAILED!"
            title_color = (255, 70, 70)

        title = menu_font.render(
            title_text,
            True,
            title_color
        )

        screen.blit(
            title,
            title.get_rect(
                center=(center_x, center_y - 100)
            )
        )

        draw_button(
            "RESTART",
            restart_button,
            mouse_pos
        )

        draw_button(
            "QUIT",
            quit_button,
            mouse_pos
        )

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()
sys.exit()
