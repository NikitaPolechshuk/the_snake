from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
BOARD_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Общий класс для игровых объектов."""

    def __init__(self, position=BOARD_CENTER,
                 body_color=BOARD_BACKGROUND_COLOR
                 ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка."""
        pass


class Apple(GameObject):
    """Класс для Яблока."""

    body_color = APPLE_COLOR

    def randomize_position(self):
        """Генерация рандомной позиции для Яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def __init__(self):
        self.randomize_position()
        super().__init__(self.position, self.body_color)

    def draw(self):
        """Отрисовка."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для Змеи."""

    def reset(self):
        """Сброс Змейки."""
        self.positions = [BOARD_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = False

    def __init__(self, position=BOARD_CENTER, body_color=SNAKE_COLOR):
        self.reset()
        super().__init__(position, body_color)

    def get_head_position(self):
        """Получение координат головы змейки."""
        return (self.positions[0][0], self.positions[0][1])

    def move(self):
        """Двигаем змейку на следующую клетку"""
        NewHeadX = self.positions[0][0] + self.direction[0] * GRID_SIZE
        NewHeadY = self.positions[0][1] + self.direction[1] * GRID_SIZE
        NewHeadPosition = (NewHeadX % SCREEN_WIDTH, NewHeadY % SCREEN_HEIGHT)
        self.positions.insert(0, NewHeadPosition)
        self.last = self.positions.pop()

    def draw(self):
        """Отрисовка."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновление позиции."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Обработка собыйтий в игре."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main."""
    # Инициализация PyGame:
    pygame.init()

    # Создаем экземпляры классов.
    Snake_Object = Snake()
    Apple_Object = Apple()

    while True:
        # Задержка
        clock.tick(SPEED)
        # Считываем нажатие клавиатуры
        handle_keys(Snake_Object)
        # Обновляем и двигаем змейку
        Snake_Object.update_direction()
        Snake_Object.move()
        # Проверка столкновения голосы с Яблоком и с своим телом
        HeadPosition = Snake_Object.get_head_position()
        if HeadPosition == Apple_Object.position:
            while True:
                Apple_Object.randomize_position()
                if Apple_Object.position not in Snake_Object.positions:
                    break
            Snake_Object.positions.append(Snake_Object.last)
        elif HeadPosition in Snake_Object.positions[1:]:
            Snake_Object.reset()
            Apple_Object.randomize_position()
            rect = (pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        # Отрисовка
        Apple_Object.draw()
        Snake_Object.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
