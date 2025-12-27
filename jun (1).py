import tkinter as tk
import random
import time

# 定义游戏面板的大小和初始地雷数量
GRID_SIZE = 10  # 网格大小 (10x10)
NUM_MINES = 10  # 地雷数量

# 游戏状态
game_over = False
start_time = None  # 计时器起始时间
end_time = None  # 计时器结束时间
flags = 0  # 当前放置的旗子数量

# 游戏面板
grid = []

# 初始化游戏
def init_game():
    global game_over, grid, flags, start_time, end_time
    game_over = False
    flags = 0
    start_time = None
    end_time = None
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # 初始化空的格子
    # 随机布置地雷
    mines = set(random.sample(range(GRID_SIZE * GRID_SIZE), NUM_MINES))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            grid[i][j] = {'mine': (i * GRID_SIZE + j) in mines, 'revealed': False, 'flagged': False, 'adjacent': 0}
    # 计算周围地雷数
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j]['mine']:
                continue
            count = 0
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                        if grid[ni][nj]['mine']:
                            count += 1
            grid[i][j]['adjacent'] = count

# 处理鼠标左键点击
def on_left_click(i, j):
    global game_over, start_time, grid
    if game_over:
        return
    if not start_time:
        start_time = time.time()  # 游戏开始计时
    if grid[i][j]['revealed'] or grid[i][j]['flagged']:
        return  # 已经揭开或放置了旗子不能再点击
    grid[i][j]['revealed'] = True
    if grid[i][j]['mine']:
        game_over = True
        end_time = time.time()  # 游戏结束计时
        reveal_all_mines()
        print(f"Game Over! Time: {end_time - start_time:.2f} seconds")
        return
    if grid[i][j]['adjacent'] == 0:  # 如果周围没有地雷，递归揭开周围的格子
        for di in range(-1, 2):
            for dj in range(-1, 2):
                ni, nj = i + di, j + dj
                if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE and not grid[ni][nj]['revealed']:
                    on_left_click(ni, nj)

# 处理鼠标右键点击
def on_right_click(i, j):
    global flags
    if game_over or grid[i][j]['revealed']:
        return
    if grid[i][j]['flagged']:
        grid[i][j]['flagged'] = False
        flags -= 1
    else:
        if flags < NUM_MINES:
            grid[i][j]['flagged'] = True
            flags += 1
    update_ui()

# 揭示所有地雷
def reveal_all_mines():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j]['mine']:
                grid[i][j]['revealed'] = True
            update_ui()

# 更新界面显示
def update_ui():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell = grid[i][j]
            text = ''
            if cell['revealed']:
                if cell['mine']:
                    text = '💣'
                else:
                    text = str(cell['adjacent']) if cell['adjacent'] > 0 else ''
            elif cell['flagged']:
                text = '🚩'
            button = buttons[i][j]
            button.config(text=text, relief="sunken" if cell['revealed'] else "raised")

# 点击按钮（左键、右键）
def button_click(i, j, event):
    if event.num == 1:  # 左键
        on_left_click(i, j)
    elif event.num == 3:  # 右键
        on_right_click(i, j)
    update_ui()

# 设置界面
def setup_ui():
    global buttons
    window = tk.Tk()
    window.title("踩地雷游戏")

    # 创建按钮
    buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            button = tk.Button(window, width=4, height=2, command=lambda i=i, j=j: button_click(i, j, event=None))
            button.bind("<Button-1>", lambda event, i=i, j=j: button_click(i, j, event))
            button.bind("<Button-3>", lambda event, i=i, j=j: button_click(i, j, event))
            button.grid(row=i, column=j)
            buttons[i][j] = button

    window.mainloop()

# 游戏初始化并启动
init_game()
setup_ui()
