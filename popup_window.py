import pygame


class PopupWindow:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def show_popup(self, message, button_text="OK", button_width=100, button_height=40,
                   popup_bg_color=(0, 0, 0), button_bg_color=(100, 100, 100), button_hover_color=(120, 120, 120),
                   text_color=(255, 255, 255)):
        is_button_hover = False
        is_button_clicked = False
        clock = pygame.time.Clock()

        # 计算弹出框的大小和位置
        text_surface = self.font.render(message, True, text_color)
        text_rect = text_surface.get_rect()
        button_surface = self.font.render(button_text, True, text_color)
        button_rect = button_surface.get_rect()
        button_rect.width = button_width
        button_rect.height = button_height
        popup_width = max(text_rect.width, button_rect.width) + 20
        popup_height = text_rect.height + button_rect.height + 20
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        is_button_clicked = True
                elif event.type == pygame.MOUSEMOTION:
                    if button_rect.collidepoint(event.pos):
                        is_button_hover = True
                    else:
                        is_button_hover = False

            # 绘制弹出框背景
            pygame.draw.rect(self.screen, popup_bg_color, (popup_x, popup_y, popup_width, popup_height))

            # 绘制提示信息
            text_rect.centerx = popup_x + popup_width // 2
            text_rect.y = popup_y + 10
            self.screen.blit(text_surface, text_rect)

            # 绘制按钮
            button_rect.centerx = popup_x + popup_width // 2
            button_rect.y = popup_y + popup_height - button_rect.height - 10
            if is_button_hover:
                pygame.draw.rect(self.screen, button_hover_color, button_rect)
            else:
                pygame.draw.rect(self.screen, button_bg_color, button_rect)
            button_surface = self.font.render(button_text, True, text_color)
            button_rect_text = button_surface.get_rect(center=button_rect.center)
            self.screen.blit(button_surface, button_rect_text)

            pygame.display.flip()
            clock.tick(60)

            if is_button_clicked:
                return True

    def display_popup(self, message, button_text="close"):
        return self.show_popup(message, button_text)
