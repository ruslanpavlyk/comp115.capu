# runs by py -3.13 wolf_cathing_eggs.py
import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
FPS = 180

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Eggs")
clock = pygame.time.Clock()

BLACK = (20, 20, 20)
GRAY = (160, 160, 160)
RED = (200, 40, 40)
WHITE = (255, 255, 255)

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 72)

background_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

egg_img = pygame.image.load("egg.png").convert_alpha()
egg_img = pygame.transform.smoothscale(egg_img, (34, 44))

BASKET_W, BASKET_H = 82, 64
basket_img = pygame.image.load("basket.png").convert_alpha()
basket_img = pygame.transform.smoothscale(basket_img, (BASKET_W, BASKET_H))

heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.smoothscale(heart_img, (36, 36))

TOP_WOLF_W, TOP_WOLF_H = 185, 295
BOT_WOLF_W, BOT_WOLF_H = 185, 295

top_wolf_right = pygame.image.load("top_wolf.png").convert_alpha()
top_wolf_right = pygame.transform.smoothscale(top_wolf_right, (TOP_WOLF_W, TOP_WOLF_H))
top_wolf_left = pygame.transform.flip(top_wolf_right, True, False)

bot_wolf_right = pygame.image.load("bot_wolf.png").convert_alpha()
bot_wolf_right = pygame.transform.smoothscale(bot_wolf_right, (BOT_WOLF_W, BOT_WOLF_H))
bot_wolf_left = pygame.transform.flip(bot_wolf_right, True, False)

CHICKEN_W, CHICKEN_H = 84, 84
chicken_right = pygame.image.load("chicken.png").convert_alpha()
chicken_right = pygame.transform.smoothscale(chicken_right, (CHICKEN_W, CHICKEN_H))
chicken_left = pygame.transform.flip(chicken_right, True, False)

wolf_pos = (395, 250)

basket_positions = {
    "UL": (365, 282),
    "UR": (508, 282),
    "LL": (360, 377),
    "LR": (520, 377),
}
basket_position = "UL"

catch_offsets = {
    "UL": (BASKET_W // 2, 28),
    "UR": (BASKET_W // 2, 28),
    "LL": (BASKET_W // 2, 18),
    "LR": (BASKET_W // 2, 18),
}

def get_catch_point(pos_name):
    bx, by = basket_positions[pos_name]
    ox, oy = catch_offsets[pos_name]
    return (bx + ox, by + oy)

chicken_positions = {
    "UL": (125, 165),
    "LL": (125, 260),
    "UR": (791, 165),
    "LR": (791, 260),
}

# Egg lanes
lanes = {
    "UL": [
        (205, 240),
        (255, 252),
        (305, 264),
        (345, 275),
        (380, 284),
        get_catch_point("UL"),
    ],
    "LL": [
        (205, 335),
        (255, 347),
        (305, 359),
        (345, 370),
        (380, 379),
        get_catch_point("LL"),
    ],
    "UR": [
        (795, 240),
        (745, 252),
        (695, 264),
        (655, 275),
        (620, 284),
        get_catch_point("UR"),
    ],
    "LR": [
        (795, 335),
        (745, 347),
        (695, 359),
        (655, 370),
        (620, 379),
        get_catch_point("LR"),
    ],
}

eggs = []
score = 0
lives = 3
game_over = False

spawn_timer = 0
spawn_delay = 850
move_timer = 0
move_delay = 180

def draw_text(text, fnt, color, x, y):
    img = fnt.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global eggs, score, lives, game_over, basket_position
    global spawn_timer, move_timer, spawn_delay, move_delay

    eggs = []
    score = 0
    lives = 3
    game_over = False
    basket_position = "UL"
    spawn_timer = 0
    move_timer = 0
    spawn_delay = 850
    move_delay = 180

def spawn_egg():
    lane = random.choice(list(lanes.keys()))
    eggs.append({"lane": lane, "step": 0})

def update_eggs():
    global eggs, score, lives, game_over, move_delay, spawn_delay

    remaining = []

    for egg in eggs:
        egg["step"] += 1
        lane = egg["lane"]

        if egg["step"] >= len(lanes[lane]):
            if basket_position == lane:
                score += 1
                if move_delay > 90:
                    move_delay -= 2
                if spawn_delay > 350:
                    spawn_delay -= 3
            else:
                lives -= 1
                if lives <= 0:
                    game_over = True
        else:
            remaining.append(egg)

    eggs = remaining

def draw_background():
    screen.blit(background_img, (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 40))
    screen.blit(overlay, (0, 0))

    # Upper
    pygame.draw.line(screen, GRAY, (190, 235), (420, 292), 5)
    pygame.draw.line(screen, GRAY, (810, 235), (580, 292), 5)
    # Lower
    pygame.draw.line(screen, GRAY, (190, 315), (420, 395), 5)
    pygame.draw.line(screen, GRAY, (810, 315), (580, 395), 5)

    screen.blit(chicken_left, chicken_positions["UL"])
    screen.blit(chicken_left, chicken_positions["LL"])
    screen.blit(chicken_right, chicken_positions["UR"])
    screen.blit(chicken_right, chicken_positions["LR"])

def draw_active_wolf_and_basket():
    bx, by = basket_positions[basket_position]

    if basket_position == "UL":
        wolf_img = top_wolf_left
    elif basket_position == "LL":
        wolf_img = bot_wolf_left
    elif basket_position == "UR":
        wolf_img = top_wolf_right
    else:
        wolf_img = bot_wolf_right

    screen.blit(wolf_img, wolf_pos)
    screen.blit(basket_img, (bx, by))

def draw_eggs():
    for egg in eggs:
        lane = egg["lane"]
        step = egg["step"]
        if 0 <= step < len(lanes[lane]):
            x, y = lanes[lane][step]
            screen.blit(egg_img, (x - egg_img.get_width() // 2, y - egg_img.get_height() // 2))

def draw_ui():
    draw_text(f"Score: {score}", font, BLACK, 30, 20)
    draw_text("Lives:", font, RED, 30, 60)

    for i in range(lives):
        screen.blit(heart_img, (120 + i * 42, 58))

def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    title = big_font.render("GAME OVER", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(title, title_rect)

    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_rect)

    restart_text = font.render("Press R to restart or ESC to quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

def handle_input(event):
    global basket_position

    if event.key == pygame.K_q:
        basket_position = "UL"
    elif event.key == pygame.K_a:
        basket_position = "LL"
    elif event.key == pygame.K_o:
        basket_position = "UR"
    elif event.key == pygame.K_l:
        basket_position = "LR"

running = True
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
            else:
                handle_input(event)

    if not game_over:
        spawn_timer += dt
        move_timer += dt

        if spawn_timer >= spawn_delay:
            spawn_timer = 0
            if len(eggs) < 6:
                spawn_egg()

        if move_timer >= move_delay:
            move_timer = 0
            update_eggs()

    draw_background()
    draw_active_wolf_and_basket()
    draw_eggs()
    draw_ui()

    if game_over:
        draw_game_over()

    pygame.display.flip()

pygame.quit()
sys.exit()