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


def draw_grid():
    # Рисуем сетку на заднем фоне
    for x in range(0, screen_size, cell_size):
        for y in range(0, screen_size, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect, 1)


# Функции для каждого из уровней
# Обновляем функции уровней, чтобы они включали доступные фрукты
def level_1():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = []  # Нет препятствий на уровне 1
    current_fruit_img = random.choice(fruit_images_by_level[1])


def level_2():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = [{'x': 5, 'y': 5}, {'x': 8, 'y': 8}]  # Пример координат препятствий на уровне 2
    current_fruit_img = random.choice(fruit_images_by_level[2])


def level_3():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = [{'x': 3, 'y': 3}, {'x': 6, 'y': 6}, {'x': 9, 'y': 9}]  # Пример координат препятствий на уровне 3
    current_fruit_img = random.choice(fruit_images_by_level[3])


def level_4():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = [{'x': 2, 'y': 2}, {'x': 5, 'y': 5}, {'x': 8, 'y': 8},
                 {'x': 11, 'y': 11}]  # Пример координат препятствий на уровне 4
    current_fruit_img = random.choice(fruit_images_by_level[4])


def level_5():
    global snake_speed, obstacles, current_fruit_img
    snake_speed = 10
    obstacles = [
        {'x': 1, 'y': 1}, {'x': 3, 'y': 3}, {'x': 5, 'y': 5}, {'x': 7, 'y': 7},
        {'x': 9, 'y': 9}, {'x': 11, 'y': 11}, {'x': 13, 'y': 13}
    ]  # Пример координат препятствий на уровне 5
    current_fruit_img = random.choice(fruit_images_by_level[5])


# Функция для отображения экрана "Главное меню"
def main_menu():
    # Очищаем экран и устанавливаем цвет фона
    screen.fill(SAND_COLOR)
    # Создаем объект шрифта для текста
    font = pygame.font.SysFont(None, 36)
    # Создаем текст "Главное меню"
    title_text = font.render('Главное меню', True, BLACK)
    # Создаем текст "Начать игру" для кнопки "Начать игру"
    start_text = font.render('Начать игру', True, BLACK)
    # Создаем текст "Выход" для кнопки "Выход"
    exit_text = font.render('Выход', True, BLACK)

    # Получаем прямоугольники, в которых будет отображаться текст
    title_rect = title_text.get_rect(center=(screen_size / 2, 100))
    start_rect = start_text.get_rect(center=(screen_size / 2, 200))
    exit_rect = exit_text.get_rect(center=(screen_size / 2, 250))

    # Отображаем текст на экране
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(exit_text, exit_rect)

    # Обработка событий мыши
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если произошло нажатие мыши
            if start_rect.collidepoint(pygame.mouse.get_pos()):
                global game_state
                game_state = LEVEL_SELECTION  # Переходим в экран выбора уровня
            elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()  # Завершаем игру


