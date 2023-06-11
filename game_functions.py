import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, stats, screen, ship, aliens, bullets):
    """Реагирование на нажатие клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        ship.fire = True
    elif event.key == pygame.K_ESCAPE:
        stats.game_active = not stats.game_active
        if stats.game_active == True:
            pygame.display.set_caption('UFO destroyer')
        else:
            pygame.display.set_caption('UFO destroyer (ПАУЗА)')
        


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускание снаряда, если лимит не достигнут"""
    # Создание нового снаряда
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        # Звук выстрела снаряда
        som = pygame.mixer.Sound('assets/fire.wav')
        som.set_volume(0.3)
        som.play()


def check_keyup_events(event, ship):
    """Изменение движения"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_SPACE:
        ship.fire = False


def check_events(ai_settings, screen, stats, sb, play_button, music_button, exit_button, ship, aliens, bullets):
    """Реагирование на нажатие клавиш"""
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

            # Проверка нажатия на кнопку "Включить/выключить музыку"
            if music_button.rect.collidepoint(mouse_x, mouse_y):
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    music_button.button_color = (220, 0, 0)
                    music_button.text_color = (230, 230, 230)
                    music_button.prep_msg("МУЗЫКА ВКЛ.")
                    
                else:
                    pygame.mixer.music.unpause()
                    music_button.button_color = (254, 178, 54)
                    music_button.text_color = (57, 48, 79)
                    music_button.prep_msg("МУЗЫКА ВЫКЛ.")

            # Проверка нажатия на кнопку "Выйти"
            if exit_button.rect.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                sys.exit()




def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запуск новой игры"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс настроек игры
        ai_settings.initialize_dynamic_settings()

        # Сброс статистики
        stats.reset_stats()
        stats.game_active = True

        pygame.display.set_caption('UFO destroyer')

        # Сброс изображения счета
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        # Очистка списка НЛО и снарядов
        aliens.empty()
        bullets.empty()

        # Создание коробля и НЛО
        create_fleet(ai_settings, screen, ship, aliens)
        # Центрирование коробля игрока
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, music_button, exit_button):
    """Обновление изображения экрана"""
    # Перерисовка экрана
    screen.fill(ai_settings.bg_color)

    if ship.fire:
        fire_bullet(ai_settings, screen, ship, bullets)

    # Изменение отображения снарядов после сталкновения с НЛО
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Отображение счета
    sb.show_score()

    # Вывод кнопок, если игра не активна
    if not stats.game_active:
        play_button.draw_button()
        music_button.draw_button()
        exit_button.draw_button()
        

    # Сделать экран видимым
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #Обноление положения снарядов и удаление ненужных
    bullets.update()

    # Удаление ненужных снарядов
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Реакция на столкновения снаряда с НЛО"""
    # Удаления снарядов столкнувшихся с НЛО
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Запуск следующей волны, если все НЛО уничтожены
        bullets.empty()
        ai_settings.increase_speed()

        # Переход на новый уровень
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Определение количества НЛО, которые могут поместиться в ряд"""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определение количества строк с НЛО, которые могут поместиться на экране"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows - 4


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Создание НЛО-пришельца и установка его позиции
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создание полного флота"""
    # Создание НЛО-пришельца и подсчет рядов
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Создание линии НЛО
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Реакция на случай, если НЛО достигли края"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Движение всего флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверка находится ли флот НЛО на правом или левом краю экрана"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Проверка столкнулся ли корабль игрока с НЛО пришельца
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Проверка достигло ли НЛО нижней части экрана
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Столкновение игрока с НЛО"""
    if stats.ship_left > 0:
        stats.ship_left -= 1

        # Очистка пришельцев и снарядов
        aliens.empty()
        bullets.empty()

        # Создание нового флота и центрирование корабля игрока
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверка достигли ли какие-либо НЛО нижней части экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Поражение корабля игрока
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Установка рекорда"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
