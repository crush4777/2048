import random
import sys
import time
from collections.abc import Iterable
from functools import reduce
import pygame

from ai import analyze_moves

# 屏幕尺寸
WIDTH, HEIGHT = (700, 370)
# 背景颜色
BG_COLOR = '#92877d'
# 棋盘需要的数据
MARGIN_SIZE = 10  # 间隔大小
BLOCK_SIZE = 80  # 棋子位置大小
username = '1'

def draw_tips(screen, x, y, z, n, text):
    """
    显示提示信息#
    420, 100, 190, 40
    """
    # 显示"分数："
    button_color = (255, 255, 0)  # 按钮颜色：绿色
    button_rect = pygame.Rect(x, y, z, n)  # 按钮位置和大小
    font_big = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", 30)
    pygame.draw.rect(screen, button_color, button_rect)  # 绘制按钮矩形
    text_surface = font_big.render(text, True, (255, 0, 0))  # 按钮上的文字
    screen.blit(text_surface, (x + 10, y + 5))
    return button_rect


def get_score(chess_nums_temp):
    """
    计算当前棋盘的总分数
    """

    def sum_all(x, y):
        if isinstance(x, Iterable):
            return sum(x) + sum(y)
        return x + sum(y)

    return reduce(sum_all, chess_nums_temp)


def draw_score(screen, score,rot):
    """
    显示分数
    """
    # 显示数字
    font_size_big = 30
    font_color = (0, 255, 255)
    font_big = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_big)
    # score = font_big.render(str(), True, (255, 255, 0))
    # screen.blit(score, (470, 20))
    score = font_big.render(str(score), True, font_color)
    screen.blit(score, (490, 20))
    # 显示"分数："
    # score_img = pygame.image.load("2.png")
    # screen.blit(score_img, (370, 30))


def show_game_over(screen,mm):
    font_size_big = 60
    font_size_small = 30
    font_color = (255, 255, 255)
    font_big = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_big)
    font_small = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size_small)
    surface = screen.convert_alpha()
    surface.fill((0, 0, 0, 2))
    text = font_big.render(f'{mm}', True, (0,0,0))
    text_rect1 = text.get_rect()
    text_rect1.centerx, text_rect1.centery = WIDTH / 2, HEIGHT / 2 - 50
    surface.blit(text1, text_rect1)
    text = font_big.render(f'Game Over!', True, (0,0,0))
    text_rect = text.get_rect()
    text_rect.centerx, text_rect.centery = WIDTH / 2, HEIGHT / 2 - 50
    surface.blit(text, text_rect) 
    button_width, button_height = 100, 40
    button_start_x_left = WIDTH / 2 - button_width - 20
    button_start_x_right = WIDTH / 2 + 20
    button_start_y = HEIGHT / 2 - button_height / 2 + 20
    pygame.draw.rect(surface, (0, 255, 255), (button_start_x_left, button_start_y, button_width, button_height))
    text_restart = font_small.render('Restart', True, (00,33,66))
    text_restart_rect = text_restart.get_rect()
    text_restart_rect.centerx, text_restart_rect.centery = button_start_x_left + button_width / 2, button_start_y + button_height / 2
    surface.blit(text_restart, text_restart_rect)
    pygame.draw.rect(surface, (0, 255, 255), (button_start_x_right, button_start_y, button_width, button_height))
    text_quit = font_small.render('Quit', True, (00,33,66))
    text_quit_rect = text_quit.get_rect()
    text_quit_rect.centerx, text_quit_rect.centery = button_start_x_right + button_width / 2, button_start_y + button_height / 2
    surface.blit(text_quit, text_quit_rect)
    clock = pygame.time.Clock()
    while True:
        screen.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                if text_quit_rect.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()
                if text_restart_rect.collidepoint(pygame.mouse.get_pos()):
                    return True
        pygame.display.update()
        clock.tick(60)


def judge_game_over(field):
    """
    只要有1个方向可以移动，那么游戏就没结束
    """
    return not any([judge_move_left(field), judge_move_right(field), judge_move_up(field), judge_move_down(field)])


def judge_move_up(chess_nums_temp):
    # 对棋盘的数字进行「行与列转置」，即原来在第2行第3列变为第3行第2列
    # zip: 实现
    # *chess_nums_temp对列表进行拆包
    chess_nums_temp = [list(row) for row in zip(*chess_nums_temp)]
    return judge_move_left(chess_nums_temp)


