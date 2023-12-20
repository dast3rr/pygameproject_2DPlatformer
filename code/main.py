from graphics import Platform, platforms, screen, fps, size, MainCharacter, vertical_platforms, horizontal_platforms, \
    character
from data import cords

import pygame
import os

if __name__ == '__main__':
    # Перемещаю экран на центр
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.display.set_mode(size)
    # таймер для обновления фпс - 60
    clock = pygame.time.Clock()

    # скорость падения, прыжка и передвижения
    move_speed = 80
    fall_speed = 120
    jump_speed = 120

    # пустое значение
    start_jump_altitude = -100000
    jump = False

    # Создаю чёрные прямоугольники стен по кординатам из data.py
    for cord in cords:
        x, y, a, b = cord
        Platform(x + 1, y, a - 2, b, platforms, horizontal_platforms)
        Platform(x, y + 1, a, b - 2, platforms, vertical_platforms)


    # создаю два прямоугольника, один отвечает за пересечение по вертикали, другой - по горизонтали
    main_character = MainCharacter(100, 185, 20, 40)

    # перемещение в стороны
    right = left = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # если нажаты клавиши
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_d]:
                    right = 1
                if keys[pygame.K_a]:
                    left = -1

                # если нажат shift то ускоряется
                if keys[pygame.K_LSHIFT]:
                    move_speed = 120
                else:
                    move_speed = 80

                # при нажатии на пробел - прыжок
                if keys[pygame.K_SPACE] and (main_character.get_hor() or main_character.get_ver()):
                    start_jump_altitude = main_character.rect.y + 1
                    main_character.rect.y -= 2
                    if main_character.get_ver() and main_character.get_hor():
                        main_character.rect.x -= 1
                        if main_character.get_ver():
                            main_character.rect.x += 2
                    jump = True

            # если отпускается какая-либо клавиша
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = 0
                if event.key == pygame.K_a:
                    left = 0
                if event.key == pygame.K_LSHIFT:
                    move_speed = 80

        # цвет можно поменять. Это будет цвет фона
        screen.fill(pygame.color.Color(200, 200, 200))

        # перемещение в стороны
        move_hor = right + left

        if move_hor < 0:
            # если движение влево, то изначально значение отрицательно
            r = range(-(move_hor * move_speed) // fps)
        else:
            r = range((move_hor * move_speed) // fps)
        for i in r:
            # начально условие
            condition = main_character.get_ver()
            # потом двигаю персонажа
            main_character.rect.x += move_hor
            # если условие не поменялось, то возвращаю обратно, и в любом случаю прекращаю движение
            if main_character.get_ver():
                if condition:
                    main_character.rect.x -= move_hor
                break

        if main_character.get_ver():
            fall_speed = 60
        else:
            fall_speed = 120
        if jump:
            fall_speed = -(60 - start_jump_altitude + main_character.rect.y) * 5
            print(fall_speed)
            if not fall_speed:
                jump = False
                fall_speed = 120


        if fall_speed:
            # падение и скольжение
            if fall_speed < 0:
                # отрицательно при прыжке
                r = range(-(fall_speed // fps))
            else:
                r = range(fall_speed // fps)
            for i in r:
                condition = main_character.get_hor()
                main_character.rect.y += fall_speed // abs(fall_speed)
                if main_character.get_ver():
                    if jump:
                        main_character.rect.y += 3
                        jump = False
                        break
                    if condition:
                        main_character.rect.y -= fall_speed // abs(fall_speed)
                    break



        # отрисовываю все группы спрайтов
        platforms.draw(screen)
        platforms.update()

        character.draw(screen)
        character.update()

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
