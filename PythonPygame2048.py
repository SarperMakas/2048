import tkinter as tk
import colors as c
import random


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")

        self.mainGrid = tk.Frame(
          self, bg=c.BgGray, bd=3, width=395, height=395
        )
        self.mainGrid.grid(pady=(1, 0))
        self.makeGUI()
        self.startGame()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    def makeGUI(self):
        # make Grid
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cellFrame = tk.Frame(
                    self.mainGrid,
                    bg=c.GrayForBlank,
                    width=c.SqSize,
                    height=c.SqSize,
                )
                cellFrame.grid(row=i, column=j, padx=5, pady=5)
                cellNumber = tk.Label(self.mainGrid, bg=c.GrayForBlank)
                cellNumber.grid(row=i, column=j)
                cellData = {"frame": cellFrame, "number": cellNumber}
                row.append(cellData)
            self.cells.append(row)

    def startGame(self):
        # create matrix of zeroes
        self.matrix = [[0] * 4 for _ in range(4)]

        # fill 2 random cells with 2s
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.GrayForBlank)
        self.cells[row][col]["number"].configure(
            bg=c.GrayFor2,
            fg="#ffffff",
            font=c.FONT,
            text="2",
        )
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.GrayForBlank)
        self.cells[row][col]["number"].configure(
            bg=c.GrayFor2,
            fg="#ffffff",
            font=c.FONT,
            text="2",
        )

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix


    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    # Add a new 2 or 4 tile randomly to an empty cell

    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])

    # Update the GUI to match the matrix

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.GrayForBlank)
                    self.cells[i][j]["number"].configure(bg=c.GrayForBlank, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.ColorsForNum[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.ColorsForNum[cell_value],
                        fg="#000000",
                        font=c.FONT,
                        text=str(cell_value)
                    )

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    # Check if any moves are possible
    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    # Check if game is over (Win(Lose)

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.mainGrid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You win",
                bg=c.WINNER_BG,
                fg="#ffffff",
                font=c.GameOverFONT
            ).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.mainGrid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game Over!",
                bg=c.Loser_BG,
                fg="#ffffff",
                font=c.GameOverFONT
            ).pack()


def main():
    Game()


if __name__ == '__main__':
    main()
