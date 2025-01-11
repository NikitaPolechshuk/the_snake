from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480  # заглушка чтобы не ругались тесты
BOARD_WIDTH, BOARD_HEIGHT = 640, 480
BOARD_CENTER = (BOARD_WIDTH // 2, BOARD_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = BOARD_WIDTH // GRID_SIZE
GRID_HEIGHT = BOARD_HEIGHT // GRID_SIZE

# Константы для Экрана с информацией
INFO_BOARD_HEIGHT = 100
INFO_BOARD_FONT_SIZE = 45
INFO_BOARD_FONT_COLOR = (54, 117, 39)
INFO_BOARD_GAME_OVER_FONT_SIZE = 90
INFO_BOARD_GAME_OVER_FONT_COLOR = (29, 215, 222)
INFO_BOARD_BACKGROUND_COLOR = (56, 54, 49)
INFO_BOARD_BORDER1_COLOR = (31, 66, 22)
INFO_BOARD_BORDER2_COLOR = (53, 112, 38)
INFO_BOARD_BORDER_SIZE = 5

# Пути к файлам с картинками
APPLE_IMG = 'Graphics/apple.png'
SNAKE_BODY_IMG = 'Graphics/body.png'
SNAKE_HEAD_IMG = 'Graphics/head.png'
SNAKE_TAIL_IMG = 'Graphics/tail.png'
SNAKE_TURN_IMG = 'Graphics/turn.png'

# Направления движения:
UP = (0, -1,)
LEFT = (-1, 0)
DOWN = (0, 1,)
RIGHT = (1, 0)

# Правила поворота изображений
IMG_TURN = {
    UP: 0,
    LEFT: 90,
    DOWN: 180,
    RIGHT: 270
}

# Правила отрисовки поворотных элементов змейки
# (delta(head, third), direction) -> angle
SNAKE_BODY_TURN_RULES = {
    ((1, -1), (0, -1)): 0,
    ((1, 1), (0, 1)): 90,
    ((-1, 1), (0, 1)): 180,
    ((-1, -1), (0, -1)): 270,

    ((-1, 1), (-1, 0)): 0,
    ((-1, -1), (-1, 0)): 90,
    ((1, -1), (1, 0)): 180,
    ((1, 1), (1, 0)): 270,
    ((1, 1), (-1, 0)): 0,
    ((1, -1), (-1, 0)): 90,
    ((-1, -1), (1, 0)): 180,
    ((-1, 1), (1, 0)): 270,
    ((1, 1), (0, -1)): 0,
    ((1, -1), (0, 1)): 90,
    ((-1, -1), (0, 1)): 180,
    ((-1, 1), (0, -1)): 270,
}

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
SPEED_START = 15

# Коэффициент прибавки скорости за каждое яблоко (+3%)
SPEED_COEFFICIENT = 3

# Настройка игрового окна:
screen = pygame.display.set_mode((BOARD_WIDTH,
                                  BOARD_HEIGHT + INFO_BOARD_HEIGHT),
                                 0,
                                 32)

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

    def draw_rect(self, color, rect, size=0):
        """Отрисовка прямоугольника."""
        pygame.draw.rect(screen, color, rect, size)

    def draw_cell(self, cell_position):
        """Метод для отрисовки одной ячейки."""
        rect = pygame.Rect(cell_position, (GRID_SIZE, GRID_SIZE))
        self.draw_rect(self.body_color, rect)
        self.draw_rect(BORDER_COLOR, rect, 1)

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
        self.surf = pygame.image.load(APPLE_IMG).convert_alpha()
        super().__init__(self.position, self.body_color)

    def draw(self):
        """Отрисовка."""
        apple_rect = self.surf.get_rect(topleft=self.position)
        screen.blit(self.surf, apple_rect)


class Snake(GameObject):
    """Класс для Змеи."""

    def clear_screan(self):
        """Очистка области экрана где ползает змейка."""
        rect = (pygame.Rect((0, 0), (BOARD_WIDTH, BOARD_HEIGHT)))
        self.draw_rect(BOARD_BACKGROUND_COLOR, rect)

    def reset(self):
        """Сброс Змейки."""
        self.positions = [BOARD_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = False
        self.speed = SPEED_START
        # Очищаем поле где ползает змейка
        self.clear_screan()

    def __init__(self, position=BOARD_CENTER, body_color=SNAKE_COLOR):
        self.reset()
        # Загрузка изображений змейки
        self.surf_body = pygame.image.load(SNAKE_BODY_IMG).convert_alpha()
        self.surf_head = pygame.image.load(SNAKE_HEAD_IMG).convert_alpha()
        self.surf_tail = pygame.image.load(SNAKE_TAIL_IMG).convert_alpha()
        self.surf_turn = pygame.image.load(SNAKE_TURN_IMG).convert_alpha()
        super().__init__(position, body_color)

    def get_head_position(self):
        """Получение координат головы змейки."""
        return self.positions[0]

    def get_second_position(self):
        """Получение координат головы змейки."""
        return self.positions[1]

    def get_third_position(self):
        """Получение координат головы змейки."""
        return self.positions[2]

    def get_tail_position(self):
        """Получение координат хвоста змейки."""
        return self.positions[len(self.positions) - 1]

    def get_pre_tail_position(self):
        """Получение координат хвоста змейки."""
        return self.positions[len(self.positions) - 2]

    def move(self):
        """Двигаем змейку на следующую клетку."""
        head_x, head_y = self.get_head_position()
        new_head_x = head_x + self.direction[0] * GRID_SIZE
        new_head_y = head_y + self.direction[1] * GRID_SIZE
        new_head_pos = (new_head_x % BOARD_WIDTH, new_head_y % BOARD_HEIGHT)
        self.positions.insert(0, new_head_pos)
        self.last = self.positions.pop()

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновление позиции."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Метод для отработки разницы координат при прохождение стенки
    @staticmethod
    def crop_delta_xy(delta):
        """Проверяем прохождение стенки"""
        if delta < -1:
            return -1
        elif delta > 1:
            return 1
        else:
            return delta

    # Метод для подсчитывание разницы координат элементов на поле
    def delta_xy(self, first_position, second_position):
        """Подсчитываем разницу координат"""
        delta_x = (first_position[0] - second_position[0]) // GRID_SIZE
        delta_y = (first_position[1] - second_position[1]) // GRID_SIZE
        delta_x = self.crop_delta_xy(delta_x)
        delta_y = self.crop_delta_xy(delta_y)
        return delta_x, delta_y

    def draw(self):
        """Отрисовка змеи."""
        # Отрисовка головы
        head_position = self.get_head_position()
        head_rect = self.surf_head.get_rect(topleft=head_position)
        rotate = pygame.transform.rotate(self.surf_head, IMG_TURN[self.direction])
        screen.blit(rotate, head_rect)

        # Отрисовка второго элемента змейки
        if len(self.positions) > 2:
            second_position = self.get_second_position()
            third_position = self.get_third_position()
            # Очистка второго элемента змейки
            second_rect = pygame.Rect(second_position, (GRID_SIZE, GRID_SIZE))
            self.draw_rect(BOARD_BACKGROUND_COLOR, second_rect)
            # Определеяем какое изображение будет на втором элменте
            turn_rect = None
            if head_position[0] == second_position[0] == third_position[0]:
                # Вертикальное тело
                angle = 0
            elif head_position[1] == second_position[1] == third_position[1]:
                # Горизонтальное тело
                angle = 90
            else:
                # Поворотное тело
                turn_rect = self.surf_turn.get_rect(topleft=second_position)
            # Отрисовка
            if turn_rect is None:
                # Отрисовка вертикального или горизонтального тела
                body_rect = self.surf_body.get_rect(topleft=second_position)
                rotate_body = pygame.transform.rotate(self.surf_body, angle)
                screen.blit(rotate_body, body_rect)
            else:
                # Отрисовка поворотного тела
                rotate_turn = pygame.transform.rotate(
                    self.surf_turn,
                    SNAKE_BODY_TURN_RULES[self.delta_xy(head_position, third_position), self.direction])
                screen.blit(rotate_turn, turn_rect)

        # Отрисовка хвоста
        tail_position = self.get_tail_position()
        if tail_position != head_position:
            # Очистка хвостового квадратика в цвет фона
            tail_rect = pygame.Rect(tail_position, (GRID_SIZE, GRID_SIZE))
            self.draw_rect(BOARD_BACKGROUND_COLOR, tail_rect)
            # Отрисовка изображения хвоста
            pre_tail_position = self.get_pre_tail_position()
            tail_rect = self.surf_tail.get_rect(topleft=tail_position)
            delta_x, delta_y = self.delta_xy(tail_position, pre_tail_position)
            angle = IMG_TURN[delta_x, delta_y]
            if (abs(tail_position[0] - pre_tail_position[0]) > GRID_SIZE) or (
               abs(tail_position[1] - pre_tail_position[1]) > GRID_SIZE):
                angle += 180
            rotate = pygame.transform.rotate(self.surf_tail, angle)
            screen.blit(rotate, tail_rect)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            self.draw_rect(BOARD_BACKGROUND_COLOR, last_rect)


class InfoBoard(GameObject):
    """Класс для экрана с информацией."""

    def __init__(self,
                 score=0,
                 speed=SPEED_START):
        self.font = pygame.font.Font(None, INFO_BOARD_FONT_SIZE)
        self.game_over_font = pygame.font.Font(None,
                                               INFO_BOARD_GAME_OVER_FONT_SIZE
                                               )
        self.score = score
        self.speed = speed
        self.set_score_and_speed(self.score, self.speed)

    def clean_screen(self):
        """Очистка экрана с информацией."""
        rect = pygame.Rect((0, BOARD_HEIGHT), (BOARD_WIDTH, INFO_BOARD_HEIGHT))
        # Отрисоква фона
        self.draw_rect(INFO_BOARD_BACKGROUND_COLOR, rect)
        # Отрисовка двойной рамки
        self.draw_rect(INFO_BOARD_BORDER1_COLOR, rect, INFO_BOARD_BORDER_SIZE)
        self.draw_rect(INFO_BOARD_BORDER2_COLOR, rect, INFO_BOARD_BORDER_SIZE // 2)

    def text_render(self, text, position):
        """Печать текста"""
        screen.blit(self.font.render(text, True, INFO_BOARD_FONT_COLOR), position)

    def draw_score(self):
        """Отрисовка экрана с информацией."""
        self.clean_screen()
        # Печатаем счёт
        self.text_render(f'СЧЁТ: {self.score}',
                         [INFO_BOARD_BORDER_SIZE * 2,
                          INFO_BOARD_BORDER_SIZE * 2 + BOARD_HEIGHT])
        # Печатаем скорость
        self.text_render(f'CКОРОСТЬ: {self.speed}',
                         [INFO_BOARD_BORDER_SIZE * 2,
                          INFO_BOARD_BORDER_SIZE * 2 + BOARD_HEIGHT + INFO_BOARD_FONT_SIZE])

    def set_score_and_speed(self, new_score, new_speed):
        """Установка счета и скорости и их отрисовка"""
        self.score = new_score
        self.speed = new_speed
        self.draw_score()

    def print_game_over(self):
        """Отрисовка надписи об окончание игры"""
        text_string_1 = 'ИГРА ЗАКОНЧЕНА'
        text_string_2 = 'Нажмите "Пробел" чтобы начать заново'
        # Создание текстовой поверхности
        text_1 = self.game_over_font.render(text_string_1,
                                            True,
                                            INFO_BOARD_GAME_OVER_FONT_COLOR)
        text_2 = self.font.render(text_string_2,
                                  True,
                                  INFO_BOARD_GAME_OVER_FONT_COLOR)
        # Получение прямоугольника текста и установка его позиции
        text_1_rect = text_1.get_rect(center=BOARD_CENTER)
        text_2_rect = text_2.get_rect(center=(BOARD_CENTER[0], BOARD_CENTER[1] + INFO_BOARD_GAME_OVER_FONT_SIZE))
        # Отображение текста на экране
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)


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
            return event.key


def main():
    """Main."""
    # Инициализация PyGame:
    pygame.init()

    # Создаем экземпляры классов.
    snake_object = Snake()
    apple_object = Apple()
    info_board = InfoBoard()

    while True:
        # Задержка
        clock.tick(round(snake_object.speed))
        # Считываем нажатие клавиатуры
        handle_keys(snake_object)
        # Обновляем и двигаем змейку
        snake_object.update_direction()
        snake_object.move()
        # Проверка столкновения головы с Яблоком и с своим телом
        head_position = snake_object.get_head_position()
        if head_position == apple_object.position:
            # Обрабатываем событие когда змея съела яблоко
            # Добавляем к хвосту змеи последний удаленный элемент
            snake_object.positions.append(snake_object.last)
            # Увелививаем скорость змейки
            snake_object.speed *= 1 + SPEED_COEFFICIENT / 100
            # Обновляем счет и скорость и отрисовываем
            info_board.set_score_and_speed(info_board.score + 1, round(snake_object.speed))
            # Генерируем новое положение яблока
            while True:
                apple_object.randomize_position()
                if apple_object.position not in snake_object.positions:
                    break
        elif head_position in snake_object.positions[3:]:
            # Обрабатываем событие когда змея врезалась в себя
            # Пишем на экране что это конец игры
            # Перед этим закрашиваем игровую области
            snake_object.clear_screan()
            info_board.print_game_over()
            pygame.display.update()
            # Ожидаем нажатия пробела чтобы начать заново игру
            while handle_keys(snake_object) != pygame.K_SPACE:
                pass
            # Сбрасываем змейку
            snake_object.reset()
            # Устанавливаем новое яблоко
            apple_object.randomize_position()
            # Обновляем счет и скорость и отрисовываем
            info_board.set_score_and_speed(0, round(snake_object.speed))
        # Отрисовка
        apple_object.draw()
        snake_object.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
