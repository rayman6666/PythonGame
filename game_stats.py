class GameStats:
    """Хранение статистики"""

    def __init__(self, ai_settings):
        """Инициализация статистики"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Запуск вторжения НЛО
        self.game_active = True

        # Запуск режима ожидания
        self.game_active = False

        # Установка рекорда
        self.high_score = 0

    def reset_stats(self):
        """Инициализация данных, которые изменяются в игре"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1