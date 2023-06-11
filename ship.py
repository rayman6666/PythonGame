import pygame


class Ship:

    def __init__(self, ai_settings, screen):
        """Инициализация космического корабля и устанавление начальной позиции"""
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения
        self.image = pygame.image.load('assets\player_ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Ставит корабль в середину в низу
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Сохраняет десятичное значение для центра космического корабля
        self.center = float(self.rect.centerx)

        # Движение
        self.moving_right = False
        self.moving_left = False

        # Огонь
        self.fire = False

    def update(self):
        """Обновление положения корабля в соответствии с выбранным движением"""
        # Обновление значение центра коробля
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Обновление объекта с учетом self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Вывод изображения коробля"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Ставит корабль в текущее положение"""
        self.center = self.screen_rect.centerx
