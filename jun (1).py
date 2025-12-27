import tkinter as tk
from tkinter import messagebox
import random

GRID_SIZE = 10
NUM_MINES = 10

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("踩地雷")

        self.buttons = []
        self.grid = []
        self.game_over = False

        self.top_frame = tk.Frame(root)
        self.top_frame.pack()

        self.restart_btn = tk.Button(
            self.top_frame, text="重新開始", command=self.restart
        )
        self.restart_btn.pack()

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.init_game()

    def init_game(self):
        self.game_over = False
        self.grid = []
        self.buttons = []

        for widget in self.frame.winfo_children():
            widget.destroy()

        # 建立資料結構
        self.grid = [[{
            "mine": False,
            "revealed": False,
            "flag": False,
            "adj": 0
        } for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # 放地雷
        mines = random.sample(range(GRID_SIZE * GRID_SIZE), NUM_MINES)
        for m in mines:
            r, c = divmod(m, GRID_SIZE)
            self.grid[r][c]["mine"] = True

        # 計算周圍雷數
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c]["mine"]:
                    continue
                self.grid[r][c]["adj"] = self.count_adjacent(r, c)

        # 建立按鈕
        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                btn = tk.Button(
                    self.frame, width=3, height=1
                )
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.left_click(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)

    def count_adjacent(self, r, c):
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if self.grid[nr][nc]["mine"]:
                        count += 1
        return count

    def left_click(self, r, c):
        if self.game_over:
            return
        cell = self.grid[r][c]
        if cell["revealed"] or cell["flag"]:
            return

        cell["revealed"] = True

        if cell["mine"]:
            self.show_mines()
            self.game_over = True
            messagebox.showinfo("遊戲結束", "💥 你踩到地雷了！")
            return

        if cell["adj"] == 0:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                        if not self.grid[nr][nc]["revealed"]:
                            self.left_click(nr, nc)

        self.update_ui()

    def right_click(self, r, c):
        if self.game_over:
            return
        cell = self.grid[r][c]
        if cell["revealed"]:
            return
        cell["flag"] = not cell["flag"]
        self.update_ui()

    def show_mines(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c]["mine"]:
                    self.buttons[r][c].config(text="💣")

    def update_ui(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = self.grid[r][c]
                btn = self.buttons[r][c]

                if cell["revealed"]:
                    btn.config(relief="sunken", bg="#ddd")
                    if cell["adj"] > 0:
                        btn.config(text=str(cell["adj"]))
                else:
                    btn.config(text="🚩" if cell["flag"] else "", relief="raised", bg="SystemButtonFace")

    def restart(self):
        self.init_game()

if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()
