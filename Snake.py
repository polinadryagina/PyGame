import pygame
import sys
import random
import time
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
import sqlokno


class Game():
    def __init__(self):
        # размеры экрана
        self.screen_width = 720
        self.screen_height = 460
        # цвета
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)
        self.blue = pygame.Color(0, 0, 255)
        self.forest_green = pygame.Color(34, 139, 34)
        self.aqw = pygame.Color(102, 205, 170)
        self.orange = pygame.Color(255, 140, 0)
        self.yellow = pygame.Color(255, 255, 0)
        self.skyblue = pygame.Color(0, 191, 255)
        self.lightblue = pygame.Color(65, 105, 225)
        self.purple = pygame.Color(148, 0, 211)
        # количество кадров в секунду
        self.fps_controller = pygame.time.Clock()
        # переменная для отображения результата
        # сколько еды съела змея
        self.score = 0
        # скорость змеи
        self.sp = 12

    def init_and_check_for_errors(self):
        """Начальная функция для инициализации и
           проверки как запустится pygame"""
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface_and_title(self):
        """Задаем поверхность на которой будет все рисоваться
        и устанавливаем заголовок окна"""
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('Змейка')

    def event_loop(self, change_to):
        """Функция для отслеживания нажатий клавиш игроком"""
        # запуск цикла по ивентам
        for event in pygame.event.get():
            # если нажали клавишу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                # нажали escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def refresh_screen(self):
        """обновляем экран и задаем скорость"""
        pygame.display.flip()
        game.fps_controller.tick(self.sp)

    def show_speed(self, choicep=1):
        sp_font = pygame.font.SysFont('Monotype Corsiva', 24)
        sp_surf = sp_font.render(
            'Speed: {0}'.format(self.sp), True, self.white)
        sp_rect = sp_surf.get_rect()
        # дефолтный случай отображаем результат слева сверху
        if choicep == 1:
            sp_rect.midtop = (170, 10)
        else:
            sp_rect.midtop = (360, 140)
        # рисуем прямоугольник поверх surface
        self.play_surface.blit(sp_surf, sp_rect)

    def show_score(self, choice=1):
        """Отображение результата"""
        s_font = pygame.font.SysFont('Monotype Corsiva', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.white)
        s_rect = s_surf.get_rect()
        # дефолтный случай отображаем результат слева сверху
        if choice == 1:
            s_rect.midtop = (80, 10)
        else:
            s_rect.midtop = (360, 120)
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        """Функция для вывода надписи Game Over и результатов
        в случае завершения игры и выход из игры"""
        go_font = pygame.font.SysFont('Monotype Corsiva', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        self.show_speed(12)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        window = sqlokno.main()
        sys.exit()


class Snake():
    def __init__(self, snake_color):
        # позиция головы змеи и ее тела
        self.snake_head_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        # направление движения змеи
        self.direction = "RIGHT"
        # смена направления движения змеи
        # при нажатии соответствующих клавиш
        self.change_to = self.direction
        self.become_extra_fat = False

    def validate_direction_and_change(self):
        """Изменяем направление движения змеи только в том случае,
        если оно не противоположно текущему"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        """Изменяем положение головы змеи"""
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(
            self, score, food_pos, stick, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            # если съели еду то задаем новое положение еды случайным
            # образом и увеличиваем score на один
            food_pos = [random.randrange(1, screen_width / 10) * 10,
                        random.randrange(1, screen_height / 10) * 10]
            score += 1
        elif (stick.check_bang(self.snake_head_pos)):  # если врезались в бортик
            # генерируем новую позицию
            stick.generate()
            # отнимаем очки
            score -= 1
            # если змея врезалась в бортик,
            # укорачиваем хвостик на один сегмент
            self.snake_body.pop()
            self.snake_body.pop()
        elif score < 0:
            game.game_over()
        elif not self.become_extra_fat:
            # если не нашли еду, убираем последний сегмент
            self.snake_body.pop()
        else:
            self.become_extra_fat = False
        return score, food_pos

    def snake_color_change(
            self, color):
        if (color.check_bang_color(self.snake_head_pos)):  # если врезались в бортик
            # генерируем новую позицию
            color.generate_color()
            self.snake_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.snake_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.snake_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return color

    def snake_speed(
            self, sp, score, speed_pos, screen_width, screen_height):
        if (self.snake_head_pos[0] == speed_pos[0] and
                self.snake_head_pos[1] == speed_pos[1]):
            speed_pos = [random.randrange(1, screen_width / 10) * 10,
                         random.randrange(1, screen_height / 10) * 10]
            sp += 3
            score += 1
            # self.snake_body.insert(0, list(self.snake_head_pos))
            self.become_extra_fat = True
        return sp, score, speed_pos

    def snake_slow_speed(
            self, sp, speed_posm, screen_width, screen_height):
        if (self.snake_head_pos[0] == speed_posm[0] and
                self.snake_head_pos[1] == speed_posm[1]):
            speed_posm = [random.randrange(1, screen_width / 10) * 10,
                          random.randrange(1, screen_height / 10) * 10]
            sp -= 2
        return sp, speed_posm

    def draw_snake(self, play_surface, surface_color):
        """Отображение всех сегментов змеи"""
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        """Проверка, что столкнулись с концами экрана или сами с собой"""
        if any((
                self.snake_head_pos[0] > screen_width - 10
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height - 10
                or self.snake_head_pos[1] < 0
        )):
            game_over()
        for block in self.snake_body[1:]:
            # проверка, что первый элемент врезался в
            # любой другой элемент змеи
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food():
    def __init__(self, food_color, screen_width, screen_height):
        """Инит еды"""
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_size_xx = 5
        self.food_size_yy = -4
        self.food_pos = [random.randrange(1, screen_width / 10) * 10,
                         random.randrange(1, screen_height / 10) * 10]

    def draw_food(self, play_surface):
        """Отображение еды"""
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_xx, self.food_size_yy))
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_yy, self.food_size_xx))


class Color():
    def __init__(self, c_color, oran, yel, gr, bl, dbl, pur, screen_width, screen_height):
        """Инит бортика для изменения цвета"""
        # цвета блоков из которых состоят бортики
        self.c_color = c_color
        self.oran = oran
        self.yel = yel
        self.gr = gr
        self.bl = bl
        self.dbl = dbl
        self.pur = pur
        self.block_sz = 10  # размер блока в пикселах, для удобства расчётов
        self.n_hor = 1  # количество блоков по горизонтали
        self.n_ver = 7  # количество блоков по вертикали
        self.six = 6
        self.five = 5
        self.four = 4
        self.three = 3
        self.two = 2
        self.one = 1
        self.c_size_x = self.n_hor * self.block_sz
        self.c_size_y = self.n_ver * self.block_sz
        self.c_size_ys = self.six * self.block_sz
        self.c_size_yfv = self.five * self.block_sz
        self.c_size_yf = self.four * self.block_sz
        self.c_size_yb = self.three * self.block_sz
        self.c_size_ydb = self.two * self.block_sz
        self.c_size_yp = self.one * self.block_sz
        self.screen_width = screen_width
        self.screen_height = screen_height
        # генерируем позицию змейки
        self.generate_color()

    def generate_color(self):
        """Сгенерировать новый бортик"""
        self.color_pos = [random.randrange(1, self.screen_width / self.block_sz) * self.block_sz,
                          random.randrange(1, self.screen_height / self.block_sz) * self.block_sz]
        self.color_pos2 = [random.randrange(1, self.screen_width / self.block_sz) * self.block_sz,
                           random.randrange(1, self.screen_height / self.block_sz) * self.block_sz]
        self.color_pos3 = [random.randrange(1, self.screen_width / self.block_sz) * self.block_sz,
                           random.randrange(1, self.screen_height / self.block_sz) * self.block_sz]

        # формируем множество блоков, в которых голова змеи будет проверяться
        color_blocks = []
        for x in range(self.n_hor):
            for y in range(self.n_ver):
                color_blocks.append((self.color_pos[0] + x * self.block_sz, self.color_pos[1] + y * self.block_sz))
                color_blocks.append((self.color_pos2[0] + x * self.block_sz, self.color_pos2[1] + y * self.block_sz))
                color_blocks.append((self.color_pos3[0] + x * self.block_sz, self.color_pos3[1] + y * self.block_sz))

        self.color_set = set(color_blocks)

    def draw_color(self, play_surface):
        """Отображение бортиков"""
        pygame.draw.rect(
            play_surface, self.c_color, pygame.Rect(
                self.color_pos[0], self.color_pos[1],
                self.c_size_x, self.c_size_y))
        pygame.draw.rect(
            play_surface, self.oran, pygame.Rect(
                self.color_pos[0], self.color_pos[1],
                self.c_size_x, self.c_size_ys))
        pygame.draw.rect(
            play_surface, self.yel, pygame.Rect(
                self.color_pos[0], self.color_pos[1],
                self.c_size_x, self.c_size_yfv))
        pygame.draw.rect(
            play_surface, self.gr, pygame.Rect(
                self.color_pos[0], self.color_pos[1],
                self.c_size_x, self.c_size_yf))
        pygame.draw.rect(
            play_surface, self.bl, pygame.Rect(
                self.color_pos[0], self.color_pos[1],
                self.c_size_x, self.c_size_yb))
        pygame.draw.rect(
            play_surface, self.dbl, pygame.Rect(
                self.color_pos[0], self.color_pos[1],
                self.c_size_x, self.c_size_ydb))
        pygame.draw.rect(
            play_surface, self.pur, pygame.Rect(
                self.color_pos[0], self.color_pos[1],
                self.c_size_x, self.c_size_yp))

        pygame.draw.rect(
            play_surface, self.c_color, pygame.Rect(
                self.color_pos2[0], self.color_pos2[1],
                self.c_size_x, self.c_size_y))
        pygame.draw.rect(
            play_surface, self.oran, pygame.Rect(
                self.color_pos2[0], self.color_pos2[1],
                self.c_size_x, self.c_size_ys))
        pygame.draw.rect(
            play_surface, self.yel, pygame.Rect(
                self.color_pos2[0], self.color_pos2[1],
                self.c_size_x, self.c_size_yfv))
        pygame.draw.rect(
            play_surface, self.gr, pygame.Rect(
                self.color_pos2[0], self.color_pos2[1],
                self.c_size_x, self.c_size_yf))
        pygame.draw.rect(
            play_surface, self.bl, pygame.Rect(
                self.color_pos2[0], self.color_pos2[1],
                self.c_size_x, self.c_size_yb))
        pygame.draw.rect(
            play_surface, self.dbl, pygame.Rect(
                self.color_pos2[0], self.color_pos2[1],
                self.c_size_x, self.c_size_ydb))
        pygame.draw.rect(
            play_surface, self.pur, pygame.Rect(
                self.color_pos2[0], self.color_pos2[1],
                self.c_size_x, self.c_size_yp))

        pygame.draw.rect(
            play_surface, self.c_color, pygame.Rect(
                self.color_pos3[0], self.color_pos3[1],
                self.c_size_x, self.c_size_y))
        pygame.draw.rect(
            play_surface, self.oran, pygame.Rect(
                self.color_pos3[0], self.color_pos3[1],
                self.c_size_x, self.c_size_ys))
        pygame.draw.rect(
            play_surface, self.yel, pygame.Rect(
                self.color_pos3[0], self.color_pos3[1],
                self.c_size_x, self.c_size_yfv))
        pygame.draw.rect(
            play_surface, self.gr, pygame.Rect(
                self.color_pos3[0], self.color_pos3[1],
                self.c_size_x, self.c_size_yf))
        pygame.draw.rect(
            play_surface, self.bl, pygame.Rect(
                self.color_pos3[0], self.color_pos3[1],
                self.c_size_x, self.c_size_yb))
        pygame.draw.rect(
            play_surface, self.dbl, pygame.Rect(
                self.color_pos3[0], self.color_pos3[1],
                self.c_size_x, self.c_size_ydb))
        pygame.draw.rect(
            play_surface, self.pur, pygame.Rect(
                self.color_pos3[0], self.color_pos3[1],
                self.c_size_x, self.c_size_yp))

    def check_bang_color(self, snake_head):
        """Проверка что башка змеи врезалась в любую часть бортика"""
        return (snake_head[0], snake_head[1]) in self.color_set


class SpeedPlus():
    def __init__(self, speed_color, screen_width, screen_height):
        """Инит прибавления скорости"""
        self.speed_color = speed_color
        self.speed_size_x = 10
        self.speed_size_y = 10
        self.food_size_xx = 5
        self.food_size_yy = -4
        self.speed_pos = [random.randrange(1, screen_width / 10) * 10,
                          random.randrange(1, screen_height / 10) * 10]

    def draw_speed(self, play_surface):
        """Отображение еды для прибавления скорости"""
        pygame.draw.rect(
            play_surface, self.speed_color, pygame.Rect(
                self.speed_pos[0], self.speed_pos[1],
                self.speed_size_x, self.speed_size_y))
        pygame.draw.rect(
            play_surface, self.speed_color, pygame.Rect(
                self.speed_pos[0], self.speed_pos[1],
                self.food_size_xx, self.food_size_yy))
        pygame.draw.rect(
            play_surface, self.speed_color, pygame.Rect(
                self.speed_pos[0], self.speed_pos[1],
                self.food_size_yy, self.food_size_xx))


class SpeedMinus():
    def __init__(self, speed_color, screen_width, screen_height):
        """Инит убавления скорости скорости"""
        self.speed_color = speed_color
        self.speed_size_x = 10
        self.speed_size_y = 10
        self.food_size_xx = 5
        self.food_size_yy = -4
        self.speed_posm = [random.randrange(1, screen_width / 10) * 10,
                           random.randrange(1, screen_height / 10) * 10]

    def draw_speed_minus(self, play_surface):
        """Отображение еды для убавления скорости"""
        pygame.draw.rect(
            play_surface, self.speed_color, pygame.Rect(
                self.speed_posm[0], self.speed_posm[1],
                self.speed_size_x, self.speed_size_y))
        pygame.draw.rect(
            play_surface, self.speed_color, pygame.Rect(
                self.speed_posm[0], self.speed_posm[1],
                self.food_size_xx, self.food_size_yy))
        pygame.draw.rect(
            play_surface, self.speed_color, pygame.Rect(
                self.speed_posm[0], self.speed_posm[1],
                self.food_size_yy, self.food_size_xx))


class Stick:
    def __init__(self, stick_color, screen_width, screen_height):
        """Инит бортика"""
        self.stick_color = stick_color
        self.block_sz = 10  # размер блока в пикселах, для удобства расчётов
        self.n_hor = 1  # количество блоков по горизонтали
        self.n_hor2 = 2
        self.n_ver = 6  # количество блоков по вертикали
        self.ver = 3
        self.ver_n = 5
        self.stick_size_x = self.n_hor * self.block_sz
        self.stick_size_y = self.n_ver * self.block_sz
        self.stick_size_z = self.ver_n * self.block_sz
        self.stick_size_k = self.ver * self.block_sz
        self.stick_size_s = self.n_hor2 * self.block_sz
        self.screen_width = screen_width
        self.screen_height = screen_height
        # генерируем позицию змейки
        self.generate()

    def generate(self):
        """Сгенерировать новый бортик"""
        self.stick_pos = [random.randrange(1, self.screen_width / self.block_sz) * self.block_sz,
                          random.randrange(1, self.screen_height / self.block_sz) * self.block_sz]
        self.stick_pos2 = [random.randrange(1, self.screen_width / self.block_sz) * self.block_sz,
                           random.randrange(1, self.screen_height / self.block_sz) * self.block_sz]
        self.stick_pos3 = [random.randrange(1, self.screen_width / self.block_sz) * self.block_sz,
                           random.randrange(1, self.screen_height / self.block_sz) * self.block_sz]
        self.stick_pos4 = [random.randrange(1, self.screen_width / self.block_sz) * self.block_sz,
                           random.randrange(1, self.screen_height / self.block_sz) * self.block_sz]
        self.stick_pos5 = [random.randrange(1, self.screen_width / self.block_sz) * self.block_sz,
                           random.randrange(1, self.screen_height / self.block_sz) * self.block_sz]
        self.stick_pos6 = [random.randrange(1, self.screen_width / self.block_sz) * self.block_sz,
                           random.randrange(1, self.screen_height / self.block_sz) * self.block_sz]
        # формируем множество блоков, в которых голова змеи будет проверяться
        stick_blocks = []
        for x in range(self.n_hor):
            for y in range(self.n_ver):
                stick_blocks.append((self.stick_pos[0] + x * self.block_sz, self.stick_pos[1] + y * self.block_sz))
                stick_blocks.append((self.stick_pos2[0] + x * self.block_sz, self.stick_pos2[1] + y * self.block_sz))
                stick_blocks.append((self.stick_pos3[0] + x * self.block_sz, self.stick_pos3[1] + y * self.block_sz))
                stick_blocks.append((self.stick_pos4[0] + x * self.block_sz, self.stick_pos4[1] + y * self.block_sz))
                stick_blocks.append((self.stick_pos5[0] + x * self.block_sz, self.stick_pos5[1] + y * self.block_sz))
                stick_blocks.append((self.stick_pos6[0] + x * self.block_sz, self.stick_pos6[1] + y * self.block_sz))
        self.stick_set = set(stick_blocks)

    def draw_stick(self, play_surface):
        """Отображение бортика"""
        pygame.draw.rect(
            play_surface, self.stick_color, pygame.Rect(
                self.stick_pos[0], self.stick_pos[1],
                self.stick_size_x, self.stick_size_y))
        pygame.draw.rect(
            play_surface, self.stick_color, pygame.Rect(
                self.stick_pos2[0], self.stick_pos2[1],
                self.stick_size_x, self.stick_size_y))
        pygame.draw.rect(
            play_surface, self.stick_color, pygame.Rect(
                self.stick_pos3[0], self.stick_pos3[1],
                self.stick_size_x, self.stick_size_y))
        pygame.draw.rect(
            play_surface, self.stick_color, pygame.Rect(
                self.stick_pos4[0], self.stick_pos4[1],
                self.stick_size_x, self.stick_size_z))
        pygame.draw.rect(
            play_surface, self.stick_color, pygame.Rect(
                self.stick_pos5[0], self.stick_pos5[1],
                self.stick_size_x, self.stick_size_k))
        pygame.draw.rect(
            play_surface, self.stick_color, pygame.Rect(
                self.stick_pos6[0], self.stick_pos6[1],
                self.stick_size_x, self.stick_size_k))

    def check_bang(self, snake_head):
        """Проверка что башка змеи врезалась в любую часть бортика"""
        return (snake_head[0], snake_head[1]) in self.stick_set


game = Game()
snake = Snake(game.green)
food = Food(game.brown, game.screen_width, game.screen_height)
stick = Stick(game.blue, game.screen_width, game.screen_height)
speed_plus = SpeedPlus(game.white, game.screen_width, game.screen_height)
speed_minus = SpeedMinus(game.aqw, game.screen_width, game.screen_height)
color = Color(game.red, game.orange, game.yellow, game.green, game.skyblue, game.lightblue, game.purple,
              game.screen_width,
              game.screen_height)
game.init_and_check_for_errors()
game.set_surface_and_title()

while True:
    snake.change_to = game.event_loop(snake.change_to)
    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(
        game.score, food.food_pos, stick, game.screen_width, game.screen_height)
    color = snake.snake_color_change(color)
    game.sp, game.score, speed_plus.speed_pos = snake.snake_speed(sp=game.sp, score=game.score,
                                                                  speed_pos=speed_plus.speed_pos,
                                                                  screen_width=game.screen_width,
                                                                  screen_height=game.screen_height)
    game.sp, speed_minus.speed_posm = snake.snake_slow_speed(sp=game.sp,
                                                             speed_posm=speed_minus.speed_posm,
                                                             screen_width=game.screen_width,
                                                             screen_height=game.screen_height)
    snake.draw_snake(game.play_surface, game.black)
    food.draw_food(game.play_surface)
    color.draw_color(game.play_surface)
    stick.draw_stick(game.play_surface)
    speed_plus.draw_speed(game.play_surface)
    speed_minus.draw_speed_minus(game.play_surface)
    snake.check_for_boundaries(
        game.game_over, game.screen_width, game.screen_height)
    game.show_score()
    game.show_speed()
    game.refresh_screen()
