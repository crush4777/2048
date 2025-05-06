import random


class JudgeAndMove:
    def __init__(self, chess_nums_temp, difficulty):
        self.chess_nums_temp = chess_nums_temp
        self.difficulty = difficulty

    def judge_game_over(self):
        """
        只要有1个方向可以移动，那么游戏就没结束
        """
        return not any([self.judge_move_left(self.chess_nums_temp), self.judge_move_right(self.chess_nums_temp),
                        self.judge_move_up(self.chess_nums_temp), self.judge_move_down(self.chess_nums_temp)])

    def judge_move_up(self, chess_nums_temp):
        # 对棋盘的数字进行「行与列转置」，即原来在第2行第3列变为第3行第2列
        # zip: 实现
        # *chess_nums_temp对列表进行拆包
        chess_nums_temp = [list(row) for row in zip(*chess_nums_temp)]
        return self.judge_move_left(chess_nums_temp)

    def judge_move_down(self, chess_nums_temp):
        """
        逻辑：判断能否向下移动, 也就是对于元素进行转置, 判断转置后的棋盘能否向右移动
        """
        # 1.「行与列转置」
        chess_nums_temp = [list(row) for row in zip(*chess_nums_temp)]
        # 2. 判断是否可以向右移动
        return self.judge_move_right(chess_nums_temp)

    def judge_move_left(self, chess_nums_temp):
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

    def judge_move_right(self, chess_nums_temp):
        # 对棋盘的每一行元素进行反转，此时就可以用向左的函数进行判断了
        return self.judge_move_left([row[::-1] for row in chess_nums_temp])

    def move_left(self, chess_nums_temp):
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

    def move_right(self, chess_nums_temp):
        # 先翻翻转
        chess_nums_temp = [row[::-1] for row in chess_nums_temp]
        # 然后在调用像左移动的功能
        chess_nums_temp = self.move_left(chess_nums_temp)
        # 最后再次翻转，实现之前的样子
        return [row[::-1] for row in chess_nums_temp]

    def move_up(self, chess_nums_temp):
        # "行与列转置"
        chess_nums_temp = [list(row) for row in zip(*chess_nums_temp)]
        # 向左移动
        chess_nums_temp = self.move_left(chess_nums_temp)
        # 再次"行与列转置"从而实现复原
        return [list(row) for row in zip(*chess_nums_temp)]

    def move_down(self, chess_nums_temp):
        # "行与列转置"
        chess_nums_temp = [list(row) for row in zip(*chess_nums_temp)]
        # 向右移动
        chess_nums_temp = self.move_right(chess_nums_temp)
        # 再次"行与列转置"从而实现复原
        return [list(row) for row in zip(*chess_nums_temp)]



    def create_random_num(self, chess_nums_temp):
        """
        在空白位置随机生成数字，根据难度调整生成概率和位置
        """
        rows, cols = len(chess_nums_temp), len(chess_nums_temp[0])

        # 定义角落位置
        corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]
        # 定义边缘位置（不包括角落）
        edges = [(i, j) for i in range(rows) for j in range(cols)
                 if (i in [0, rows - 1] or j in [0, cols - 1]) and (i, j) not in corners]
        # 定义内部位置（既不在角落也不在边缘）
        inner = []
        empty_cells = []
        for i in range(rows):
            for j in range(cols):
                if chess_nums_temp[i][j] == 0:
                    empty_cells.append((i, j))
                    if (i, j) not in corners and (i, j) not in edges:
                        inner.append((i, j))

        print('len(empty_cells):', len(empty_cells))
        print('empty_cells:', empty_cells)

        if len(empty_cells) <= 3:
            row, col = random.choice(empty_cells)
            chess_nums_temp[row][col] = random.choice([2, 4])
            return chess_nums_temp

        if empty_cells:
            # 根据难度选择位置
            rand_pos = random.random()
            if self.difficulty == 'easy':
                if rand_pos < 0.7 and any(cell in corners for cell in empty_cells):
                    available_corners = [cell for cell in corners if cell in empty_cells]
                    row, col = random.choice(available_corners)
                else:
                    row, col = random.choice(empty_cells)
            elif self.difficulty == 'normal':
                if rand_pos < 0.6 and any(cell in edges for cell in empty_cells):
                    available_edges = [cell for cell in edges if cell in empty_cells]
                    row, col = random.choice(available_edges)
                elif rand_pos < 0.8 and any(cell in corners for cell in empty_cells):
                    available_corners = [cell for cell in corners if cell in empty_cells]
                    row, col = random.choice(available_corners)
                else:
                    row, col = random.choice(empty_cells)
            elif self.difficulty == 'difficult':
                if rand_pos < 0.7 and any(cell in inner for cell in empty_cells):
                    available_inner = [cell for cell in inner if cell in empty_cells]
                    row, col = random.choice(available_inner)
                elif rand_pos < 0.9 and any(cell in edges for cell in empty_cells):
                    available_edges = [cell for cell in edges if cell in empty_cells]
                    row, col = random.choice(available_edges)
                elif any(cell in corners for cell in empty_cells):
                    available_corners = [cell for cell in corners if cell in empty_cells]
                    row, col = random.choice(available_corners)
                else:
                    row, col = random.choice(empty_cells)

            # 确保选择的位置是空白的
            assert chess_nums_temp[row][col] == 0

            # 根据难度选择数字
            rand_num = random.random()
            if self.difficulty == 'easy':
                # 简单难度：95% 概率生成 2，5% 概率生成 4
                chess_nums_temp[row][col] = 2 if rand_num < 0.95 else 4
            elif self.difficulty == 'normal':
                # 普通难度：80% 概率生成 2，20% 概率生成 4
                chess_nums_temp[row][col] = 2 if rand_num < 0.8 else 4
            elif self.difficulty == 'difficult':
                # 困难难度：60% 概率生成 2，30% 概率生成 4，10% 概率生成 8
                if rand_num < 0.6:
                    chess_nums_temp[row][col] = 2
                elif rand_num < 0.9:
                    chess_nums_temp[row][col] = 4
                else:
                    chess_nums_temp[row][col] = 8
        return chess_nums_temp

    def move(self, direction):
        """
        根据方向移动数字
        """
        # 存储判断各个方向是否可移动对应的函数
        judge_move_func_dict = {
            'left': self.judge_move_left,
            'right': self.judge_move_right,
            'up': self.judge_move_up,
            'down': self.judge_move_down
        }
        # 存储各个方向移动的函数
        move_func_dict = {
            'left': self.move_left,
            'right': self.move_right,
            'up': self.move_up,
            'down': self.move_down
        }

        # 调用对应的函数，判断是否可以朝这个方向移动
        ret = judge_move_func_dict[direction](self.chess_nums_temp)
        print("%sIs the direction movable：" % direction, ret)
        if ret:
            self.chess_nums_temp = move_func_dict[direction](self.chess_nums_temp)
            self.chess_nums_temp = self.create_random_num(self.chess_nums_temp)

        # 返回列表，如果更新了就是新的，如果没有更新就是之前的那个
        self.write_field_to_txt()
        return self.chess_nums_temp

    def write_field_to_txt(self):
        try:
            with open('game_field.txt', 'a') as file:
                for row in self.chess_nums_temp:
                    line = ' '.join(map(str, row))
                    file.write(line + '\n')
                file.write('\n')
        except Exception as e:
            print(f"Error writing to file: {e}")



