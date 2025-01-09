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

# Правила поворота змейки:
TURN_RULES = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

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

    def __init__(self,
                 position=BOARD_CENTER,
                 body_color=BOARD_BACKGROUND_COLOR
                 ):
        self.position = position
        self.body_color = body_color

    def cell_draw(self, cell_position):
        """Метод для отрисовки одной ячейки."""
        rect = pygame.Rect(cell_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовка."""


class Apple(GameObject):
    """Класс для Яблока."""

    def randomize_position(self):
        """Генерация рандомной позиции для Яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def __init__(self):
        self.randomize_position()
        self.body_color = APPLE_COLOR
        super().__init__(self.position, self.body_color)

    def draw(self):
        """Отрисовка."""
        self.cell_draw(self.position)


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
        return self.positions[0]

    def move(self):
        """Двигаем змейку на следующую клетку."""
        head_x, head_y = self.get_head_position()
        new_head_x = head_x + self.direction[0] * GRID_SIZE
        new_head_y = head_y + self.direction[1] * GRID_SIZE
        new_head_pos = (new_head_x % SCREEN_WIDTH, new_head_y % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_pos)
        self.last = self.positions.pop()

    def draw(self):
        """Отрисовка."""
        for position in self.positions[:-1]:
            self.cell_draw(position)

        # Отрисовка головы змейки
        self.cell_draw(self.get_head_position())

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
    """Обработка событий в игре."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            new_direction = TURN_RULES.get((event.key, game_object.direction))
            if new_direction is not None:
                game_object.next_direction = new_direction


def main():
    """Main."""
    # Инициализация PyGame:
    pygame.init()

    # Создаем экземпляры классов.
    snake_object = Snake()
    apple_object = Apple()

    while True:
        # Задержка
        clock.tick(SPEED)
        # Считываем нажатие клавиатуры
        handle_keys(snake_object)
        # Обновляем и двигаем змейку
        snake_object.update_direction()
        snake_object.move()
        # Проверка столкновения головы с Яблоком и с своим телом
        HeadPosition = snake_object.get_head_position()
        if HeadPosition == apple_object.position:
            while True:
                apple_object.randomize_position()
                if apple_object.position not in snake_object.positions:
                    break
            snake_object.positions.append(snake_object.last)
        elif HeadPosition in snake_object.positions[3:]:
            snake_object.reset()
            apple_object.randomize_position()
            rect = (pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        # Отрисовка
        apple_object.draw()
        snake_object.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
