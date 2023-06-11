import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс управления снарядами игрока"""

    def __init__(self, ai_settings, screen, ship):
        """Создание объекта снаряда"""
        super().__init__()
        self.screen = screen

        # установка положения снаряда
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Преобразование позиции в более точное значение
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Движение снаряда вверх"""
        # Обновление позиции
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод изображения снаряда"""
        pygame.draw.rect(self.screen, self.color, self.rect)