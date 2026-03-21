import pygame
import random
import sys

from pygame import Rect, draw, font, MOUSEBUTTONDOWN

pygame.init()

WIDTH = 600
HEIGHT = 400
CELL = 20

MENU_BACKGROUND_IMAGE = "sarpe-1.png"
GAME_BACKGROUND_IMAGE = "fon.png"
current_food_skin = "RED"


game_bg = pygame.image.load(GAME_BACKGROUND_IMAGE)
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))
menu_bg = pygame.image.load(MENU_BACKGROUND_IMAGE)
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
food_img = pygame.image.load("food.png")
food_img = pygame.transform.scale(food_img, (CELL, CELL))
gold_food_img = pygame.image.load("golden.png")
gold_food_img = pygame.transform.scale(gold_food_img, (CELL, CELL))
snake_head = pygame.image.load("head.png")
snake_head = pygame.transform.scale(snake_head, (CELL, CELL))
snake_body = pygame.image.load("snake.telo.png")
snake_body = pygame.transform.scale(snake_body, (CELL, CELL))
snake_tail = pygame.image.load("snake.tail.png")
snake_tail = pygame.transform.scale(snake_tail, (CELL, CELL))

def game_over_screen(score, best, screen_width, screen_height):
    # draw background
    game_bg_scaled = pygame.transform.scale(game_bg, (screen_width, screen_height))
    screen.blit(game_bg_scaled, (0, 0))

    font_big = pygame.font.SysFont("Comic Sans MS", 50)
    font_small = pygame.font.SysFont("Comic Sans MS", 30)

    # надписи на английском
    text1 = font_big.render("Game Over!", True, (255, 0, 0))
    text2 = font_small.render(f"Best Score: {best}", True, (0, 255, 0))

    # позиционирование по центру
    text1_x = screen_width // 2 - text1.get_width() // 2
    text1_y = screen_height // 2 - 60
    text2_x = screen_width // 2 - text2.get_width() // 2
    text2_y = screen_height // 2 + 10

    screen.blit(text1, (text1_x, text1_y))
    screen.blit(text2, (text2_x, text2_y))

    pygame.display.update()
    pygame.time.delay(3000)  # pause 3 seconds

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake PRO")

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (120, 120, 120)

font_big = pygame.font.SysFont("Comic Sans MS", 40)

# ===== SCORE SETTINGS =====
apples_eaten = 0
invulnerable_until = 0
best_score = 0
show_best_score = True
music_enabled = True

# ===== BUTTON CLASS =====
class Button:
    def __init__(self, x, y, width, height, color, text, text_color=(255, 255, 255)):
        self.base_rect = Rect(x, y, width, height)
        self.rect = self.base_rect.copy()
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font.Font(None, 28)

    def draw(self):
        if self.is_hover():
            self.rect = self.base_rect.inflate(10, 6)
        else:
            self.rect = self.base_rect.copy()

        draw.rect(screen, self.color, self.rect, border_radius=10)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

    def is_hover(self):
        return self.base_rect.collidepoint(pygame.mouse.get_pos())


# ===== SETTINGS VARIABLES =====
control_mode = "ARROWS"

modifier_double_food = False
modifier_swap_tail = False

FIELD_MODES = {
    "SMALL": (400, 300),
    "MEDIUM": (600, 400),
    "LARGE": (800, 600)
}

field_mode = "MEDIUM"


# ===== CONTROLS =====
def handle_controls(event, direction):
    global control_mode

    if event.type == pygame.KEYDOWN:

        if control_mode == "ARROWS":
            if event.key == pygame.K_UP and direction != "DOWN":
                return "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                return "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                return "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                return "RIGHT"

        if control_mode == "WASD":
            if event.key == pygame.K_w and direction != "DOWN":
                return "UP"
            if event.key == pygame.K_s and direction != "UP":
                return "DOWN"
            if event.key == pygame.K_a and direction != "RIGHT":
                return "LEFT"
            if event.key == pygame.K_d and direction != "LEFT":
                return "RIGHT"

    return direction


