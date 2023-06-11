import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс НЛО"""

    def __init__(self, ai_settings, screen):
        """Инициализация НЛО и установка позиции"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения НЛО
        self.image = pygame.image.load('assets/alien_ufo.png')
        self.rect = self.image.get_rect()

        # Установка позиции
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение позиции в точное значение
        self.x = float(self.rect.x)

    def blitme(self):
        """Вывод изображения инопланетянина"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Изменение движения НЛО, если оно находится на краю экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Перемещение НЛО"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