def judge_move_down(chess_nums_temp):
    """
    逻辑：判断能否向下移动, 也就是对于元素进行转置, 判断转置后的棋盘能否向右移动
    """
    # 1.「行与列转置」
    chess_nums_temp = [list(row) for row in zip(*chess_nums_temp)]
    # 2. 判断是否可以向右移动
    return judge_move_right(chess_nums_temp)


def judge_move_left(chess_nums_temp):
    # 只要棋盘的任意一行可以向左移动， 就返回True
    for row in chess_nums_temp:
        for i in range(3):  # 每一行判断3次
            # 如果判断的左边的数为0，右边的数不为0，则说明可以向左移动；
            if row[i] == 0 and row[i + 1] != 0:
                return True
            elif row[i] != 0 and row[i + 1] == row[i]:
                # 如果判断的左边的数不为0，且左右2个数相等，则说明可以向左移动；
                return True
    return False


def judge_move_right(chess_nums_temp):
    # 对棋盘的每一行元素进行反转，此时就可以用向左的函数进行判断了
    return judge_move_left([row[::-1] for row in chess_nums_temp])


def move_left(chess_nums_temp):
    for i, row in enumerate(chess_nums_temp):
        # 1.把这一行的非0 数字向前放，把0向后放。例如之前是[0, 2, 2, 2]-->[2, 2, 2, 0]
        row = sorted(row, key=lambda x: 1 if x == 0 else 0)

        # 2.依次循环判断两个数是否相等，如果相等 第一个*2 第二个数为0。例如[2, 2, 2, 0]-->[4, 0, 2, 0]
        for index in range(3):
            if row[index] == row[index + 1]:
                row[index] *= 2
                row[index + 1] = 0

        # 3.将合并之后的空隙移除，即非0靠左，0靠右。例如[4, 0, 2, 0]-->[4, 2, 0, 0]
        row = sorted(row, key=lambda x: 1 if x == 0 else 0)
        # 4. 更新数字列表，因为这一行已经是操作之后的了
        chess_nums_temp[i] = row
    return chess_nums_temp


def move_right(chess_nums_temp):
    # 先翻翻转
    chess_nums_temp = [row[::-1] for row in chess_nums_temp]
    # 然后在调用像左移动的功能
    move_left(chess_nums_temp)
    # 最后再次翻转，实现之前的样子
    return [row[::-1] for row in chess_nums_temp]


def move_up(chess_nums_temp):
    # "行与列转置"
    chess_nums_temp = [list(row) for row in zip(*chess_nums_temp)]
    # 向左移动
    chess_nums_temp = move_left(chess_nums_temp)
    # 再次"行与列转置"从而实现复原
    return [list(row) for row in zip(*chess_nums_temp)]


def move_down(chess_nums_temp):
    # "行与列转置"
    chess_nums_temp = [list(row) for row in zip(*chess_nums_temp)]
    # 向右移动
    chess_nums_temp = move_right(chess_nums_temp)
    # 再次"行与列转置"从而实现复原
    return [list(row) for row in zip(*chess_nums_temp)]


def move(chess_nums_temp, direction):
    """
    根据方向移动数字
    """
    # 存储判断各个方向是否可移动对应的函数
    judge_move_func_dict = {
        'left': judge_move_left,
        'right': judge_move_right,
        'up': judge_move_up,
        'down': judge_move_down
    }
    # 存储各个方向移动的函数
    move_func_dict = {
        'left': move_left,
        'right': move_right,
        'up': move_up,
        'down': move_down
    }

    # 调用对应的函数，判断是否可以朝这个方向移动
    ret = judge_move_func_dict[direction](chess_nums_temp)
    print("%s方向是否可以移动：" % direction, ret)
    if ret:
        chess_nums_temp = move_func_dict[direction](chess_nums_temp)
        create_random_num(chess_nums_temp)

    # 返回列表，如果更新了就是新的，如果没有更新就是之前的那个
    return chess_nums_temp


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
    for row, line in enumerate(nums_temp):
        for col, num in enumerate(line):
            if num == 0:
                positions.append((row, col))
    row, col = random.choice(positions)
    nums_temp[row][col] = random.choice([2, 4, 2])


