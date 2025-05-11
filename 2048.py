import random
import sys
import time
from collections.abc import Iterable
from functools import reduce
import pygame
import tkinter as tk
from tkinter import messagebox
from functools import reduce
from collections.abc import Iterable

from popup_window import PopupWindow
from Judge_Move import JudgeAndMove
from game_login_register import GameLoginRegister

from ai import analyze_moves
from ai import rl_analyze_moves




def get_theme(theme):
    
    bg_color = '#92877d'

    
    theme_colors = {
        'bright': {
            'bg_color': '#ffffff',  # 明亮主题使用白色背景
        },
        'light green': {
            'bg_color': '#90ee90',  # 浅绿色主题使用浅绿色背景
        },
        'gray': {
            'bg_color': '#808080',  # 灰色主题使用灰色背景
        }
    }

    # 根据传入的主题获取对应的颜色设置
    if theme in theme_colors:
        bg_color = theme_colors[theme]['bg_color']

    return bg_color



def show_game_over(screen, score, width, height, theme):
    # 动态计算字体大小
    font_size_big = int(height * 0.1)
    font_size_small = int(height * 0.05)
    font_color = (255, 255, 255)
    font_big = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_big)
    font_small = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_small)
    surface = screen.convert_alpha()
    surface.fill((0, 0, 0, 2))
    text1 = font_big.render(f'{score}', True, (0, 255, 0))
    text_rect1 = text1.get_rect()
    text_rect1.centerx, text_rect1.centery = width // 2, height // 2 - int(height * 0.15)
    surface.blit(text1, text_rect1)
    text = font_big.render(f'Game Over!', True, font_color)
    text_rect = text.get_rect()
    text_rect.centerx, text_rect.centery = width // 2, height // 2 - int(height * 0.07)
    surface.blit(text, text_rect)
    # 动态计算按钮大小和位置
    button_width = int(width * 0.15)
    button_height = int(height * 0.07)
    button_start_x_left = width // 2 - button_width - int(width * 0.03)
    button_start_x_right = width // 2 + int(width * 0.03)
    button_start_y = height // 2 - button_height // 2 + int(height * 0.03)
    pygame.draw.rect(surface, (0, 255, 255), (button_start_x_left, button_start_y, button_width, button_height))
    text_restart = font_small.render('Restart', True, (0, 33, 66))
    text_restart_rect = text_restart.get_rect()
    text_restart_rect.centerx, text_restart_rect.centery = button_start_x_left + button_width // 2, button_start_y + button_height // 2
    surface.blit(text_restart, text_restart_rect)
    pygame.draw.rect(surface, (0, 255, 255), (button_start_x_right, button_start_y, button_width, button_height))
    text_quit = font_small.render('Quit', True, (0, 33, 66))
    text_quit_rect = text_quit.get_rect()
    text_quit_rect.centerx, text_quit_rect.centery = button_start_x_right + button_width // 2, button_start_y + button_height // 2
    surface.blit(text_quit, text_quit_rect)
    clock = pygame.time.Clock()
    while True:
        screen.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                # 重新计算字体大小
                font_size_big = int(height * 0.1)
                font_size_small = int(height * 0.05)
                font_big = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_big)
                font_small = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_small)
                surface = screen.convert_alpha()
                surface.fill((0, 0, 0, 2))

                # 重新绘制得分
                text1 = font_big.render(f'{score}', True, (0, 255, 0))
                text_rect1 = text1.get_rect()
                text_rect1.centerx, text_rect1.centery = width // 2, height // 2 - int(height * 0.15)
                surface.blit(text1, text_rect1)

                # 重新绘制 Game Over 文本
                text = font_big.render(f'Game Over!', True, font_color)
                text_rect = text.get_rect()
                text_rect.centerx, text_rect.centery = width // 2, height // 2 - int(height * 0.07)
                surface.blit(text, text_rect)

                # 重新计算按钮大小和位置
                button_width = int(width * 0.15)
                button_height = int(height * 0.07)
                button_start_x_left = width // 2 - button_width - int(width * 0.03)
                button_start_x_right = width // 2 + int(width * 0.03)
                button_start_y = height // 2 - button_height // 2 + int(height * 0.03)

                pygame.draw.rect(surface, (0, 255, 255),
                                 (button_start_x_left, button_start_y, button_width, button_height))
                text_restart = font_small.render('Restart', True, (0, 33, 66))
                text_restart_rect = text_restart.get_rect()
                text_restart_rect.centerx, text_restart_rect.centery = button_start_x_left + button_width // 2, button_start_y + button_height // 2
                surface.blit(text_restart, text_restart_rect)

                pygame.draw.rect(surface, (0, 255, 255),
                                 (button_start_x_right, button_start_y, button_width, button_height))
                text_quit = font_small.render('Quit', True, (0, 33, 66))
                text_quit_rect = text_quit.get_rect()
                text_quit_rect.centerx, text_quit_rect.centery = button_start_x_right + button_width // 2, button_start_y + button_height // 2
                surface.blit(text_quit, text_quit_rect)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                if text_quit_rect.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()
                if text_restart_rect.collidepoint(pygame.mouse.get_pos()):
                    return True, width, height, theme
        pygame.display.update()
        clock.tick(60)