def level_selection():
    try:
        screen.fill(SAND_COLOR)
        font = pygame.font.SysFont(None, 36)

        level_texts = []
        for i in range(1, 6):
            level_text = font.render(f'Уровень {i}', True, BLACK)
            level_rect = level_text.get_rect(center=(screen_size / 2, 100 + i * 50))
            level_texts.append((level_text, level_rect))
            screen.blit(level_text, level_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (_, rect) in enumerate(level_texts):
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        global game_state
                        current_level = i + 1  # Установка текущего уровня
                        game_state = GAME_PLAYING
                        # Вызов функции для настройки выбранного уровня
                        if current_level == 1:
                            level_1()
                        elif current_level == 2:
                            level_2()
                        elif current_level == 3:
                            level_3()
                        elif current_level == 4:
                            level_4()
                        elif current_level == 5:
                            level_5()
    except Exception as e:
        print(f"Ошибка в функции level_selection: {e}")
        raise


def game_playing():
    try:
        global game_state, score, snake, fruit, special_fruit_counter, special_fruit_active, change_direction, obstacles

        # Обработка событий клавиш
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and change_direction != "DOWN":
                    change_direction = "UP"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and change_direction != "UP":
                    change_direction = "DOWN"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and change_direction != "RIGHT":
                    change_direction = "LEFT"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and change_direction != "LEFT":
                    change_direction = "RIGHT"
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Отрисовка фона
        screen.fill(SAND_COLOR)
        draw_grid()  # Рисуем сетку

        # Отрисовка препятствий
        for obstacle in obstacles:
            screen.blit(wall_block_img, (obstacle['x'] * cell_size, obstacle['y'] * cell_size))

        # Обновление координат головы змеи
        if change_direction == "UP":
            snake[0]["y"] -= cell_size
        elif change_direction == "DOWN":
            snake[0]["y"] += cell_size
        elif change_direction == "LEFT":
            snake[0]["x"] -= cell_size
        elif change_direction == "RIGHT":
            snake[0]["x"] += cell_size

        # Проверка столкновения с границами экрана
        if snake[0]["x"] >= screen_size:
            snake[0]["x"] = 0
        elif snake[0]["x"] < 0:
            snake[0]["x"] = screen_size - cell_size
        if snake[0]["y"] >= screen_size:
            snake[0]["y"] = 0
        elif snake[0]["y"] < 0:
            snake[0]["y"] = screen_size - cell_size

        # Проверка столкновения с самой собой
        for segment in snake[1:]:
            if segment["x"] == snake[0]["x"] and segment["y"] == snake[0]["y"]:
                game_state = GAME_OVER

        # Проверка поедания фрукта
        if snake[0]["x"] == fruit["x"] and snake[0]["y"] == fruit["y"]:
            score += 10
            special_fruit_counter += 1
            snake.append({"x": -1, "y": -1})
            fruit = {"x": random.randrange(1, screen_size // cell_size) * cell_size,
                     "y": random.randrange(1, screen_size // cell_size) * cell_size}
            # Воспроизведение звука при съедании фрукта
            eat_sound.play()

        # Обновление координат тела змеи
        for i in range(len(snake) - 1, 0, -1):
            snake[i]["x"] = snake[i - 1]["x"]
            snake[i]["y"] = snake[i - 1]["y"]

        # Рисуем голову змеи
        if len(snake) > 0:
            head_position = (snake[0]['x'], snake[0]['y'])
            screen.blit(snake_head_img, head_position)

        # Рисуем тело змеи
        for segment in snake[1:]:
            screen.blit(snake_body_img, (segment['x'], segment['y']))

        # Рисуем фрукт
        screen.blit(current_fruit_img, (fruit["x"], fruit["y"]))

        # Проверка столкновений с препятствиями
        for obstacle in obstacles:
            if snake[0]['x'] == obstacle['x'] * cell_size and snake[0]['y'] == obstacle['y'] * cell_size:
                game_state = GAME_OVER

        # Обновление и отображение счета
        update_score()

        # Обновление экрана
        pygame.display.flip()
    except Exception as e:
        print(f"Ошибка в функции game_playing: {e}")
        raise


# Функция для обновления счета
def update_score():
    # Установка шрифта для отображения счета
    font = pygame.font.SysFont(None, 36)
    # Создание текста для отображения
    score_text = font.render(f'Очки: {score}', True, BLACK)
    # Размещение текста на экране
    screen.blit(score_text, (10, 10))


# Функция для перезагрузки игры
def reset_game():
    global snake, score, fruit, game_state, snake_speed, change_direction, obstacles, special_fruit_active
    # Сброс переменных игры
    score = 0
    snake_speed = 10  # Скорость змейки по умолчанию
    change_direction = "RIGHT"
    special_fruit_active = False
    snake = [{"x": 100, "y": 100}, {"x": 90, "y": 100}, {"x": 80, "y": 100}]
    fruit = {"x": random.randrange(1, screen_size // cell_size) * cell_size,
             "y": random.randrange(1, screen_size // cell_size) * cell_size}
    obstacles = []  # Сброс препятствий
    game_state = GAME_PLAYING  # Начать игру заново


# Функция для отображения экрана "Игра окончена"
def game_over():
    # Очищаем экран и устанавливаем цвет фона
    screen.fill(SAND_COLOR)

    # Создаем объект шрифта для текста
    font = pygame.font.SysFont(None, 36)

    # Создаем текст "Игра окончена. Очки:" с текущим счетом
    game_over_text = font.render(f'Игра окончена. Очки: {score}', True, BLACK)

    # Создаем текст "Играть снова" для кнопки "Играть снова"
    retry_text = font.render('Играть снова', True, BLACK)

    # Создаем текст "Выйти в меню" для кнопки "Выйти в меню"
    menu_text = font.render('Выйти в меню', True, BLACK)

    # Получаем прямоугольники, в которых будет отображаться текст
    game_over_rect = game_over_text.get_rect(center=(screen_size / 2, 100))
    retry_rect = retry_text.get_rect(center=(screen_size / 2, 200))
    menu_rect = menu_text.get_rect(center=(screen_size / 2, 250))

    # Отображаем текст на экране
    screen.blit(game_over_text, game_over_rect)
    screen.blit(retry_text, retry_rect)
    screen.blit(menu_text, menu_rect)

    # Обработка событий мыши
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если произошло нажатие мыши
            if retry_rect.collidepoint(pygame.mouse.get_pos()):
                reset_game()  # Сбрасываем игру для начала новой игры
            elif menu_rect.collidepoint(pygame.mouse.get_pos()):
                global game_state
                game_state = MAIN_MENU  # Возвращаемся в главное меню


# Главный игровой цикл
while True:
    clock.tick(snake_speed)

    if game_state == MAIN_MENU:
        main_menu()
    elif game_state == LEVEL_SELECTION:
        level_selection()
    elif game_state == GAME_PLAYING:
        game_playing()
    elif game_state == GAME_OVER:
        game_over()
    pygame.display.flip()

pygame.quit()
