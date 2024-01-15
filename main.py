import pygame

pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Инициализация экрана
screen_size = 400
cell_size = 20
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Snake Game")


# Инициализация змеи
snake = [{"x": 100, "y": 100}, {"x": 90, "y": 100}, {"x": 80, "y": 100}]
snake_direction = "RIGHT"
change_direction = snake_direction
snake_speed = 15


pygame.display.flip()
