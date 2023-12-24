from graphics import Platform, platforms, screen, fps, size, MainCharacter, vertical_platforms, horizontal_platforms, \
    character, N
from data import cords

import pygame
import os

def initialization():
    for cord in cords:
        x, y, a, b = cord
        Platform(x + 1 / N, y, a - 2 / N, b, platforms, horizontal_platforms)
        Platform(x, y + 1 / N, a, b - 2 / N, platforms, vertical_platforms)

    # главный герой
    main_character = MainCharacter(0, 0, 10, 20, 'white')
    return main_character


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.x = size[0] // 2
        self.y = size[1] // 2

    # позиционировать камеру на объекте target
    def update(self):
        global start_jump_altitude, start_jump_from_wall_position
        d_x = main_character.rect.x - self.x
        d_y = main_character.rect.y - self.y

        r = 30 * N
        if d_x > r:
            for platform in platforms:
                platform.rect.x -= (d_x - r)
            main_character.rect.x -= d_x - r
            self.x = main_character.rect.x - r
            start_jump_from_wall_position -= (d_x - r)
        elif d_x < -r:
            for platform in platforms:
                platform.rect.x -= (d_x + r)
            main_character.rect.x -= d_x + r
            self.x = main_character.rect.x + r
            start_jump_from_wall_position -= (d_x + r)
        if d_y > r:
            for platform in platforms:
                platform.rect.y -= (d_y - r)
            main_character.rect.y -= d_y - r
            self.y = main_character.rect.y - r
            start_jump_altitude -= (d_y - r)
        elif d_y < -r:
            for platform in platforms:
                platform.rect.y -= (d_y + r)
            main_character.rect.y -= d_y + r
            self.y = main_character.rect.y + r
            start_jump_altitude -= (d_y + r)



if __name__ == '__main__':
    # Перемещаю экран на центр
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.display.set_mode(size)
    # таймер для обновления фпс - 60
    clock = pygame.time.Clock()

    # скорость падения, прыжка и передвижения


    # пустое значение
    start_jump_altitude = -100000
    start_jump_from_wall_position = 0
    jump = False
    jump_from_wall = False
    speeds_before_jump = [0, 0]

    # скорости
    move_speed = 40 * N
    fall_speed = 60 * N
    jump_speed = 60 * N

    # инициализация главного героя и платформ.
    main_character = initialization()

    # перемещение в стороны
    right = left = 0

    camera = Camera()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # если нажаты клавиши
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_d]:
                    if not jump_from_wall:
                        right = 1
                    else:
                        speeds_before_jump[0] = 1
                if keys[pygame.K_a]:
                    if not jump_from_wall:
                        left = -1
                    else:
                        speeds_before_jump[1] = -1

                # если нажат shift то ускоряется
                if keys[pygame.K_LSHIFT]:
                    move_speed = 60 * N
                else:
                    move_speed = 40 * N

                # при нажатии на пробел - прыжок
                if event.key == pygame.K_SPACE and (main_character.get_hor() or main_character.get_ver()):
                    start_jump_altitude = main_character.rect.y + 1
                    # проверка на зацепление за текстуры(был баг без этого)
                    main_character.rect.y -= 2
                    if main_character.get_ver() and main_character.get_hor():
                        main_character.rect.x += 1
                        if main_character.get_ver():
                            main_character.rect.x -= 2
                    # объявляю прыжок
                    jump = True
                    if main_character.get_ver():  # если есть касани вертикально стены, то объявляю прыжок от стены
                        jump_from_wall = True
                        speeds_before_jump = [0, 0]
                        main_character.rect.x -= 1
                        # запоминаю скорости
                        if main_character.get_ver():
                            right = 1
                            left = 0
                        else:
                            right = 0
                            left = -1

                        main_character.rect.x += 1
                        start_jump_from_wall_position = main_character.rect.x
                    else:
                        jump_from_wall = False

            # если отпускается какая-либо клавиша
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = 0
                if event.key == pygame.K_a:
                    left = 0
                if event.key == pygame.K_LSHIFT:
                    move_speed = 40 * N

        # цвет можно поменять. Это будет цвет фона
        screen.fill(pygame.color.Color(200, 200, 200))

        # перемещение в стороны
        move_hor = right + left

        # определение скорости падения
        if main_character.get_ver() and not jump:
            fall_speed = 30 * N
        elif not jump:
            fall_speed = 60 * N
        if jump:
            # при прыжке, на самой верхней точке скорость меньше
            fall_speed = -(30 * N - start_jump_altitude + main_character.rect.y) * 5
            if not fall_speed:
                jump = False
                fall_speed = 60 * N
        # если совершается прыжок от стены
        if jump_from_wall:
            # если уже далеко от стены
            if abs(main_character.rect.x - start_jump_from_wall_position) > 10 * N:
                jump_from_wall = False
                right, left = speeds_before_jump
                speeds_before_jump = [0, 0]

        camera.update()

        # отрисовываю все группы спрайтов
        platforms.draw(screen)
        platforms.update()

        character.draw(screen)
        jump = main_character.update(move_hor, jump, move_speed, fall_speed)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
