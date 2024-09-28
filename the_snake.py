from random import randint

import pygame as pg
import sys

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Черный цвет
BLACK_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Позиция по умолчанию
BASIC_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """
    Имеет цвет, позицию и абстрактный метод draw.

    Методы класса:
    draw - изображает предмет на экране.
    """

    def __init__(self, position=BASIC_POSITION, body_color=BLACK_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод, который будет переопределен в подклассах."""
        raise NotImplementedError

    def draw_cell(self, position, body_color):
        """Отрисовывает ячейка на экран."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Имеет цвет, позицию, может изображать себя и менять позицию.

    Методы класса:
    draw - изображает яблоко на экране.
    randomize_position - меняет позицию яблока на экране.
    """

    def __init__(self, body_color=APPLE_COLOR, busy_cell=[BASIC_POSITION]):
        super().__init__(body_color=body_color)
        self.randomize_position(busy_cell=busy_cell)

    def randomize_position(self, busy_cell=[BASIC_POSITION]):
        """Метод генерирующий случайную позицию для яблока"""
        new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        while (new_position in busy_cell):
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.position = new_position

    def draw(self):
        """Метод изображающий яблоко на экране"""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """
    Имеет цвет, позицию, длину и направление движения,
    может изображать себя, двигаться, менять направление движения.

    Методы класса:
    draw - изображает змейку на экране.
    update_direction - меняет направление движения.
    move - перемещает голову змейки и уменьшает ее, если нужно.
    get_head_position - возвращает положение головы змейки.
    reset - возвращает змейку в начальное состояния.
    """

    def __init__(self, postion=BASIC_POSITION, body_color=SNAKE_COLOR):
        super().__init__(position=postion, body_color=body_color)
        self.reset()

    def update_direction(self, next_direction):
        """Метод обновляющий направление движения змейки"""
        self.direction = next_direction

    def move(self):
        """Метод перемещающий голову змейки и уменьшающий ее длину"""
        head = self.get_head_position()
        new_x = (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        new_position = (new_x, new_y)

        self.positions.insert(0, new_position)

        if self.length < len(self.positions) - 1:
            self.positions.pop()

    def draw(self):
        """Метод рисующий змейку на экране"""
# Без цикла длина змеи на экране не увеличивается
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)
        head_position = self.get_head_position()
        self.draw_cell(head_position, self.body_color)

    def get_head_position(self):
        """Метод возвращающий положение головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод возвращающий змейку в начальное состояние"""
        self.length = 1
        self.positions = [BASIC_POSITION]
        self.direction = RIGHT


def handle_keys(game_object):
    """Метод управляющий действиями пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit(0)


def main():
    """Метод, содержащий бесконечный цик, в котором происходят события игры"""
    snake = Snake()
    apple = Apple(busy_cell=snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        else:

            if snake.get_head_position() == apple.position:
                snake.length += 1
                apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