def draw_text(screen, font, text, color, x, y):
    """绘制文本到屏幕上"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(screen, x, y, width, height, color, text, font, text_color):
    """绘制按钮并添加文本"""
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(screen, font, text, text_color, x + width // 2, y + height // 2)


def show_settings(screen, width, height, theme):
    # 定义颜色（以十六进制格式）
    DARK_COLOR = '#8B7D6B'
    LIGHT_COLOR = '#96CDCD'
    LIGHT_GREEN_COLOR = '#B4EEB4'
    DEFAULT_BUTTON_COLOR = '#0080ff'
    DEFAULT_BUTTON_HOVER_COLOR = '#00aaff'
    DEFAULT_BUTTON_CLICKED_COLOR = '#00c8ff'
    TEXT_COLOR = '#ffffff'

    # 定义主题对应的颜色设置
    theme_settings = {
        'bright': {
            'background': LIGHT_COLOR,
            'button': {
                'normal': '#0080ff',
                'hover': '#00aaff',
                'clicked': '#00c8ff'
            }
        },
        'light green': {
            'background': LIGHT_GREEN_COLOR,
            'button': {
                'normal': '#008000',
                'hover': '#00a000',
                'clicked': '#00c000'
            }
        },
        'gray': {
            'background': DARK_COLOR,
            'button': {
                'normal': '#808080',
                'hover': '#a0a0a0',
                'clicked': '#c0c0c0'
            }
        }
    }

    current_background = theme  # 默认背景颜色为灰暗
    current_size = "medium"  # 默认大小为中
    current_difficulty = "normal"  # 默认难度为普通
    current_button_colors = theme_settings['gray']['button']

    # 动态计算字体大小
    font_size_big = int(height * 0.1)
    font_size_small = int(height * 0.05)
    font_big = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_big)
    font_small = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_small)

    # 定义选项和按钮相关信息
    options = ['主题', '大小', '难度']
    sub_options = [
        ['bright', 'light green', 'gray'],  # ['明亮', '灰白','灰暗'],
        ['large', 'medium', 'small'],  # ['大', '中', '小'],
        ['simple', 'normal', 'difficult']  # ['简单', '普通', '困难']
    ]
    button_width = int(width * 0.1)
    button_height = int(height * 0.05)
    option_x = width // 2 - int(width * 0.2)
    button_start_x = width // 2 + int(width * 0.05)
    option_y = height // 2 - len(options) * int(height * 0.1) // 2

    # 记录每个按钮的状态（正常、悬停、点击）
    button_states = []
    for sub_option in sub_options:
        button_states.append([0] * len(sub_option))

    clock = pygame.time.Clock()
    while True:
        # 将十六进制颜色转换为 RGB 格式
        bg_rgb = tuple(int(current_background.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        screen.fill(bg_rgb)

        # 绘制设置标题
        draw_text(screen, font_big, 'setting', tuple(int(TEXT_COLOR.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)),
                  width // 2, height // 2 - int(height * 0.35))

        # 绘制设置选项和按钮
        option_y = height // 2 - len(options) * int(height * 0.1) // 2
        for i, option in enumerate(options):
            draw_text(screen, font_small, option, tuple(int(TEXT_COLOR.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)),
                      option_x, option_y)
            sub_x = button_start_x
            for j, sub_option in enumerate(sub_options[i]):
                if button_states[i][j] == 0:
                    color_hex = current_button_colors['normal']
                elif button_states[i][j] == 1:
                    color_hex = current_button_colors['hover']
                else:
                    color_hex = current_button_colors['clicked']
                color_rgb = tuple(int(color_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
                draw_button(screen, sub_x, option_y - button_height // 2, button_width, button_height, color_rgb,
                            sub_option, font_small, tuple(int(TEXT_COLOR.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)))
                sub_x += button_width + int(width * 0.02)
            option_y += int(height * 0.1)

        # 动态计算关闭按钮大小和位置
        close_button_width = int(width * 0.15)
        close_button_height = int(height * 0.07)
        close_button_start_x = width // 2 - close_button_width // 2
        close_button_start_y = height // 2 + int(height * 0.2)
        close_button_rect = pygame.Rect(close_button_start_x, close_button_start_y, close_button_width,
                                        close_button_height)
        close_button_color_hex = current_button_colors['normal']
        close_button_color_rgb = tuple(int(close_button_color_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        draw_button(screen, close_button_start_x, close_button_start_y, close_button_width, close_button_height,
                    close_button_color_rgb, 'close', font_small,
                    tuple(int(TEXT_COLOR.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                # 重新计算字体大小
                font_size_big = int(height * 0.1)
                font_size_small = int(height * 0.05)
                font_big = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_big)
                font_small = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_small)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if close_button_rect.collidepoint(mouse_pos):
                    return width, height, current_background, current_size, current_difficulty
                for i, sub_option_list in enumerate(sub_options):
                    sub_x = button_start_x
                    for j, _ in enumerate(sub_option_list):
                        button_rect = pygame.Rect(sub_x, option_y - button_height // 2 - int(height * 0.1) * len(
                            sub_options) + int(height * 0.1) * i, button_width, button_height)
                        if button_rect.collidepoint(mouse_pos):
                            button_states[i] = [0] * len(sub_option_list)
                            button_states[i][j] = 2
                            if i == 0:
                                # 根据选择的主题更新背景颜色和按钮颜色
                                theme = sub_options[i][j]
                                current_background = theme_settings[theme]['background']
                                current_button_colors = theme_settings[theme]['button']
                            elif i == 1:
                                current_size = sub_options[i][j]
                            elif i == 2:
                                current_difficulty = sub_options[i][j]
                        sub_x += button_width + int(width * 0.02)
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for i, sub_option_list in enumerate(sub_options):
                    sub_x = button_start_x
                    for j, _ in enumerate(sub_option_list):
                        button_rect = pygame.Rect(sub_x, option_y - button_height // 2 - int(height * 0.1) * len(
                            sub_options) + int(height * 0.1) * i, button_width, button_height)
                        if button_rect.collidepoint(mouse_pos):
                            if button_states[i][j] == 0:
                                button_states[i][j] = 1
                        else:
                            if button_states[i][j] == 1:
                                button_states[i][j] = 0
                        sub_x += button_width + int(width * 0.02)
        pygame.display.update()
        clock.tick(60)


def get_size(size):
    if size == 'large':
        return 1000, 600
    elif size == 'medium':
        return  700, 370
    elif size == 'small':
        return  400, 200
#     sizes = [(1000, 600), (700, 370), (400, 200)]


def get_num_color(num):
    """
    根据当前要显示的数字，提取出背景色以及字体颜色
    对应的数字：[方格背景颜色, 方格里的字体颜色]
    """
    color_dict = {
        2: ['#eee4da', '#776e65'], 4: ['#ede0c8', '#776e65'], 8: ['#f2b179', '#f9f6f2'],
        16: ['#f59563', '#f9f6f2'], 32: ['#f67c5f', '#f9f6f2'], 64: ['#f65e3b', '#f9f6f2'],
        128: ['#edcf72', '#f9f6f2'], 256: ['#edcc61', '#f9f6f2'], 512: ['#edc850', '#f9f6f2'],
        1024: ['#edc53f', '#f9f6f2'], 2048: ['#edc22e', '#f9f6f2'], 4096: ['#eee4da', '#776e65'],
        8192: ['#edc22e', '#f9f6f2'], 16384: ['#f2b179', '#776e65'], 32768: ['#f59563', '#776e65'],
        65536: ['#f67c5f', '#f9f6f2'], 0: ['#9e948a', None]
    }
    return color_dict[num]


def create_random_num(nums_temp):
    positions = list()
    print('nums_temp', nums_temp)
    for row, line in enumerate(nums_temp):
        for col, num in enumerate(line):
            if num == 0:
                positions.append((row, col))
    row, col = random.choice(positions)
    nums_temp[row][col] = random.choice([2, 4])
    return nums_temp

def draw_nums(screen, chess_nums_temp, margin_size, block_size, font):
    """
    显示棋盘上的数字
    """
    # 遍历数字
    for i, line in enumerate(chess_nums_temp):
        for j, num in enumerate(line):
            if num != 0:
                # 计算显示位置（x坐标、y坐标）
                x = margin_size * (j + 1) + block_size * j
                y = margin_size * (i + 1) + block_size * i
                # 获取颜色
                font_color = pygame.Color(get_num_color(num)[1])
                # 显示数字
                text = font.render(str(num), True, font_color)
                text_rect = text.get_rect()
                text_rect.centerx, text_rect.centery = int(x + block_size / 2), int(y + block_size / 2)
                # 用对应的数字背景色，重新绘制这个方块
                pygame.draw.rect(screen, pygame.Color(get_num_color(num)[0]), (x, y, block_size, block_size))
                screen.blit(text, text_rect)


def draw_chess_board(screen, margin_size, block_size):
    """
    显示棋盘
    """
    for i in range(4):
        for j in range(4):
            x = margin_size * (j + 1) + block_size * j
            y = margin_size * (i + 1) + block_size * i
            pygame.draw.rect(screen, pygame.Color('#f9f6f2'), (x, y, block_size, block_size))


def draw_next_aistep(screen, x, y, z, n, text, font):
    """
    使用文本框显示单行信息，优化外观
    函数参数 z 直接指定文本框的宽度
    """
    # 定义颜色
    textbox_color = (245, 245, 245)  # 浅灰色背景，比白色柔和一些
    border_color = (100, 100, 100)  # 深灰色边框，增加对比度
    text_color = (240, 30, 30)  # 文本颜色

    # 计算文本框高度，添加一定内边距
    textbox_height = n + 10

    # 绘制文本框
    textbox_rect = pygame.Rect(int(x), int(y), z, textbox_height)
    pygame.draw.rect(screen, textbox_color, textbox_rect)
    pygame.draw.rect(screen, border_color, textbox_rect, 2)

    # 渲染并绘制文本
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(left=x + 15, centery=y + textbox_height // 2)
    screen.blit(text_surface, text_rect)

    print(text)
    return textbox_rect


def get_score(chess_nums_temp):
    """
    计算当前棋盘的总分数
    """

    def sum_all(x, y):
        if isinstance(x, Iterable):
            return sum(x) + sum(y)
        return x + sum(y)

    return reduce(sum_all, chess_nums_temp)



def init_game(width, height, theme, difficulty):
    """
    初始化游戏参数
    """
    margin_size = min(width, height) // 40
    block_size = (min(width, height) - margin_size * 5) // 4
    chess_nums = [[0 for _ in range(4)] for _ in range(4)]
    chess_nums = create_random_num(chess_nums)
    chess_nums = create_random_num(chess_nums)

    difficulty = difficulty

    theme = theme

    judgeandmove = JudgeAndMove(chess_nums, difficulty)

    clock = pygame.time.Clock()
    flag = False
    flag_1 = 0



    score = 0  # get_score(chess_nums)
    ro1 = 0
    button_area_width_ratio = 0.3
    button_width_ratio = 0.4
    button_height_ratio = 0.08
    button_vertical_gap_ratio = 0.03
    button_area_start_x = width * (1 - button_area_width_ratio) - margin_size
    button_start_y = height * 0.25
    button_width = int(width * button_area_width_ratio * button_width_ratio)
    button_height = int(height * button_height_ratio)
    button_vertical_gap = int(height * button_vertical_gap_ratio)
    return margin_size, block_size, chess_nums, judgeandmove, score, difficulty, theme, clock, flag, flag_1, ro1, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap




def calculate_button_area(width, height):
    """
    计算按钮区域的尺寸和位置
    """
    button_area_width_ratio = 0.3
    button_width_ratio = 0.4
    button_height_ratio = 0.08
    button_vertical_gap_ratio = 0.03
    margin_size = min(width, height) // 40
    button_area_start_x = width * (1 - button_area_width_ratio) - margin_size
    button_start_y = height * 0.25
    button_width = int(width * button_area_width_ratio * button_width_ratio)
    button_height = int(height * button_height_ratio)
    button_vertical_gap = int(height * button_vertical_gap_ratio)
    return margin_size, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap



def draw_tips(screen, width, height, x_ratio, y_ratio, width_ratio, height_ratio, text, font_size_ratio):
    """
    显示提示信息
    """
    button_color = (255, 255, 0)  # 按钮颜色：绿色
    x = width * x_ratio
    y = height * y_ratio
    button_width = width * width_ratio
    button_height = height * height_ratio
    button_rect = pygame.Rect(int(x), int(y), button_width, button_height)
    pygame.draw.rect(screen, button_color, button_rect)

    font_size = int(height * font_size_ratio)
    font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect


def draw_score(screen, score, steps, width, height, x_ratio, y_ratio, font_size_ratio):
    """
    显示分数
    """
    font_color = (0, 255, 255)
    score_label_text = 'score:'
    step_label_text = 'step:'

    font_size = int(height * font_size_ratio)
    font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size)

    score_label_width = font.size(score_label_text)[0]
    step_label_width = font.size(step_label_text)[0]
    max_label_width = max(score_label_width, step_label_width)

    score_text = font.render(score_label_text + str(score), True, font_color)
    step_text = font.render(step_label_text + str(steps), True, font_color)

    x = width * x_ratio
    y = height * y_ratio

    score_number_x = x - max_label_width
    step_number_x = x - max_label_width

    screen.blit(score_text, (score_number_x - score_label_width, y))
    screen.blit(step_text, (step_number_x - step_label_width, y + score_text.get_height()))


def draw_game(screen, width, height, difficulty, theme, chess_nums, score, ro1, margin_size, block_size, button_area_start_x,
              button_start_y, button_width, button_height, button_vertical_gap):
    """
    绘制游戏界面
    """
    print('draw_game, width, height,', width, height)
    print('screen_theme', theme)
    screen.fill(pygame.Color(theme))

    margin_size = min(width, height) // 40
    block_size = (min(width, height) - margin_size * 5) // 4

    draw_chess_board(screen, margin_size, block_size)

    font_size = block_size - 25
    font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size)
    draw_nums(screen, chess_nums, margin_size, block_size, font)
    score_font_size_ratio = 0.08

    # 调整 score 显示的 x 比例，让文字更靠右
    score_x_ratio = 0.99
    score_y_ratio = 0.02

    draw_score(screen, score, ro1, width, height, score_x_ratio, score_y_ratio, score_font_size_ratio)

    # 调整按钮区域宽度比例，避免与右边边界重合
    button_area_width_ratio = 0.2  # 减小按钮区域宽度比例
    button_width_ratio = 0.8  # 按钮宽度占按钮区域宽度的比例
    button_height_ratio = 0.08
    button_vertical_gap_ratio = 0.03
    button_area_start_x = width * (1 - button_area_width_ratio) - margin_size
    button_start_y = height * 0.25
    button_width = int(width * button_area_width_ratio * button_width_ratio)
    button_height = int(height * button_height_ratio)
    button_vertical_gap = int(height * button_vertical_gap_ratio)

    tip_font_size_ratio = button_height_ratio * 0.6
    button_labels = ['ai_automatic', 'Smart Tips', 'setting', 'gameModel']
    for i, label in enumerate(button_labels):
        y_ratio = (button_start_y + i * (button_height + button_vertical_gap)) / height
        draw_tips(screen, width, height, (button_area_start_x / width), y_ratio,
                  button_width_ratio * button_area_width_ratio, button_height_ratio, label, tip_font_size_ratio)

    print('final draw')



def handle_ai(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size, button_area_start_x,
              button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, username):
    """
    处理 AI 逻辑
    """
    if flag and flag_1 == 1:
        try:
            ai1, ai2, ai3, text = analyze_moves(chess_nums)
            old_chess_nums = [row[:] for row in chess_nums]
            chess_nums = judgeandmove.move(ai1)
            if chess_nums != old_chess_nums:
                ro1 += 1
            time.sleep(0.5)
            score = get_score(chess_nums)
        except:
            if judgeandmove.judge_game_over():
                print("Game over")
                score = get_score(chess_nums)
                with open('fs.txt', 'a') as f:
                    f.write(f'{username}:{score}')
                return score, width, height, difficulty, theme, None, None, None, None, None, None, None, None, None, None, None
    return score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1






def handle_smart_tips(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size, button_area_start_x,
                      button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, username):
    """
    处理 smart tips 逻辑
    """
    print('flag, flag_1:',flag, flag_1)
    if flag and flag_1 == 2:
        try:
            move_probs_dict  = rl_analyze_moves(chess_nums) #analyze_moves(chess_nums)
            print('chess_nums:', chess_nums)
            print('move_probs_dict:', move_probs_dict)
            move_probs_dict = {key: round(float(value), 2) for key, value in move_probs_dict.items()}

            tip_font_size = int(button_height * 0.6)
            tip_font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", tip_font_size)
            #draw_next_aistep(screen, button_area_start_x*0.95, button_start_y + 4 * (button_height + button_vertical_gap), button_width*1.4  + margin_size, button_height*0.9, text[0], tip_font)
            #draw_next_aistep(screen, button_area_start_x*0.95, button_start_y + 5 * (button_height + button_vertical_gap), button_width*1.4  + margin_size, button_height*0.9, text[1], tip_font)
            #draw_next_aistep(screen, button_area_start_x*0.95, button_start_y + 6 * (button_height + button_vertical_gap), button_width*1.4  + margin_size, button_height*0.9, text[2], tip_font)
            move = 'up'
            prob = move_probs_dict.get('up', 0)
            prob_text = f"{move}: {prob * 100:.2f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.95,
                             button_start_y + (4 + 0) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.2 + margin_size, button_height * 0.5, prob_text, tip_font)

            # 处理 'down'
            move = 'down'
            prob = move_probs_dict.get('down', 0)
            prob_text = f"{move}: {prob * 100:.2f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.95,
                             button_start_y + (4 + 0.8) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.2 + margin_size, button_height * 0.5, prob_text, tip_font)

            # 处理 'left'
            move = 'left'
            prob = move_probs_dict.get('left', 0)
            prob_text = f"{move}: {prob * 100:.2f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.95,
                             button_start_y + (4 + 1.6) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.2 + margin_size, button_height * 0.5, prob_text, tip_font)

            # 处理 'right'
            move = 'right'
            prob = move_probs_dict.get('right', 0)
            prob_text = f"{move}: {prob * 100:.2f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.95,
                             button_start_y + (4 + 2.4) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.2 + margin_size, button_height * 0.5, prob_text, tip_font)

            score = get_score(chess_nums)
        except:
            if judgeandmove.judge_game_over():
                print("Game over")
                score = get_score(chess_nums)
                with open('fs.txt', 'a') as f:
                    f.write(f'{username}:{score}')
                return score, width, height, difficulty, theme, None, None, None, None, None, None, None, None, None, None, None
    return score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1


def handle_setting(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size, button_area_start_x,
                   button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, username):
    """
    处理 setting 设置
    """
    if flag and flag_1 == 3:
        new_width, new_height, current_background, current_size, current_difficulty = show_settings(screen, width, height,theme)

        print('current_background:', current_background)
        print('current_size:', current_size)
        print('current_difficulty:', current_difficulty)
        print('judgeandmove:', judgeandmove.difficulty)
        # current_background: (240, 240, 240)
        # current_size: 中
        # current_difficulty: 普通

        #theme = get_theme(current_background)
        print('theme_color', theme)
        theme = current_background
        difficulty = current_difficulty
        # 如果窗口大小改变，重新计算依赖于窗口大小的参数
        print('theme_color2', theme)

        new_width, new_height = get_size(current_size)

        if new_width != width or new_height != height:
            width = new_width
            height = new_height
            margin_size = min(width, height) // 40
            block_size = (min(width, height) - margin_size * 5) // 4
            button_area_width_ratio = 0.3
            button_width_ratio = 0.4
            button_height_ratio = 0.08
            button_vertical_gap_ratio = 0.03
            button_area_start_x = width * (1 - button_area_width_ratio) - margin_size
            button_start_y = height * 0.25
            button_width = int(width * button_area_width_ratio * button_width_ratio)
            button_height = int(height * button_height_ratio)
            button_vertical_gap = int(height * button_vertical_gap_ratio)

        flag = False  # 关闭设置界面后重置标志
        flag_1 = 0
        judgeandmove = JudgeAndMove(chess_nums, difficulty)
        screen = pygame.display.set_mode((width, height))

    return score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, \
           button_width, button_height, button_vertical_gap, flag, flag_1






def handle_events(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size, button_area_start_x,
                  button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, username):
    """
    处理游戏事件
    """
    button_area_width_ratio = 0.2
    button_width_ratio = 0.8
    button_height_ratio = 0.08
    button_vertical_gap_ratio = 0.03
    tip_font_size_ratio = button_height_ratio * 0.6
    button_labels = ['ai_automatic', 'Smart Tips', 'setting', 'gameModel']

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            margin_size = min(width, height) // 40
            block_size = (min(width, height) - margin_size * 5) // 4

            button_area_start_x = width * (1 - button_area_width_ratio) - margin_size
            button_start_y = height * 0.25
            button_width = int(width * button_area_width_ratio * button_width_ratio)
            button_height = int(height * button_height_ratio)
            button_vertical_gap = int(height * button_vertical_gap_ratio)

            score_font_size_ratio = 0.08
            score_x_ratio = 0.99
            score_y_ratio = 0.02
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                flag = False
                direction = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[
                    event.key]
                old_chess_nums = [row[:] for row in chess_nums]
                chess_nums = judgeandmove.move(direction)
                if chess_nums != old_chess_nums:
                    ro1 += 1
                if judgeandmove.judge_game_over():
                    with open('fs.txt', 'a') as f:
                        f.write(f'{username}:{score}\n')
                    print("Game over")
                    return score, width, height, difficulty, theme, None, None, None, None, None, None, None, None, None, None, None, None
                score = get_score(chess_nums)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, label in enumerate(button_labels):
                button_area_start_x = width * (1 - button_area_width_ratio) - margin_size
                button_start_y = height * 0.25
                button_width = int(width * button_area_width_ratio * button_width_ratio)
                button_height = int(height * button_height_ratio)
                button_vertical_gap = int(height * button_vertical_gap_ratio)
                y_ratio = (button_start_y + i * (button_height + button_vertical_gap)) / height
                button_rect = draw_tips(screen, width, height, (button_area_start_x / width), y_ratio,
                                        button_width_ratio * button_area_width_ratio, button_height_ratio, label,
                                        tip_font_size_ratio)
                if button_rect.collidepoint(mouse_pos):
                    flag = True
                    flag_1 = i + 1

    return score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1






def run(screen, width, height, username, theme, difficulty, game_model):
    """
    运行游戏
    """
    pygame.display.set_caption("2048_single_game")

    margin_size, block_size, chess_nums, judgeandmove, score, difficulty, theme, clock, flag, flag_1, ro1, \
    button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap = init_game(width, height, theme, difficulty)

    #print('width, height, margin_size, button_width, button_height:', width, height)
    draw_game(screen, width, height, difficulty, theme, chess_nums, score, ro1, margin_size, block_size, button_area_start_x,
              button_start_y, button_width, button_height, button_vertical_gap)
    #print('width, height, margin_size, button_width, button_height:', width, height, difficulty)
    while True:
        draw_game(screen, width, height, difficulty, theme, chess_nums, score, ro1, margin_size, block_size, button_area_start_x,
                  button_start_y, button_width, button_height, button_vertical_gap)
        result = handle_events(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size,
                               button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap,
                               flag, flag_1, username)
        if result[0] is not None and result[8] is None:
            return result[0], width, height, theme, difficulty, game_model

        score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, \
        button_width, button_height, button_vertical_gap, flag, flag_1 = result


        result = handle_setting(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size,
                                button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap,
                                flag, flag_1, username)
        score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, \
        button_width, button_height, button_vertical_gap, flag, flag_1 = result

        print('handle_setting  width, height, margin_size, theme, difficulty,button_width, button_height:', width, height, margin_size, theme,
              difficulty, button_width, button_height, flag, flag_1)

        if flag and flag_1 == 1:
            result = handle_ai(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size,
                               button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap,
                               flag, flag_1, username)
        elif flag_1 == 2:
            result = handle_smart_tips(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size,
                                       button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap,
                                       flag, flag_1, username)
        #else:
        #    result = (score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y,
        #              button_width, button_height, button_vertical_gap, flag, flag_1)

        if result[0] is not None and result[8] is None:
            return result[0], width, height, theme, difficulty, game_model

        score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, \
        button_width, button_height, button_vertical_gap, flag, flag_1 = result

        print('width, height, margin_size, button_width, button_height:', width, height, margin_size)

        if flag and flag_1 == 4:
            game_model = 'double'
            return result[0], width, height, theme, difficulty, game_model


        pygame.display.update()
        pygame.display.flip()
        clock.tick(30)













def handle_double_player_input(chess_nums1, judgeandmove1, score1, step1, chess_nums2, judgeandmove2, score2, step2, event, username):
    """处理双人游戏的按键输入事件"""
    if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
        direction = {pygame.K_w: 'up', pygame.K_s: 'down', pygame.K_a: 'left', pygame.K_d: 'right'}[event.key]
        old_chess_nums = [row[:] for row in chess_nums1]
        chess_nums1 = judgeandmove1.move(direction)
        if chess_nums1 != old_chess_nums:
            step1 += 1
        if judgeandmove1.judge_game_over():
            with open('fs.txt', 'a') as f:
                f.write(f'{username} (Player 1):{score1}\n')
            print("Player 1 Game over")
        score1 = get_score(chess_nums1)
    elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
        direction = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[event.key]
        old_chess_nums = [row[:] for row in chess_nums2]
        chess_nums2 = judgeandmove2.move(direction)
        if chess_nums2 != old_chess_nums:
            step2 += 1
        if judgeandmove2.judge_game_over():
            with open('fs_double.txt', 'a') as f:
                f.write(f'{username} (Player 2):{score2}\n')
            print("Player 2 Game over")
        score2 = get_score(chess_nums2)
    return score1, chess_nums1, judgeandmove1, step1, score2, chess_nums2, judgeandmove2, step2



def handle_quit_event():
    """处理退出事件"""
    pygame.quit()
    sys.exit()




def init_double_player_game(width, height, theme, difficulty):
    margin_size = min(width, height) // 60
    block_size = (min(width, height) - margin_size * 15) // 12

    chess_nums1 = [[0] * 4 for _ in range(4)]
    chess_nums1 = create_random_num(chess_nums1)
    chess_nums1 = create_random_num(chess_nums1)
    judgeandmove1 = JudgeAndMove(chess_nums1, difficulty)  # 这里应该是处理移动和判断的对象，需要具体实现
    score1 = 0
    step1 = 0


    chess_nums2 = [[0] * 4 for _ in range(4)]
    chess_nums2 = create_random_num(chess_nums2)
    chess_nums2 = create_random_num(chess_nums2)
    judgeandmove2 = JudgeAndMove(chess_nums2, difficulty)
    score2 = 0
    step2 = 0

    difficulty = difficulty

    theme = theme


    clock = pygame.time.Clock()
    flag = False
    flag_1 = 0
    flag_2 = 0
    button_area_width_ratio = 0.2
    button_area_start_x = width * (1 - button_area_width_ratio) - margin_size
    button_start_y = height * 0.25
    button_width_ratio = 0.8
    button_width = int(width * button_area_width_ratio * button_width_ratio)
    button_height_ratio = 0.08
    button_height = int(height * button_height_ratio)
    button_vertical_gap_ratio = 0.03
    button_vertical_gap = int(height * button_vertical_gap_ratio)

    return margin_size, block_size, chess_nums1, judgeandmove1, score1, step1, \
           chess_nums2, judgeandmove2, score2, step2, \
           difficulty, theme, clock, flag, flag_1, flag_2, \
           button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap


def draw_double_score(screen, score, step, x, y, score_font_size):
    score_font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", score_font_size)
    score_text = score_font.render(f'Score:{score}', True, pygame.Color('#776e65'))
    ro1_text = score_font.render(f'Steps:{step}', True, pygame.Color('#776e65'))
    screen.blit(score_text, (x, y))
    screen.blit(ro1_text, (x, y + score_font_size + 5))


def draw_double_chess_board(screen, x_offset, margin_size, block_size):
    """
    显示棋盘
    """
    for i in range(4):
        for j in range(4):
            x = x_offset + margin_size * (j + 1) + block_size * j
            y = margin_size * (i + 1) + block_size * i
            pygame.draw.rect(screen, pygame.Color('#f9f6f2'), (x, y, block_size, block_size))


def draw_double_nums(screen, chess_nums, x_offset, margin_size, block_size, font):
    """
    显示棋盘上的数字
    """
    # 遍历数字
    for i, line in enumerate(chess_nums):
        for j, num in enumerate(line):
            if num != 0:
                # 计算显示位置（x坐标、y坐标）
                x = x_offset + margin_size * (j + 1) + block_size * j
                y = margin_size * (i + 1) + block_size * i
                # 获取颜色
                font_color = pygame.Color(get_num_color(num)[1])
                # 显示数字
                text = font.render(str(num), True, font_color)
                text_rect = text.get_rect()
                text_rect.centerx, text_rect.centery = int(x + block_size / 2), int(y + block_size / 2)
                # 用对应的数字背景色，重新绘制这个方块
                pygame.draw.rect(screen, pygame.Color(get_num_color(num)[0]), (x, y, block_size, block_size))
                screen.blit(text, text_rect)



def draw_double_tips(screen, button_x, button_y, button_width, button_height, label):
    """
    绘制双人游戏操作按钮
    """
    # 使用单人游戏中的按钮颜色设置
    DEFAULT_BUTTON_COLOR = '#0080ff'
    TEXT_COLOR = '#ffccff'

    button_color = pygame.Color(DEFAULT_BUTTON_COLOR)
    text_color = pygame.Color(TEXT_COLOR)

    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, button_color, button_rect)

    # 设置字体大小，这里简单根据按钮高度设置
    tip_font_size = int(button_height * 0.6)
    tip_font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", tip_font_size)
    tip_text = tip_font.render(label, True, text_color)
    tip_text_rect = tip_text.get_rect(center=button_rect.center)
    screen.blit(tip_text, tip_text_rect)

    return button_rect






def handle_setting(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size, button_area_start_x,
                   button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, username):
    """
    处理 setting 设置
    """
    if flag and flag_1 == 3:
        new_width, new_height, current_background, current_size, current_difficulty = show_settings(screen, width, height,theme)

        print('current_background:', current_background)
        print('current_size:', current_size)
        print('current_difficulty:', current_difficulty)
        print('judgeandmove:', judgeandmove.difficulty)
        # current_background: (240, 240, 240)
        # current_size: 中
        # current_difficulty: 普通

        #theme = get_theme(current_background)
        print('theme_color', theme)
        theme = current_background
        difficulty = current_difficulty
        # 如果窗口大小改变，重新计算依赖于窗口大小的参数
        print('theme_color2', theme)

        new_width, new_height = get_size(current_size)

        if new_width != width or new_height != height:
            width = new_width
            height = new_height
            margin_size = min(width, height) // 40
            block_size = (min(width, height) - margin_size * 5) // 4
            button_area_width_ratio = 0.3
            button_width_ratio = 0.4
            button_height_ratio = 0.08
            button_vertical_gap_ratio = 0.03
            button_area_start_x = width * (1 - button_area_width_ratio) - margin_size
            button_start_y = height * 0.25
            button_width = int(width * button_area_width_ratio * button_width_ratio)
            button_height = int(height * button_height_ratio)
            button_vertical_gap = int(height * button_vertical_gap_ratio)

        flag = False  # 关闭设置界面后重置标志
        flag_1 = 0
        judgeandmove = JudgeAndMove(chess_nums, difficulty)
        screen = pygame.display.set_mode((width, height))

    return score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, \
           button_width, button_height, button_vertical_gap, flag, flag_1

def draw_double_game(screen, width, height, theme, chess_nums1, chess_nums2, score1, score2, step1, step2, margin_size,block_size):
    """
    绘制双人游戏界面
    """
    # 将十六进制主题颜色转换为 RGB 格式
    bg_rgb = tuple(int(theme.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    screen.fill(bg_rgb)

    margin_size = min(width, height) // 60
    block_size = (max(width, height)- margin_size * 14) // 10

    # 计算棋盘和分数显示区域的宽度
    board_width = block_size * 4 + margin_size * 5
    score_width = width // 6  # 分数显示区域宽度为窗口宽度的四分之一

    # 绘制玩家 1 的棋盘及相关信息
    left_x = margin_size
    draw_double_chess_board(screen, left_x, margin_size, block_size)
    font_size = block_size - 28
    font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size)
    draw_double_nums(screen, chess_nums1, left_x, margin_size, block_size, font)
    score_x = left_x + board_width + margin_size
    score_y =  font_size*0.5
    score_font_size = int(font_size // 2.2)
    draw_double_score(screen, score1, step1, score_x, score_y, score_font_size)

    # 绘制玩家 2 的棋盘及相关信息
    right_x = width * 0.5 + margin_size
    draw_double_chess_board(screen, right_x, margin_size, block_size)
    draw_double_nums(screen, chess_nums2, right_x, margin_size, block_size, font)
    score_x = right_x + board_width + margin_size*0.5
    draw_double_score(screen, score2, step2, score_x, score_y, score_font_size)

    # 计算分数显示区域的总高度，假设分数和步数信息共占两行文字高度加一些间距
    score_area_height = score_font_size * 2.5

    # 绘制操作按钮
    button_vertical_gap_ratio = 0.03
    button_width = 0.95 * block_size
    button_height = 0.4 * block_size


    button_vertical_gap = margin_size*1.2  # 按钮垂直间距，使用固定值

    button_area_start_x = score_x
    # 将按钮起始纵坐标调整到分数显示区域下方
    button_start_y = score_y + score_area_height

    button_labels = ['AI', 'setting', 'gameModel']
    #print('button_area_start_x, current_button_y, button_width, button_height:', button_area_start_x, button_start_y,
          #button_width, button_height)
    for i, label in enumerate(button_labels):
        if i == 0 or i == 2:
            current_button_y = button_start_y + i * (button_height + button_vertical_gap)
            print('button_area_start_x, current_button_y, button_width, button_height:',
                  button_area_start_x, current_button_y, button_width, button_height)
            draw_double_tips(screen, button_area_start_x, current_button_y, button_width, button_height, label)
            print('margin_size, ')
        else:
            continue
    return margin_size, button_area_start_x,button_start_y, button_width, button_height, button_vertical_gap


def handle_double_smart_tips(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size, button_area_start_x,
                      button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, flag_2, username):
    """
    处理 smart tips 逻辑
    """
    try:
        move_probs_dict = rl_analyze_moves(chess_nums)  # analyze_moves(chess_nums)
        print('chess_nums:', chess_nums)
        print('move_probs_dict:', move_probs_dict)
        move_probs_dict = {key: round(float(value), 2) for key, value in move_probs_dict.items()}

        tip_font_size = int(button_height * 0.5)
        tip_font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", tip_font_size)

        if flag_1 == 5:
            move = 'up'
            prob = move_probs_dict.get('up', 0)
            prob_text = f"{move}:{prob * 100:.1f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.44,
                             button_start_y + (4 + 0) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.2 + margin_size, button_height * 0.5, prob_text, tip_font)
            # 处理 'down'
            move = 'down'
            prob = move_probs_dict.get('down', 0)
            prob_text = f"{move}:{prob * 100:.1f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.44,
                             button_start_y + (4 + 0.8) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.2 + margin_size, button_height * 0.5, prob_text, tip_font)

            # 处理 'left'
            move = 'left'
            prob = move_probs_dict.get('left', 0)
            prob_text = f"{move}:{prob * 100:.1f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.44,
                             button_start_y + (4 + 1.6) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.2 + margin_size, button_height * 0.5, prob_text, tip_font)

            # 处理 'right'
            move = 'right'
            prob = move_probs_dict.get('right', 0)
            prob_text = f"{move}:{prob * 100:.1f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.44,
                             button_start_y + (4 + 2.4) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.2 + margin_size, button_height * 0.5, prob_text, tip_font)


            score = get_score(chess_nums)
        if flag_2 == 5:
            move = 'up'
            prob = move_probs_dict.get('up', 0)
            prob_text = f"{move}:{prob * 100:.1f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.99,
                             button_start_y + (4 + 0) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.11 + margin_size, button_height * 0.5, prob_text, tip_font)
            # 处理 'down'
            move = 'down'
            prob = move_probs_dict.get('down', 0)
            prob_text = f"{move}:{prob * 100:.1f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.99,
                             button_start_y + (4 + 0.8) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.11 + margin_size, button_height * 0.5, prob_text, tip_font)

            # 处理 'left'
            move = 'left'
            prob = move_probs_dict.get('left', 0)
            prob_text = f"{move}:{prob * 100:.1f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.99,
                             button_start_y + (4 + 1.6) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.11 + margin_size, button_height * 0.5, prob_text, tip_font)

            # 处理 'right'
            move = 'right'
            prob = move_probs_dict.get('right', 0)
            prob_text = f"{move}:{prob * 100:.1f}%"
            print('prob_text:', prob_text)
            draw_next_aistep(screen, button_area_start_x * 0.99,
                             button_start_y + (4 + 2.4) * (button_height + button_vertical_gap * 0.8),
                             button_width * 1.11 + margin_size, button_height * 0.5, prob_text, tip_font)

            score = get_score(chess_nums)
    except:
        if judgeandmove.judge_game_over():
            print("Game over")
            score = get_score(chess_nums)
            with open('fs.txt', 'a') as f:
                f.write(f'{username}:{score}')




def handle_double_even(screen, width, height, difficulty, theme, chess_nums1, judgeandmove1, score1, step1,
                       chess_nums2, judgeandmove2, score2, step2, margin_size, button_area_start_x,
                       button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, flag_2, username):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:

            width, height = event.size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            # 处理玩家 1 的输入
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]  and flag_1 != 22:
                flag_1 = 0
                direction = {pygame.K_w: 'up', pygame.K_s: 'down', pygame.K_a: 'left', pygame.K_d: 'right'}[event.key]
                old_chess_nums = [row[:] for row in chess_nums1]
                chess_nums1 = judgeandmove1.move(direction)
                if chess_nums1 != old_chess_nums:
                    step1 += 1
                if judgeandmove1.judge_game_over():
                    with open('fs.txt', 'a') as f:
                        f.write(f'{username} (Player 1):{score1}\n')
                    print("Player 1 Game over")
                    flag_1 = 22
                    return score1, step1, chess_nums1, score2, step2,chess_nums2, width, height, difficulty, theme, flag_1, flag_2, None, None, None, None, None, None, None, None, None, None
                score1 = get_score(chess_nums1)
            # 处理玩家 2 的输入
            elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] and flag_2 != 22:
                flag_2 = 0
                direction = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[
                    event.key]
                old_chess_nums = [row[:] for row in chess_nums2]
                chess_nums2 = judgeandmove2.move(direction)
                if chess_nums2 != old_chess_nums:
                    step2 += 1
                if judgeandmove2.judge_game_over():
                    with open('fs.txt', 'a') as f:
                        f.write(f'{username} (Player 2):{score2}\n')
                    print("Player 2 Game over")
                    flag_2 = 22
                    print('chess_nums2:', chess_nums2)
                    return score1, step1, chess_nums1, score2, step2,chess_nums2, width, height, difficulty, theme, flag_1, flag_2, None, None, None, None, None, None, None, None, None, None, None, None
                score2 = get_score(chess_nums2)
                # 玩家 1 按 q 键显示提示
            elif event.key == pygame.K_q:
                print('pygame.K_q')
                flag = True
                flag_1 = 5
            # 玩家 2 按 0 键显示提示
            elif event.key == pygame.K_0:
                print('pygame.K_0')
                flag = True
                flag_2 = 5

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            button_labels = ['AI', 'setting', 'gameModel']
            for i, label in enumerate(button_labels):
                current_button_y = button_start_y + i * (button_height + button_vertical_gap)
                button_rect = pygame.Rect(button_area_start_x, current_button_y, button_width, button_height)

                if button_rect.collidepoint(mouse_x, mouse_y):
                    if label == 'AI':
                        #score1, score2, width, height, difficulty, theme, chess_nums1, judgeandmove1, step1, chess_nums2, judgeandmove2, step2, margin_size, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1 = result
                        flag = True
                        flag_1 = 3
                        print('mouse_x, mouse_y:', mouse_x, mouse_y, label)
                    elif label == 'setting':
                        print('mouse_x, mouse_y:', mouse_x, mouse_y, label)

                        #score1, score2, width, height, difficulty, theme, chess_nums1, judgeandmove1, step1, chess_nums2, judgeandmove2, step2, margin_size, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1 = result
                    elif label == 'gameModel':
                        flag = True
                        flag_1 = 4
                        print('mouse_x, mouse_y:', mouse_x, mouse_y, label)
    return score1, score2, width, height, difficulty, theme, chess_nums1, judgeandmove1, step1, chess_nums2, judgeandmove2, step2, margin_size, \
           button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1,flag_2


def handle_double_ai(screen, width, height, difficulty, theme, chess_nums, judgeandmove, score, ro1, margin_size, button_area_start_x,
              button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, username):
    """
    处理 AI 逻辑
    """
    try:
        ai1, ai2, ai3, text = analyze_moves(chess_nums)
        old_chess_nums = [row[:] for row in chess_nums]
        chess_nums = judgeandmove.move(ai1)
        if chess_nums != old_chess_nums:
            ro1 += 1
        time.sleep(0.5)
        score = get_score(chess_nums)
    except:
        if judgeandmove.judge_game_over():
            print("Game over")
            score = get_score(chess_nums)
            flag_2 = 22
            with open('fs.txt', 'a') as f:
                f.write(f'{username}:{score}')
                #return score, width, height, difficulty, theme, None, None, None, None, None, None, None, None, None, None, None
            return score, ro1, chess_nums, width, height, difficulty, theme, flag_2, None, None, None, None, None, None, None, None, None, None, None
    return score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1



def draw_one_game_over(screen, score, step, left_x, margin_size, block_size):
    """
    在玩家一游戏结束后，在对应的棋盘处用红色文字显示最终的分数和步数
    :param screen: pygame 的屏幕对象
    :param score1: 玩家一的最终分数
    :param step1: 玩家一的步数
    :param left_x: 玩家一棋盘的左边界 x 坐标
    :param margin_size: 棋盘的边距大小
    :param block_size: 棋盘每个格子的大小
    """
    # 设置字体
    font_size = int(block_size * 2)  # 字体大小根据格子大小调整
    font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size)

    # 计算显示文字的位置
    text_x = left_x + margin_size
    text_y = margin_size * 2  # 从棋盘上方一定距离开始显示

    # 准备要显示的文字
    score_text = f"score: {score}"
    steps_text = f"step: {step}"

    # 渲染文字
    score_surface = font.render(score_text, True, (255, 0, 0))  # 红色文字
    steps_surface = font.render(steps_text, True, (255, 0, 0))

    # 在屏幕上绘制文字
    screen.blit(score_surface, (text_x, text_y))
    text_y += font_size + margin_size  # 向下移动一定距离显示下一行文字
    screen.blit(steps_surface, (text_x, text_y))

def show_double_game_over(screen, score, width, height, theme, player):
    # 动态计算字体大小
    font_size_big = int(height * 0.1)
    font_size_small = int(height * 0.05)
    font_color = (255, 255, 255)
    font_big = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_big)
    font_small = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_small)
    surface = screen.convert_alpha()
    surface.fill((0, 0, 0, 2))
    text1 = font_big.render(f'{score}', True, (0, 255, 0))
    text_rect1 = text1.get_rect()
    text_rect1.centerx, text_rect1.centery = width // 2, height // 2 - int(height * 0.15)
    surface.blit(text1, text_rect1)
    text = font_big.render(f'{player} WIN !', True, font_color)
    text_rect = text.get_rect()
    text_rect.centerx, text_rect.centery = width // 2, height // 2 - int(height * 0.07)
    surface.blit(text, text_rect)
    # 动态计算按钮大小和位置
    button_width = int(width * 0.15)
    button_height = int(height * 0.07)
    button_start_x_left = width // 2 - button_width - int(width * 0.03)
    button_start_x_right = width // 2 + int(width * 0.03)
    button_start_y = height // 2 - button_height // 2 + int(height * 0.03)
    pygame.draw.rect(surface, (0, 255, 255), (button_start_x_left, button_start_y, button_width, button_height))
    text_restart = font_small.render('Restart', True, (0, 33, 66))
    text_restart_rect = text_restart.get_rect()
    text_restart_rect.centerx, text_restart_rect.centery = button_start_x_left + button_width // 2, button_start_y + button_height // 2
    surface.blit(text_restart, text_restart_rect)
    pygame.draw.rect(surface, (0, 255, 255), (button_start_x_right, button_start_y, button_width, button_height))
    text_quit = font_small.render('Quit', True, (0, 33, 66))
    text_quit_rect = text_quit.get_rect()
    text_quit_rect.centerx, text_quit_rect.centery = button_start_x_right + button_width // 2, button_start_y + button_height // 2
    surface.blit(text_quit, text_quit_rect)
    clock = pygame.time.Clock()
    while True:
        screen.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                # 重新计算字体大小
                font_size_big = int(height * 0.1)
                font_size_small = int(height * 0.05)
                font_big = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_big)
                font_small = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_small)
                surface = screen.convert_alpha()
                surface.fill((0, 0, 0, 2))

                # 重新绘制得分
                text1 = font_big.render(f'{score}', True, (0, 255, 0))
                text_rect1 = text1.get_rect()
                text_rect1.centerx, text_rect1.centery = width // 2, height // 2 - int(height * 0.15)
                surface.blit(text1, text_rect1)

                # 重新绘制 Game Over 文本
                text = font_big.render(f'{player}', True, font_color)
                text_rect = text.get_rect()
                text_rect.centerx, text_rect.centery = width // 2, height // 2 - int(height * 0.07)
                surface.blit(text, text_rect)

                # 重新计算按钮大小和位置
                button_width = int(width * 0.15)
                button_height = int(height * 0.07)
                button_start_x_left = width // 2 - button_width - int(width * 0.03)
                button_start_x_right = width // 2 + int(width * 0.03)
                button_start_y = height // 2 - button_height // 2 + int(height * 0.03)

                pygame.draw.rect(surface, (0, 255, 255),
                                 (button_start_x_left, button_start_y, button_width, button_height))
                text_restart = font_small.render('Restart', True, (0, 33, 66))
                text_restart_rect = text_restart.get_rect()
                text_restart_rect.centerx, text_restart_rect.centery = button_start_x_left + button_width // 2, button_start_y + button_height // 2
                surface.blit(text_restart, text_restart_rect)

                pygame.draw.rect(surface, (0, 255, 255),
                                 (button_start_x_right, button_start_y, button_width, button_height))
                text_quit = font_small.render('Quit', True, (0, 33, 66))
                text_quit_rect = text_quit.get_rect()
                text_quit_rect.centerx, text_quit_rect.centery = button_start_x_right + button_width // 2, button_start_y + button_height // 2
                surface.blit(text_quit, text_quit_rect)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                if text_quit_rect.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()
                if text_restart_rect.collidepoint(pygame.mouse.get_pos()):
                    return True, width, height, theme
        pygame.display.update()
        clock.tick(60)

def run_double_player_game(screen, width, height, username, theme, difficulty, game_model):
    pygame.display.set_caption("2048_double_game")

    margin_size, block_size, chess_nums1, judgeandmove1, score1, step1, \
    chess_nums2, judgeandmove2, score2, step2, \
    difficulty, theme, clock, flag, flag_1, flag_2,\
    button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap = init_double_player_game(width, height, theme, difficulty)

    while True:
        margin_size, button_area_start_x,button_start_y, button_width, button_height, button_vertical_gap = draw_double_game(screen, width, height, theme,
                                                                                                                             chess_nums1, chess_nums2, score1,
                                                                                                                             score2, step1, step2, margin_size,
                                                                                                                             block_size)

        result = handle_double_even(screen, width, height, difficulty, theme, chess_nums1, judgeandmove1, score1, step1,
                               chess_nums2, judgeandmove2, score2, step2, margin_size, button_area_start_x,
                               button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, flag_2, username)
        print('result:', result)

        if result[0] is not None and result[15] is None:#玩家一游戏结束
            #score1, width, height, difficulty, theme, flag_1 = result[0:6]
            #return score1, step1, chess_nums1, width, height, difficulty, theme, flag_1, flag_2, None, None, None, None, None, None, None, None, None, None
            flag_1 = result[10]
            flag_2 = result[11]
            #return score1, step1, chess_nums1, score2, step2, chess_nums2, width, height, difficulty, theme, flag_1, flag_2, None, None, None, None, None, None, None, None, None, None, None, None

            if flag_1 == 22 and flag_2 == 22:
                score1, step1, chess_nums1, score2, step2, chess_nums2 = result[0:6]
                if score1 > score2:
                    player = 'Player1 win'
                    print('player1:', player)
                    return score1, width, height, theme, difficulty, game_model, player

                elif score2 > score1:
                    player = 'Player2'
                    return score2, width, height, theme, difficulty, game_model, player
                else:
                    # 分数相同，比较步数
                    if step1 < step2:
                        print( "玩家 1 获胜")
                        player = 'Player1'
                        return score1, width, height, theme, difficulty, game_model, player
                    elif step2 < step1:
                        print("玩家 2 获胜")
                        player = 'Player2'
                        return score2, width, height, theme, difficulty, game_model, player
                    else:
                        player = 'score draw'
                        print("平局")
                        return score2, width, height, theme, difficulty, game_model, player
            elif flag_1 == 22 and flag_2 != 22:
                score1, step1, chess_nums1, score2, step2, chess_nums2, width, height, difficulty, theme, flag_1, flag_2 = result[0:12]
                print('draw_one_game_over(screen, score2, step2, width * 0.1, margin_size, block_size)', score1, step1,
                      width * 0.7)
                draw_one_game_over(screen, score1, step1, width * 0.1, margin_size, block_size)

            elif flag_1 != 22 and flag_2 == 22:
                score1, step1, chess_nums1, score2, step2, chess_nums2, width, height, difficulty, theme, flag_1, flag_2 = result[0:12]
                print('draw_one_game_over(screen, score2, step2, width * 0.7, margin_size, block_size)', score2, step2,
                      width * 0.7)
                draw_one_game_over(screen, score2, step2, width * 0.55, margin_size, block_size)
        else:
            score1, score2, width, height, difficulty, theme, chess_nums1, judgeandmove1, step1, chess_nums2, judgeandmove2, step2, \
        margin_size, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, flag_2 = result
        #score1, score2, width, height, difficulty, theme, chess_nums1, judgeandmove1, step1, chess_nums2, judgeandmove2, step2, margin_size, \
        #button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1, flag_2


        if flag_1 == 22 and flag_2 != 22；
            print('123123kkkkkkkkkkkkk')
            print('draw_one_game_over(screen, score2, step2, width * 0.7, margin_size, block_size)', score1, step1,
                  width * 0.7)
            draw_one_game_over(screen, score1, step1, width * 0.1, margin_size, block_size)
        if flag_1 != 22 and flag_2 == 22:
            print('22222222222222222pppppppppppppp')
            print('draw_one_game_over(screen, score2, step2, width * 0.7, margin_size, block_size)', score2, step2,
                  width * 0.7)
            draw_one_game_over(screen, score2, step2, width * 0.55, margin_size, block_size)




        print(' flag, flag_1 flag_2:',  flag, flag_1, flag_2)
        if flag  and  flag_1 == 5:
            print('flag  and  flag_1 == 5')
            handle_double_smart_tips(screen, width, height, difficulty, theme, chess_nums1, judgeandmove1, score1,
                                       step1, margin_size, button_area_start_x,
                                       button_start_y, button_width, button_height, button_vertical_gap, flag,
                                       flag_1, flag_2, username)
        elif flag  and  flag_2 == 5 :
            print('flag  and  flag_2 == 5')
            handle_double_smart_tips(screen, width, height, difficulty, theme, chess_nums2, judgeandmove2, score2,
                                       step2, margin_size, button_area_start_x,
                                       button_start_y, button_width, button_height, button_vertical_gap, flag,
                                       flag_1, flag_2, username)

        if flag and flag_1 == 3:
            ai_result = handle_double_ai(screen, width, height, difficulty, theme, chess_nums2, judgeandmove2, score2, step2, margin_size,
                               button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap,
                               flag, flag_1, username)
            print('ai_result:', ai_result)
            print('(ai_result[0] is not None):', (ai_result[0] is not None))
            print('(ai_result[10] is None):', (ai_result[15] is None))
            print('flag_1==22', flag_2==22)

            if  (ai_result[0] is not None) and (ai_result[15] is None):#玩家2游戏结束
                score2, step2, chess_nums2, width, height, difficulty, theme, flag_2 = ai_result[0:8]
            else:
                score2, width, height, difficulty, theme, chess_nums2, judgeandmove2, step2, margin_size, \
            button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1 = ai_result

        #return score, width, height, difficulty, theme, chess_nums, judgeandmove, ro1, margin_size, button_area_start_x, button_start_y, button_width, button_height, button_vertical_gap, flag, flag_1

        if flag and flag_1 == 4:
            game_model = 'single'
            player = 'player1'
            return result[0], width, height, theme, difficulty, game_model, player

        pygame.display.update()
        pygame.display.flip()
        clock.tick(30)





if __name__ == "__main__":
    pygame.init()
    # 大、中、小三种界面大小
    sizes = [(960, 600), (760, 370), (400, 200)]
    size_index = 1  # 初始选择大界面

    isGameRestart = 0

    WIDTH, HEIGHT = sizes[size_index]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_login_register = GameLoginRegister(screen)

    loginFlag, username, WIDTH, HEIGHT = game_login_register.login_screen(WIDTH, HEIGHT)
    theme = '#92877d'
    difficulty = 'normal'
    game_model = 'single'
    if loginFlag:
        while True:
            # 运行一次游戏
            if game_model == 'single':
                score, new_width, new_height, theme, difficulty, game_model = run(screen, WIDTH, HEIGHT, username, theme, difficulty, game_model)
                WIDTH, HEIGHT = new_width, new_height  # 更新窗口宽度和高度
                # 显示游戏结束，是否重来
                # 这里假设 show_game_over 函数存在

                if game_model == 'single':
                    isGameRestart, width, height, theme = show_game_over(screen, score, WIDTH, HEIGHT, theme)

            if game_model == 'double':
                score, new_width, new_height, theme, difficulty, game_model, player = run_double_player_game(screen, WIDTH, HEIGHT, username, theme,difficulty, game_model)
                WIDTH, HEIGHT = new_width, new_height  
                if game_model == 'double':
                    isGameRestart, width, height, theme = show_double_game_over(screen, score, WIDTH, HEIGHT, theme, player)