# ===== SETTINGS MENU =====
def settings():
    global music_enabled
    global control_mode, show_best_score, music_enabled
    global control_mode, show_best_score

    left_x = 120
    right_x = 340

    row1_y = 150
    row2_y = 220

    arrows_btn = Button(left_x, row1_y, 180, 50, GRAY, "ARROWS")
    wasd_btn = Button(right_x, row1_y, 180, 50, GRAY, "WASD")

    score_btn = Button(left_x, row2_y, 180, 50, GRAY, "BEST SCORE")
    music_btn = Button(340, 220, 180, 50, GRAY, "MUSIC")

    back_btn = Button(200, 320, 200, 50, GRAY, "BACK")

    while True:
        screen.blit(menu_bg, (0, 0))

        title = font_big.render("Controls", True, GREEN)
        screen.blit(title, (WIDTH // 2 - 110, 60))

        for event in pygame.event.get():
            music_btn.color = GREEN if music_enabled else RED
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if music_btn.is_clicked(event):
                music_enabled = not music_enabled

            if arrows_btn.is_clicked(event):
                control_mode = "ARROWS"

            if wasd_btn.is_clicked(event):
                control_mode = "WASD"

            if score_btn.is_clicked(event):
                show_best_score = not show_best_score

            if back_btn.is_clicked(event):
                return



        arrows_btn.color = GREEN if control_mode == "ARROWS" else GRAY
        wasd_btn.color = GREEN if control_mode == "WASD" else GRAY
        score_btn.color = GREEN if show_best_score else GRAY

        for btn in [arrows_btn, wasd_btn, score_btn, music_btn, back_btn]:
            btn.draw()

        pygame.display.update()


# ===== CUSTOM SETTINGS MENU =====
def custom_settings_menu():
    global modifier_double_food, modifier_swap_tail, field_mode

    double_btn = Button(150, 120, 300, 50, GRAY, "2x Apples")
    swap_btn = Button(150, 180, 300, 50, GRAY, "Swap Head-Tail")

    small_btn = Button(150, 260, 100, 40, GRAY, "Small")
    medium_btn = Button(260, 260, 100, 40, GRAY, "Medium")
    large_btn = Button(370, 260, 100, 40, GRAY, "Large")

    back_btn = Button(200, 340, 200, 50, GRAY, "START GAME")

    while True:
        screen.blit(menu_bg, (0, 0))

        title = font_big.render("Custom Game", True, GREEN)
        screen.blit(title, (WIDTH // 2 - 140, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if double_btn.is_clicked(event):
                modifier_double_food = not modifier_double_food

            if swap_btn.is_clicked(event):
                modifier_swap_tail = not modifier_swap_tail

            if small_btn.is_clicked(event):
                field_mode = "SMALL"

            if medium_btn.is_clicked(event):
                field_mode = "MEDIUM"

            if large_btn.is_clicked(event):
                field_mode = "LARGE"

            if back_btn.is_clicked(event):
                custom_game()
                return

        double_btn.color = GREEN if modifier_double_food else GRAY
        swap_btn.color = GREEN if modifier_swap_tail else GRAY

        small_btn.color = GREEN if field_mode == "SMALL" else GRAY
        medium_btn.color = GREEN if field_mode == "MEDIUM" else GRAY
        large_btn.color = GREEN if field_mode == "LARGE" else GRAY

        for btn in [double_btn, swap_btn,
                    small_btn, medium_btn, large_btn, back_btn]:
            btn.draw()

        pygame.display.update()


# ===== CLASSIC GAME =====
def classic_game():
    global screen, apples_eaten, best_score

    pygame.display.set_mode((WIDTH, HEIGHT))

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"

    apples_eaten = 0

    food = (random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL))

    while True:
        game_bg_scaled = pygame.transform.scale(
            game_bg,
            (WIDTH - WIDTH % CELL, HEIGHT - HEIGHT % CELL)
        )
        screen.blit(game_bg_scaled, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                break

            direction = handle_controls(event, direction)

        head_x, head_y = snake[0]

        if direction == "UP": head_y -= CELL
        if direction == "DOWN": head_y += CELL
        if direction == "LEFT": head_x -= CELL
        if direction == "RIGHT": head_x += CELL

        new_head = (head_x, head_y)

        if (head_x < 0 or head_x >= WIDTH or
                head_y < 0 or head_y >= HEIGHT or
                new_head in snake):
            game_over_screen(apples_eaten, best_score, WIDTH, HEIGHT)
            break
        snake.insert(0, new_head)

        if new_head == food:
            apples_eaten += 1
            best_score = max(best_score, apples_eaten)

            food = (random.randrange(0, WIDTH, CELL),
                    random.randrange(0, HEIGHT, CELL))
        else:
            snake.pop()

        for i, segment in enumerate(snake):

            for i, segment in enumerate(snake):
                for i, segment in enumerate(snake):
                    x, y = segment

        for i, segment in enumerate(snake):
            x, y = segment

        for i, segment in enumerate(snake):
            x, y = segment

        for i, segment in enumerate(snake):
            x, y = segment

        for i, segment in enumerate(snake):
            x, y = segment

            # ===== ГОЛОВА =====
            if i == 0:
                if direction == "UP":
                    img = snake_head
                elif direction == "DOWN":
                    img = pygame.transform.rotate(snake_head, 180)
                elif direction == "LEFT":
                    img = pygame.transform.rotate(snake_head, 90)
                elif direction == "RIGHT":
                    img = pygame.transform.rotate(snake_head, -90)
                screen.blit(img, (x, y))

            # ===== ХВОСТ =====
            elif i == len(snake) - 1:
                prev_x, prev_y = snake[i - 1]

                dx = prev_x - x
                dy = prev_y - y

                # Центрируем хвост по сегменту
                tail_rect = snake_tail.get_rect()
                tail_rect.topleft = (x, y)

                if dx > 0:
                    tail_img = pygame.transform.rotate(snake_tail, 0)
                elif dx < 0:
                    tail_img = pygame.transform.rotate(snake_tail, 180)
                elif dy > 0:
                    tail_img = pygame.transform.rotate(snake_tail, -90)
                elif dy < 0:
                    tail_img = pygame.transform.rotate(snake_tail, 90)


                screen.blit(tail_img, (x, y))

            # ===== ТЕЛО =====
            else:
                prev_x, prev_y = snake[i - 1]
                next_x, next_y = snake[i + 1]

                if prev_y == next_y:
                    body_img = pygame.transform.rotate(snake_body, 0)
                elif prev_x == next_x:
                    body_img = pygame.transform.rotate(snake_body, 90)
                else:  # углы
                    if (prev_x < x and next_y < y) or (next_x < x and prev_y < y):
                        body_img = pygame.transform.rotate(snake_body, 0)
                    elif (prev_x < x and next_y > y) or (next_x < x and prev_y > y):
                        body_img = pygame.transform.rotate(snake_body, 270)
                    elif (prev_x > x and next_y < y) or (next_x > x and prev_y < y):
                        body_img = pygame.transform.rotate(snake_body, 90)
                    else:
                        body_img = pygame.transform.rotate(snake_body, 180)

                screen.blit(body_img, (x, y))

        if food:
            if current_food_skin == "RED":
                screen.blit(food_img, food)
            else:  # GOLD
                screen.blit(gold_food_img, food)

        score_text = font.Font(None, 30).render(
            f"Score: {apples_eaten}", True, GREEN)
        screen.blit(score_text, (10, 10))

        if show_best_score:
            best_text = font.Font(None, 30).render(
                f"Best: {best_score}", True, GREEN)
            screen.blit(best_text, (10, 40))

        pygame.display.update()
        clock.tick(10)

    pygame.display.set_mode((WIDTH, HEIGHT))


# ===== CUSTOM GAME =====
def custom_game():
    global modifier_double_food, modifier_swap_tail, field_mode, screen
    global apples_eaten, best_score

    game_width, game_height = FIELD_MODES[field_mode]

    screen = pygame.display.set_mode((game_width, game_height))

    game_bg_scaled = pygame.transform.scale(game_bg, (game_width, game_height))

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"

    apples_eaten = 0

    speed = 8

    food = (random.randrange(0, game_width, CELL),
            random.randrange(0, game_height, CELL))

    food2 = None
    if modifier_double_food:
        food2 = (random.randrange(0, game_width, CELL),
                 random.randrange(0, game_height, CELL))

    while True:
        game_bg_scaled = pygame.transform.scale(
            game_bg,
            (game_width - game_width % CELL, game_height - game_height % CELL)
        )
        screen.blit(game_bg_scaled, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.set_mode((WIDTH, HEIGHT))
                return

            direction = handle_controls(event, direction)

        # ===== HEAD MOVEMENT =====
        head_x, head_y = snake[0]

        if direction == "UP": head_y -= CELL
        if direction == "DOWN": head_y += CELL
        if direction == "LEFT": head_x -= CELL
        if direction == "RIGHT": head_x += CELL

        new_head = (head_x, head_y)

        # ===== DEATH CHECK =====
        if (head_x < 0 or head_x >= game_width or
                head_y < 0 or head_y >= game_height or
                new_head in snake):
            game_over_screen(apples_eaten, best_score, game_width, game_height)
            break
        snake.insert(0, new_head)

        # ===== FOOD COLLISION =====
        if new_head == food or (food2 and new_head == food2):

            # Swap modifier → управление от хвоста
            if modifier_swap_tail and len(snake) > 2:
                snake.reverse()

                if direction == "UP": direction = "DOWN"
                elif direction == "DOWN": direction = "UP"
                elif direction == "LEFT": direction = "RIGHT"
                elif direction == "RIGHT": direction = "LEFT"

            apples_eaten += 1
            best_score = max(best_score, apples_eaten)

            if modifier_double_food:
                food = (random.randrange(0, game_width, CELL),
                        random.randrange(0, game_height, CELL))

                food2 = (random.randrange(0, game_width, CELL),
                         random.randrange(0, game_height, CELL))
            else:
                food = (random.randrange(0, game_width, CELL),
                        random.randrange(0, game_height, CELL))

            speed += 0.3
        else:
            snake.pop()

        # ===== DRAW =====
        for i, segment in enumerate(snake):
            x, y = segment

            # ===== ГОЛОВА =====
            if i == 0:
                if direction == "UP":
                    img = snake_head
                elif direction == "DOWN":
                    img = pygame.transform.rotate(snake_head, 180)
                elif direction == "LEFT":
                    img = pygame.transform.rotate(snake_head, 90)
                elif direction == "RIGHT":
                    img = pygame.transform.rotate(snake_head, -90)
                screen.blit(img, (x, y))

            # ===== ХВОСТ =====
            elif i == len(snake) - 1:
                prev_x, prev_y = snake[i - 1]

                dx = prev_x - x
                dy = prev_y - y

                if prev_x == x:  # вертикально
                    if prev_y > y:
                        tail_img = pygame.transform.rotate(snake_tail, -90)
                    else:
                        tail_img = pygame.transform.rotate(snake_tail, 90)
                else:  # горизонтально
                    if prev_x > x:
                        tail_img = pygame.transform.rotate(snake_tail, 0)
                    else:
                        tail_img = pygame.transform.rotate(snake_tail, 180)

                screen.blit(tail_img, (x, y))

            # ===== ТЕЛО =====
            else:
                prev_x, prev_y = snake[i - 1]
                next_x, next_y = snake[i + 1]

                if prev_y == next_y:
                    body_img = pygame.transform.rotate(snake_body, 0)
                elif prev_x == next_x:
                    body_img = pygame.transform.rotate(snake_body, 90)
                else:
                    if (prev_x < x and next_y < y) or (next_x < x and prev_y < y):
                        body_img = pygame.transform.rotate(snake_body, 0)
                    elif (prev_x < x and next_y > y) or (next_x < x and prev_y > y):
                        body_img = pygame.transform.rotate(snake_body, 270)
                    elif (prev_x > x and next_y < y) or (next_x > x and prev_y < y):
                        body_img = pygame.transform.rotate(snake_body, 90)
                    else:
                        body_img = pygame.transform.rotate(snake_body, 180)

                screen.blit(body_img, (x, y))
        # Отрисовка первого яблока
        if food:
            if current_food_skin == "RED":
                screen.blit(food_img, food)
            else:  # GOLD
                screen.blit(gold_food_img, food)

        # Отрисовка второго яблока
        if food2:
            if current_food_skin == "RED":
                screen.blit(food_img, food2)
            else:  # GOLD
                screen.blit(gold_food_img, food2)

        score_text = font.Font(None, 30).render(
            f"Score: {apples_eaten}", True, GREEN)
        screen.blit(score_text, (10, 10))

        if show_best_score:
            best_text = font.Font(None, 30).render(
                f"Best: {best_score}", True, GREEN)
            screen.blit(best_text, (10, 40))

        pygame.display.update()
        clock.tick(speed)

    pygame.display.set_mode((WIDTH, HEIGHT))

def skins_menu():
    global current_food_skin

    red_btn = Button(200, 150, 200, 50, GRAY, "Red Apple")
    gold_btn = Button(200, 220, 200, 50, GRAY, "Gold Apple")
    back_btn = Button(200, 290, 200, 50, GRAY, "BACK")

    # маленькие иконки рядом с кнопками
    red_icon = pygame.transform.scale(food_img, (30, 30))
    gold_icon = pygame.transform.scale(gold_food_img, (30, 30))

    while True:
        screen.blit(menu_bg, (0, 0))

        title = font_big.render("SKINS", True, GREEN)
        screen.blit(title, (WIDTH // 2 - 80, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if red_btn.is_clicked(event):
                current_food_skin = "RED"

            if gold_btn.is_clicked(event):
                current_food_skin = "GOLD"

            if back_btn.is_clicked(event):
                return

        # подсветка выбранной кнопки
        red_btn.color = GREEN if current_food_skin == "RED" else GRAY
        gold_btn.color = GREEN if current_food_skin == "GOLD" else GRAY

        # отрисовка кнопок
        for btn in [red_btn, gold_btn, back_btn]:
            btn.draw()

        # отрисовка иконок рядом с кнопками
        screen.blit(red_icon, (red_btn.base_rect.x - 40, red_btn.base_rect.y + 10))
        screen.blit(gold_icon, (gold_btn.base_rect.x - 40, gold_btn.base_rect.y + 10))

        pygame.display.update()

# ===== MODE SELECT =====
def choose_mode():
    classic_btn = Button(200, 150, 200, 50, GRAY, "Classic Game")
    custom_btn = Button(200, 220, 200, 50, GRAY, "Custom Game")
    back_btn = Button(200, 290, 200, 50, GRAY, "BACK")

    while True:
        screen.blit(menu_bg, (0, 0))

        title = font_big.render("Choose Mode", True, GREEN)
        screen.blit(title, (WIDTH // 2 - 140, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if classic_btn.is_clicked(event):
                classic_game()

            if custom_btn.is_clicked(event):
                custom_settings_menu()

            if back_btn.is_clicked(event):
                return

        for btn in [classic_btn, custom_btn, back_btn]:
            btn.color = GREEN if btn.is_hover() else GRAY
            btn.draw()

        pygame.display.update()


# ===== MAIN MENU =====
# ===== MAIN MENU =====
# ===== MAIN MENU =====
def menu():
    # Кнопки
    play_btn = Button(110, 120, 200, 50, GRAY, "PLAY")      # выше
    skins_btn = Button(110, 190, 200, 50, GRAY, "SKINS")    # под PLAY
    settings_btn = Button(110, 260, 200, 50, GRAY, "SETTINGS")
    exit_btn = Button(110, 330, 200, 50, GRAY, "EXIT")

    while True:
        screen.blit(menu_bg, (0, 0))

        # Надпись SNAKE PRO поднята выше
        title = font_big.render("SNAKE PRO", True, GREEN)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play_btn.is_clicked(event):
                choose_mode()

            if skins_btn.is_clicked(event):
                skins_menu()

            if settings_btn.is_clicked(event):
                settings()

            if exit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()

        # Подсветка кнопок при наведении
        for btn in [play_btn, skins_btn, settings_btn, exit_btn]:
            btn.color = GREEN if btn.is_hover() else GRAY
            btn.draw()

        pygame.display.update()


menu()