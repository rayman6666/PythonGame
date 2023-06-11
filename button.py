import pygame.font


class Button:

    def __init__(self, ai_settings, screen, msg):
        """Инициализация кнопки"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Определение размера кнопки
        self.width, self.height = 365, 50
        self.button_color = (254, 178, 54)
        self.text_color = (57, 48, 79)
        self.font = pygame.font.Font('assets\PsychicForce2012Monospaced.otf', 48)

        # Создает прямоугольный объект кнопки
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.msg = msg

        # Закрепление кнопки
        self.prep_msg(self.msg)

    def prep_msg(self, msg):
        """Превращение сообщения в изображение и центрирование кнопки"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Вывод кнопки и сообщения
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
