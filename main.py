import pygame
import sys
import random

# Инициализация Pygame
pygame.init()
# Инициализация звуков Pygame
pygame.mixer.init()

clock = pygame.time.Clock()

# Определение цветов и параметров
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND_COLOR = (194, 178, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen_size = 400
# Определение размера клетки
cell_size = 20
current_level = 1  # Уровень по умолчанию
# Проверка существования файлов с изображениями и звуком
try:
    # Загрузка изображений для игры
    # Голова змеи
    snake_head_img = pygame.image.load('snake_yellow_head.png')
    # Тело змеи
    snake_body_img = pygame.image.load('snake_yellow_blob.png')
    # Яблоки
    apple_green_img = pygame.image.load('apple_green.png')
    apple_red_img = pygame.image.load('apple_red.png')  # Может потребоваться изменение размера
    # Стена (препятствие)
    wall_block_img = pygame.image.load('wall_block.png')
    # Звук съедания фрукта
    eat_sound = pygame.mixer.Sound('fruit_eat_sound.wav')
except pygame.error as e:
    print(f"Ошибка при загрузке ресурсов: {e}")
    sys.exit()

# Запасные значения
# Определение цветов и параметров
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# SAND_COLOR = (194, 178, 128)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
# BLUE = (0, 0, 255)
# screen_size = 400

# Переводим все в размер одной клетки карты
snake_head_img = pygame.transform.scale(snake_head_img, (cell_size, cell_size))
snake_body_img = pygame.transform.scale(snake_body_img, (cell_size, cell_size))
apple_green_img = pygame.transform.scale(apple_green_img, (cell_size, cell_size))
apple_red_img = pygame.transform.scale(apple_red_img, (cell_size, cell_size))
wall_block_img = pygame.transform.scale(wall_block_img, (cell_size, cell_size))

# Запасные значения
# Загрузка изображений для игры
# Голова змеи
# snake_head_img = pygame.image.load('snake_yellow_head.png')
# Тело змеи
# snake_body_img = pygame.image.load('snake_yellow_blob.png')
# Яблоки
# apple_green_img = pygame.image.load('apple_green.png')
# apple_red_img = pygame.image.load('apple_red.png')  # Может потребоваться изменение размера
# Стена (препятствие)
# wall_block_img = pygame.image.load('wall_block.png')
# Звук съедания фрукта
# eat_sound = pygame.mixer.Sound('fruit_eat_sound.wav')

# Словарь, который будет хранить изображения фруктов и информацию о доступности на каждом уровне
fruit_images_by_level = {
    1: [apple_green_img],
    2: [apple_green_img, apple_red_img],
    3: [apple_green_img, apple_red_img],
    4: [apple_green_img, apple_red_img],
    5: [apple_green_img, apple_red_img]
}

# Текущее изображение фрукта
current_fruit_img = apple_green_img

# Изменение размера изображений, если необходимо
apple_red_img = pygame.transform.scale(apple_red_img, (cell_size, cell_size))
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
