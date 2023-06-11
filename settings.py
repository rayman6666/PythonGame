class Settings:
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализировать настройки игры"""
        # Настройки экрана
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (57, 0, 77)

        # Настройки космического корабля
        self.ship_limit = 3

        # Настройки снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 204, 0
        self.bullets_allowed = 3

        # Настройки НЛО
        self.fleet_drop_speed = 10

        # Увеличивается скорость игры
        self.speedup_scale = 1.1

        # Скорость, с которой баллы за каждое сбитое НЛО увеличиваются
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализация настроек, которые меняются в ходе игры"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # Fleet_direction, равный 1, означает движение вправо, -1 влево
        self.fleet_direction = 1

        # Пунктуация
        self.alien_points = 10

    def increase_speed(self):
        """Изменение настроек скорости"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