def draw_nums(screen, chess_nums_temp):
    """
    显示棋盘上的数字
    """
    # 准备字体等
    font_size = BLOCK_SIZE - 23
    font = pygame.font.Font("QingNiaoHuaGuangJianMeiHei-2.ttf", font_size)
    # 遍历数字
    for i, line in enumerate(chess_nums_temp):
        for j, num in enumerate(line):
            if num != 0:
                # 计算显示位置（x坐标、y坐标）
                x = MARGIN_SIZE * (j + 1) + BLOCK_SIZE * j
                y = MARGIN_SIZE * (i + 1) + BLOCK_SIZE * i
                # 获取颜色
                font_color = pygame.Color(get_num_color(num)[1])
                # 显示数字
                text = font.render(str(num), True, font_color)
                text_rect = text.get_rect()
                text_rect.centerx, text_rect.centery = x + BLOCK_SIZE / 2, y + BLOCK_SIZE / 2
                # 用对应的数字背景色，重新绘制这个方块
                pygame.draw.rect(screen, pygame.Color(get_num_color(num)[0]), (x, y, BLOCK_SIZE, BLOCK_SIZE))
                screen.blit(text, text_rect)


def draw_chess_board(screen):
    """
    显示棋盘
    """
    for i in range(4):
        for j in range(4):
            x = MARGIN_SIZE * (j + 1) + BLOCK_SIZE * j
            y = MARGIN_SIZE * (i + 1) + BLOCK_SIZE * i
            pygame.draw.rect(screen, pygame.Color('#f9f6f2'), (x, y, BLOCK_SIZE, BLOCK_SIZE))


