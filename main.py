import pygame
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
