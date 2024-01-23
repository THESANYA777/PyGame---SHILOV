import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

clock = pygame.time.Clock()

# Определение цветов и параметров
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND_COLOR = (194, 178, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen_size = 400
cell_size = 20
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Snake Game")

# Константы состояний игры
MAIN_MENU, LEVEL_SELECTION, GAME_PLAYING, GAME_OVER = range(4)

# Текущее состояние и переменные игры
game_state = MAIN_MENU
score = 0
special_fruit_counter = 0
special_fruit_active = False
special_fruit = {"x": 0, "y": 0}
obstacles = []  # Добавить препятствия для уровней
snake = [{"x": 100, "y": 100}, {"x": 90, "y": 100}, {"x": 80, "y": 100}]
snake_speed = 15  # Скорость змейки
change_direction = "RIGHT"
fruit = {"x": random.randrange(1, screen_size // cell_size) * cell_size,
         "y": random.randrange(1, screen_size // cell_size) * cell_size}


# Функции для каждого из уровней
def level_1():
    global snake_speed, obstacles
    snake_speed = 75
    obstacles = []


def level_2():
    global snake_speed, obstacles
    snake_speed = 3
    obstacles = [{'x': 100, 'y': 200}, {'x': 200, 'y': 200}]


def level_3():
    global snake_speed, obstacles
    snake_speed = 3  # Та же скорость, что и на уровне 2
    # Больше препятствий
    obstacles = [{'x': 100, 'y': 200}, {'x': 200, 'y': 200}, {'x': 300, 'y': 100}]


def level_4():
    global snake_speed, obstacles
    snake_speed = 5  # Еще более высокая скорость
    obstacles = []  # Нет препятствий


def level_5():
    global snake_speed, obstacles, special_fruit_active
    snake_speed = 10
    obstacles = [{'x': 50, 'y': 100}, {'x': 150, 'y': 300}, {'x': 250, 'y': 150}]
    special_fruit_active = True  # Активация специальных фруктов на этом уровне


def main_menu():
    screen.fill(SAND_COLOR)
    font = pygame.font.SysFont(None, 36)
    title_text = font.render('Главное меню', True, BLACK)
    start_text = font.render('Начать игру', True, BLACK)
    exit_text = font.render('Выход', True, BLACK)

    title_rect = title_text.get_rect(center=(screen_size / 2, 100))
    start_rect = start_text.get_rect(center=(screen_size / 2, 200))
    exit_rect = exit_text.get_rect(center=(screen_size / 2, 250))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(exit_text, exit_rect)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(pygame.mouse.get_pos()):
                global game_state
                game_state = LEVEL_SELECTION
            elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()
