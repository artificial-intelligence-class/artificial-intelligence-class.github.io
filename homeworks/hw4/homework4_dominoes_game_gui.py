import sys
import tkinter

import homework4

class Square(tkinter.Canvas):

    COLOR_EMPTY = "white"
    COLOR_FILLED = "gray50"

    def __init__(self, master, size=50):
        tkinter.Canvas.__init__(self, master, height=size, width=size,
            background=Square.COLOR_EMPTY, highlightthickness=2,
            highlightbackground="black")

    def set_state(self, state):
        color = Square.COLOR_FILLED if state else Square.COLOR_EMPTY
        self.configure(background=color)

class Board(tkinter.Frame):

    def __init__(self, master, game, rows, cols):

        tkinter.Frame.__init__(self, master)

        self.game = game
        self.vertical = True
        self.rows = rows
        self.cols = cols

        self.squares = []
        for row in range(rows):
            row_squares = []
            for col in range(cols):
                square = Square(self)
                square.grid(row=row, column=col, padx=1, pady=1)
                square.bind("<Button-1>",
                    lambda event, row=row, col=col: self.perform_move(row, col))
                row_squares.append(square)
            self.squares.append(row_squares)

    def perform_move(self, row, col):
        if self.game.is_legal_move(row, col, self.vertical):
            self.game.perform_move(row, col, self.vertical)
            self.vertical = not self.vertical
            self.update_squares()
            self.master.update_status()

    def update_squares(self):
        game_board = self.game.get_board()
        for row in range(self.rows):
            for col in range(self.cols):
                self.squares[row][col].set_state(game_board[row][col])

class DominoesGUI(tkinter.Frame):

    def __init__(self, master, rows, cols):

        tkinter.Frame.__init__(self, master)

        self.game = homework4.create_dominoes_game(rows, cols)
        self.rows = rows
        self.cols = cols

        self.board = Board(self, self.game, rows, cols)
        self.board.pack(side=tkinter.LEFT, padx=1, pady=1)

        menu = tkinter.Frame(self)

        self.status_label = tkinter.Label(menu, font=("Arial", 16))
        self.status_label.pack(padx=1, pady=(1, 10))
        self.update_status()
        
        tkinter.Label(menu, text="Press 'r' to perform a random move.").pack(
            padx=1, pady=1, anchor=tkinter.W)

        tkinter.Label(menu,
            text=("Press a number between 1 and 9\n"
                  "to perform the best move found\n"
                  "according to an alpha-beta search\n"
                  "with that limit."), justify=tkinter.LEFT).pack(
            padx=1, pady=1, anchor=tkinter.W)
        
        tkinter.Button(menu, text="Reset Game",
            command=self.reset_click).pack(fill=tkinter.X, padx=1, pady=1)
        
        menu.pack(side=tkinter.RIGHT)

        self.focus_set()

        self.bind("r", lambda event: self.perform_random_move())
        for i in range(1, 10):
            self.bind(str(i), lambda event, i=i: self.perform_best_move(i))

    def update_status(self):
        if self.game.game_over(self.board.vertical):
            winner = "Horizontal" if self.board.vertical else "Vertical"
            self.status_label.config(text="Winner: " + winner)
        else:
            turn = "Vertical" if self.board.vertical else "Horizontal"
            self.status_label.config(text="Turn: " + turn)

    def reset_click(self):
        self.game.reset()
        self.board.vertical = True
        self.board.update_squares()
        self.update_status()

    def perform_random_move(self):
        if not self.game.game_over(self.board.vertical):
            row, col = self.game.get_random_move(self.board.vertical)
            self.board.perform_move(row, col)

    def perform_best_move(self, limit):
        if not self.game.game_over(self.board.vertical):
            (row, col), best_value, total_leaves = \
                self.game.get_best_move(self.board.vertical, limit)
            self.board.perform_move(row, col)

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Dominoes Game")
    rows, cols = sys.argv[1:]
    DominoesGUI(root, int(rows), int(cols)).pack()
    root.resizable(height=False, width=False)
    root.mainloop()
