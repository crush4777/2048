import pygame
import sys



class GameLoginRegister:
    USER_FILE = "user.txt"
    BG_COLOR = '#96CDCD'
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def check_user(self, username, password):
        try:
            with open(self.USER_FILE, "r") as file:
                for line in file:
                    saved_username, saved_password = line.strip().split(":")
                    if username == saved_username and password == saved_password:
                        return True
        except FileNotFoundError:
            pass
        return False

    def register_user(self, username, password):
        with open(self.USER_FILE, "a") as file:
            file.write(f"{username}:{password}\n")

    def draw_text_input(self, rect, text, cursor_pos, show_cursor, blink_time):
        parts = text.split(": ", 1)
        if len(parts) == 2:
            label_text, input_text = parts
        else:
            label_text = text
            input_text = ""

        label_surface = self.font.render(label_text + ": ", True, (255, 255, 255))
        label_width = label_surface.get_width()
        label_height = label_surface.get_height()

        labels = ["Username", "Password"]
        max_label_width = max([self.font.size(label + ": ")[0] for label in labels])

        label_y = rect.y + (rect.height - label_height) // 2
        label_x = rect.x + max_label_width - label_width
        self.screen.blit(label_surface, (label_x, label_y))

        input_box_x = rect.x + max_label_width + 10
        input_box_y = rect.y
        input_box_width = rect.width - max_label_width - 10
        input_box_height = rect.height

        input_box_rect = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)

        border_width = 2
        pygame.draw.rect(self.screen, (255, 255, 255), input_box_rect, border_width)

        inner_rect = pygame.Rect(input_box_x + border_width, input_box_y + border_width,
                                 input_box_width - 2 * border_width,
                                 input_box_height - 2 * border_width)
        pygame.draw.rect(self.screen, (0, 0, 0), inner_rect)

        input_text_surface = self.font.render(input_text, True, (255, 255, 255))
        input_text_y = input_box_y + (input_box_height - input_text_surface.get_height()) // 2
        self.screen.blit(input_text_surface, (input_box_x + 5, input_text_y))

        if show_cursor and blink_time % 60 < 30:
            cursor_x = input_box_x + input_text_surface.get_width() + 5
            cursor_y = input_text_y
            cursor_height = self.font.get_height() - 2
            cursor_rect = pygame.Rect(cursor_x, cursor_y, 2, cursor_height)
            pygame.draw.rect(self.screen, (255, 255, 255), cursor_rect)

        return input_box_rect

    def handle_mouse_click(self, event, username_rect, password_rect, username, password,
                           show_username_cursor, show_password_cursor):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            username_input_box_rect = self.draw_text_input(username_rect, f"Username: {username}", 0,
                                                           show_username_cursor, 0)
            if username_input_box_rect.collidepoint(mouse_pos):
                show_username_cursor = True
                show_password_cursor = False
            password_input_box_rect = self.draw_text_input(password_rect,
                                                           f"Password: {'*' * len(password)}", 0,
                                                           show_password_cursor, 0)
            if password_input_box_rect.collidepoint(mouse_pos):
                show_password_cursor = True
                show_username_cursor = False
        return show_username_cursor, show_password_cursor

    def handle_keyboard_input(self, event, username, password, show_username_cursor, show_password_cursor):
        if event.type == pygame.KEYDOWN:
            if show_username_cursor:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            elif show_password_cursor:
                if event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.check_user(username, password):
                        return username, password, True
                    else:
                        print("用户名或密码错误")
                else:
                    password += event.unicode
        return username, password, False

    def draw_button(self, rect, text, is_hover, is_clicked):
        normal_color = (100, 200, 100) if text == "Login" else (100, 100, 200)
        hover_color = (120, 220, 120) if text == "Login" else (120, 120, 220)
        clicked_color = (80, 180, 80) if text == "Login" else (80, 80, 180)
        button_color = normal_color
        if is_hover:
            button_color = hover_color
        if is_clicked:
            button_color = clicked_color
        pygame.draw.rect(self.screen, button_color, rect)
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def login_screen(self, width, height):
        username = ""
        password = ""
        blink_time = 0

        from popup_window import PopupWindow
        popup = PopupWindow(self.screen)
        username_rect = pygame.Rect(width // 2 - 150, height // 3 - 50, 300, 50)
        password_rect = pygame.Rect(width // 2 - 150, height // 3 + 20, 300, 50)
        login_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 20, 200, 50)
        register_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 90, 200, 50)

        show_username_cursor = False
        show_password_cursor = False

        while True:
            is_username_hover = username_rect.collidepoint(pygame.mouse.get_pos())
            is_password_hover = password_rect.collidepoint(pygame.mouse.get_pos())
            is_login_button_hover = login_button_rect.collidepoint(pygame.mouse.get_pos())
            is_register_button_hover = register_button_rect.collidepoint(pygame.mouse.get_pos())
            is_login_button_clicked = False
            is_register_button_clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    username_rect = pygame.Rect(width // 2 - 150, height // 3 - 50, 300, 50)
                    password_rect = pygame.Rect(width // 2 - 150, height // 3 + 20, 300, 50)
                    login_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 20, 200, 50)
                    register_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 90, 200, 50)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    show_username_cursor, show_password_cursor = self.handle_mouse_click(event, username_rect,
                                                                                         password_rect,
                                                                                         username, password,
                                                                                         show_username_cursor,
                                                                                         show_password_cursor)
                    if login_button_rect.collidepoint(event.pos):
                        is_login_button_clicked = True
                    elif register_button_rect.collidepoint(event.pos):
                        is_register_button_clicked = True
                elif event.type == pygame.KEYDOWN:
                    username, password, login_success = self.handle_keyboard_input(event, username, password,
                                                                                   show_username_cursor,
                                                                                   show_password_cursor)
                    if login_success:
                        return True, username, width, height

            if is_login_button_clicked:
                if self.check_user(username, password):
                    return True, username, width, height
                else:
                    popup.display_popup("Incorrect username or password", button_text="OK")
                    print("用户名或密码错误")

            if is_register_button_clicked:
                self.register_screen(width, height)

            #self.screen.fill((60, 60, 30))
            self.screen.fill(pygame.Color(self.BG_COLOR))
            self.draw_text_input(username_rect, f"Username: {username}", 0,
                                 show_username_cursor, blink_time)
            self.draw_text_input(password_rect, f"Password: {'*' * len(password)}", 0,
                                 show_password_cursor, blink_time)

            self.draw_button(login_button_rect, "Login", is_login_button_hover, is_login_button_clicked)
            self.draw_button(register_button_rect, "Register", is_register_button_hover, is_register_button_clicked)

            blink_time += 1
            pygame.display.update()
            self.clock.tick(60)

    def register_screen(self, width, height):
        new_username = ""
        new_password = ""
        input_username = False
        input_password = False
        blink_time = 0

        from popup_window import PopupWindow
        popup = PopupWindow(self.screen)
        username_rect = pygame.Rect(width // 2 - 150, height // 3 - 50, 300, 50)
        password_rect = pygame.Rect(width // 2 - 150, height // 3 + 20, 300, 50)
        back_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 20, 200, 50)
        register_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 90, 200, 50)

        while True:
            is_username_hover = username_rect.collidepoint(pygame.mouse.get_pos())
            is_password_hover = password_rect.collidepoint(pygame.mouse.get_pos())
            is_back_button_hover = back_button_rect.collidepoint(pygame.mouse.get_pos())
            is_register_button_hover = register_button_rect.collidepoint(pygame.mouse.get_pos())
            is_back_button_clicked = False
            is_register_button_clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    username_rect = pygame.Rect(width // 2 - 150, height // 3 - 50, 300, 50)
                    password_rect = pygame.Rect(width // 2 - 150, height // 3 + 20, 300, 50)
                    back_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 20, 200, 50)
                    register_button_rect = pygame.Rect(width // 2 - 100, height // 2 + 90, 200, 50)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if username_rect.collidepoint(event.pos):
                        input_username = True
                        input_password = False
                    elif password_rect.collidepoint(event.pos):
                        input_username = False
                        input_password = True
                    elif back_button_rect.collidepoint(event.pos):
                        is_back_button_clicked = True
                    elif register_button_rect.collidepoint(event.pos):
                        is_register_button_clicked = True
                elif event.type == pygame.KEYDOWN:
                    if input_username:
                        if event.key == pygame.K_BACKSPACE:
                            new_username = new_username[:-1]
                        else:
                            new_username += event.unicode
                    elif input_password:
                        if event.key == pygame.K_BACKSPACE:
                            new_password = new_password[:-1]
                        elif event.key == pygame.K_RETURN:
                            if new_username and new_password:
                                self.register_user(new_username, new_password)
                                popup.display_popup("successfully registered", button_text="OK")
                                print("注册成功")
                                return
                            else:
                                popup.display_popup("User name and password cannot be empty", button_text="OK")
                                print("用户名和密码不能为空")
                        else:
                            new_password += event.unicode

            if is_back_button_clicked:
                return

            if is_register_button_clicked:
                if new_username and new_password:
                    if not self.check_user(new_username, new_password):
                        self.register_user(new_username, new_password)
                        popup.display_popup("successfully registered", button_text="OK")
                        print("注册成功")
                        return
                    else:
                        popup.display_popup("该用户名已存在，请选择其他用户名。", button_text="OK")
                else:
                    popup.display_popup("User name and password cannot be empty", button_text="OK")
                    print("用户名和密码不能为空")

            #self.screen.fill((60, 60, 30))
            self.screen.fill(pygame.Color(self.BG_COLOR))
            self.draw_text_input(username_rect, f"Username: {new_username}", 0, input_username, blink_time)
            self.draw_text_input(password_rect, f"Password: {'*' * len(new_password)}", 0, input_password, blink_time)

            self.draw_button(back_button_rect, "Back", is_back_button_hover, is_back_button_clicked)
            self.draw_button(register_button_rect, "Register", is_register_button_hover, is_register_button_clicked)

            blink_time += 1
            pygame.display.update()
            self.clock.tick(60)

