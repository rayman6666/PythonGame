import pygame

from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Инициализация запуска игры
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('UFO destroyer')

    # Кнопка запуска
    play_button = Button(ai_settings, screen, "Новая игра")



    # Кнопка включения/выключения музыки
    music_button = Button(ai_settings, screen, "МУЗЫКА ВЫКЛ.")
    music_button.rect.centerx = play_button.rect.centerx
    music_button.rect.centery = play_button.rect.centery + 80
    
    music_button.msg_image_rect.y = play_button.rect.centery + 61

    
    # Кнопка выхода
    exit_button = Button(ai_settings, screen, "Выйти")
    exit_button.rect.centerx = play_button.rect.centerx
    exit_button.rect.centery = music_button.rect.centery + 90
    
    exit_button.msg_image_rect.y = play_button.rect.centery + 151



    # Создание объектов хранения игровой статиски
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Создание коробля игрока, группу снарядов и группу НЛО
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Вывод отображения НЛО
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Загрузка музыки
    pygame.mixer.music.load('assets\8-bit_music.mp3')
    pygame.mixer.music.play(-1) 

    # Запуск основного игрового цикла
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, music_button, exit_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, music_button, exit_button)


run_game()