def run(screen):
    print(username)

    # 定义列表，用来记录当前棋盘上的所有数字，如果某位置没有数字，则为0
    chess_nums = [[0 for _ in range(4)] for _ in range(4)]
    # 随机生成一个数字
    create_random_num(chess_nums)
    create_random_num(chess_nums)
    # 记录当前的分数
    score = get_score(chess_nums)
    # 创建计时器（防止while循环过快，占用太多CPU的问题）
    clock = pygame.time.Clock()
    flag = False
    flag_1 = 0
    while True:
        # 显示背景色
        screen.fill(pygame.Color(BG_COLOR))

        # 显示棋盘
        draw_chess_board(screen)

        # 显示棋盘上的数字
        draw_nums(screen, chess_nums)

        # 显示分数
        draw_score(screen, score)

        # 显示操作提示
        button_rect = draw_tips(screen, 370, 100, 130, 40, '贪心算法')
        button_rect1 = draw_tips(screen, 510, 100, 130, 40, '最大空格')
        button_rect2 = draw_tips(screen, 370, 150, 130, 40, '综合评估')
        button_rect3 = draw_tips(screen, 510, 150, 130, 40, '智能提示')

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    flag = False
                    direction = \
                    {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[
                        event.key]
                    chess_nums = move(chess_nums, direction)
                    if judge_game_over(chess_nums):
                        with open('fs.txt', 'a') as f:
                            f.write(f'{username}:{score}\n')
                        print("游戏结束....")
                        return
                    # 每按下方向键，就重新计算
                    score = get_score(chess_nums)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标点击事件
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标位置
                if button_rect.collidepoint(mouse_pos):  # 判断鼠标是否点击到按钮区域
                    # 假设当前玩家坐标为 (px, py)，目标坐标为 (tx, ty)
                    flag = True
                    flag_1 = 1
                if button_rect1.collidepoint(mouse_pos):  # 判断鼠标是否点击到按钮区域
                    # 假设当前玩家坐标为 (px, py)，目标坐标为 (tx, ty)
                    flag = True
                    flag_1 = 2
                if button_rect2.collidepoint(mouse_pos):  # 判断鼠标是否点击到按钮区域
                    # 假设当前玩家坐标为 (px, py)，目标坐标为 (tx, ty)
                    flag = True
                    flag_1 = 3
                if button_rect3.collidepoint(mouse_pos):  # 判断鼠标是否点击到按钮区域
                    # 假设当前玩家坐标为 (px, py)，目标坐标为 (tx, ty)
                    flag = True
                    flag_1 = 4

        if flag:
            try:
                ai1, ai2, ai3, text = analyze_moves(chess_nums)
                if flag_1 == 1:
                    chess_nums = move(chess_nums, ai1)
                    time.sleep(0.5)
                elif flag_1 == 2:
                    chess_nums = move(chess_nums, ai2)
                    time.sleep(0.5)
                elif flag_1 == 3:
                    chess_nums = move(chess_nums, ai3)
                    time.sleep(0.5)
                else:
                    draw_tips(screen, 370, 200, 320, 40, text[0])
                    draw_tips(screen, 370, 250, 320, 40, text[1])
                    draw_tips(screen, 370, 300, 320, 40, text[2])


                score = get_score(chess_nums)

            except:
                if judge_game_over(chess_nums):

                    print("游戏结束....")
                    score = get_score(chess_nums)
                    with open('fs.txt', 'a') as f:
                        f.write(f'{username}:{score}')
                    return

        # 刷新显示（此时窗口才会真正的显示）
        pygame.display.update()

        # FPS（每秒钟显示画面的次数）
        clock.tick(60)  # 通过一定的延时，实现1秒钟能够循环60次


def main():

    # 游戏初始化
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    while True:
        # 运行一次游戏
       mm = run(screen)

        # 显示游戏结束，是否重来
        show_game_over(screen,mm)


if __name__ == '__main__':
    import tkinter as tk
    from tkinter import messagebox


    # 文件路径
    USER_FILE = "user.txt"


    # 检查用户是否存在
    def check_user(username, password):
        try:
            with open(USER_FILE, "r") as file:
                for line in file:
                    saved_username, saved_password = line.strip().split(":")
                    if username == saved_username and password == saved_password:
                        return True
        except FileNotFoundError:
            pass
        return False


    # 注册用户
    def register_user(username, password):
        with open(USER_FILE, "a") as file:
            file.write(f"{username}:{password}\n")
        messagebox.showinfo("注册成功", "用户注册成功！")


    # 登录功能
    def login():
        global username
        username = entry_username.get()
        password = entry_password.get()

        if check_user(username, password):
            messagebox.showinfo("登录成功", f"欢迎回来，{username}！")
            root.destroy()
            main()
        else:
            messagebox.showerror("登录失败", "用户名或密码错误！")
    def login_1():
        root.deiconify()
        root1.withdraw()

      # 注册功能
    def register():
        root.withdraw()
        root1.deiconify()

    def register1():


        username = entry_username1.get()
        password = entry_password1.get()

        if username and password:
            register_user(username, password)
        else:
            messagebox.showerror("注册失败", "用户名和密码不能为空！")


    # 创建主窗口
    root = tk.Tk()
    root.title("登录和注册")
    root.geometry("300x200")

    # 用户名标签和输入框
    label_username = tk.Label(root, text="用户名:")
    label_username.pack(pady=5)
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)

    # 密码标签和输入框
    label_password = tk.Label(root, text="密码:")
    label_password.pack(pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)

    # 创建一个框架来放置登录和注册按钮
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # 登录按钮
    button_login = tk.Button(button_frame, text="登录", command=login)
    button_login.pack(side=tk.LEFT, padx=5)

    # 注册按钮
    button_register = tk.Button(button_frame, text="注册", command=register)
    button_register.pack(side=tk.LEFT, padx=5)

    root1 = tk.Tk()
    root1.title("登录和注册")
    root1.geometry("300x200")

    # 用户名标签和输入框
    label_username1 = tk.Label(root1, text="用户名:")
    label_username1.pack(pady=5)
    entry_username1 = tk.Entry(root1)
    entry_username1.pack(pady=5)

    # 密码标签和输入框
    label_password1 = tk.Label(root1, text="密码:")
    label_password1.pack(pady=5)
    entry_password1 = tk.Entry(root1, show="*")
    entry_password1.pack(pady=5)

    # 创建一个框架来放置登录和注册按钮
    button_frame1 = tk.Frame(root1)
    button_frame1.pack(pady=10)

    # 登录按钮
    button_login = tk.Button(button_frame1, text="返回", command=login_1)
    button_login.pack(side=tk.LEFT, padx=5)

    # 注册按钮
    button_register1 = tk.Button(button_frame1, text="注册", command=register1)
    button_register1.pack(side=tk.LEFT, padx=5)
    root1.withdraw()
    root1.mainloop()
    # 运行主循环
    root.mainloop()


