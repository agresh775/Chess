import pygame

class Settings:

    WIDTH, HEIGHT = 150, 50
    WHITE = (221, 228, 240)
    FONT = pygame.font.Font(None, 30)
    
    class Button:
        
        def __init__(self, x, y, width, height, text, color):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.text_image = Settings.FONT.render(self.text, True, (0, 0, 0))
            self.color = color
            
        def draw(self, surface):
            pygame.draw.rect(surface, self.color, self.rect, 0)
            pygame.draw.rect(surface, (0, 0, 0), self.rect, 3)
            text_rect = self.text_image.get_rect(center = self.rect.center)
            surface.blit(self.text_image, text_rect)

    def __init__(self, x, y, center_x, center_y):
        self.main_button = Settings.Button(x, y, self.WIDTH, self.HEIGHT, "SETTINGS", self.WHITE)
        self.button_white = Settings.Button(center_x - self.WIDTH // 2, center_y - self.HEIGHT * 2 + 6 , self.WIDTH, self.HEIGHT, "WHITE", self.WHITE)
        self.button_black = Settings.Button(center_x - self.WIDTH // 2, center_y - self.HEIGHT + 3, self.WIDTH, self.HEIGHT, "BLACK", self.WHITE)
        self.button_difficulty = Settings.Button(center_x - self.WIDTH // 2, center_y, self.WIDTH, self.HEIGHT, "DIFFICULTY: 1", self.WHITE)
        self.button_exit = Settings.Button(center_x - self.WIDTH // 2, center_y + self.HEIGHT - 3, self.WIDTH, self.HEIGHT, "EXIT", self.WHITE)
        self.is_opened = False

    def click(self, mouse_x, mouse_y):
        if self.is_opened:
            if self.button_white.rect.collidepoint(mouse_x, mouse_y):
                return "white"
            elif self.button_black.rect.collidepoint(mouse_x, mouse_y):
                return "black"
            elif self.button_difficulty.rect.collidepoint(mouse_x, mouse_y):
                if self.button_difficulty.text == "DIFFICULTY: 1":
                    self.button_difficulty.text = "DIFFICULTY: 2"
                    self.button_difficulty.text_image = self.FONT.render(self.button_difficulty.text, True, (0, 0, 0))
                else:
                    self.button_difficulty.text = "DIFFICULTY: 1"
                    self.button_difficulty.text_image = self.FONT.render(self.button_difficulty.text, True, (0, 0, 0))
                return "reset"
            elif self.button_exit.rect.collidepoint(mouse_x, mouse_y):
                return "exit"
            elif self.main_button.rect.collidepoint(mouse_x, mouse_y):
                self.is_opened = False
                return "close"
            else:
                return "open"
        else:
            if self.main_button.rect.collidepoint(mouse_x, mouse_y):
                self.is_opened = True
                return "open"
            else:
                return "nothing"

    def draw(self, surface):
        self.main_button.draw(surface)
        if self.is_opened:
            self.button_white.draw(surface)
            self.button_black.draw(surface)
            self.button_difficulty.draw(surface)
            self.button_exit.draw(surface)
