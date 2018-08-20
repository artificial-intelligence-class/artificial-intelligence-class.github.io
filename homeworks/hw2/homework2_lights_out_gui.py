import sys
import Tkinter

import homework2

class Light(Tkinter.Canvas):

    BACKGROUND_ON = "white"
    BACKGROUND_OFF = "gray50"

    BORDER_ON = "red"
    BORDER_OFF = "black"

    def __init__(self, master, size=60):
        Tkinter.Canvas.__init__(self, master, height=size, width=size,
            background=Light.BACKGROUND_OFF, highlightthickness=2,
            highlightbackground=Light.BORDER_OFF)

    def set_state(self, state):
        color = Light.BACKGROUND_ON if state else Light.BACKGROUND_OFF
        self.configure(background=color)

    def set_selected(self, selected):
        color = Light.BORDER_ON if selected else Light.BORDER_OFF
        self.configure(highlightbackground=color)

class Board(Tkinter.Frame):

    def __init__(self, master, puzzle, rows, cols):

        Tkinter.Frame.__init__(self, master)

        self.puzzle = puzzle
        self.rows = rows
        self.cols = cols

        self.lights = []
        for row in range(self.rows):
            row_lights = []
            for col in range(self.cols):
                light = Light(self)
                light.grid(row=row, column=col, padx=1, pady=1)
                light.bind("<Button-1>",
                    lambda event, row=row, col=col: self.click(row, col))
                row_lights.append(light)
            self.lights.append(row_lights)

    def click(self, row, col):
        self.puzzle.perform_move(row, col)
        self.update_lights()

    def update_lights(self):
        puzzle_board = self.puzzle.get_board()
        for row in range(self.rows):
            for col in range(self.cols):
                self.lights[row][col].set_state(puzzle_board[row][col])

    def animate_moves(self, moves, delay=500):
        if moves:
            row, col = moves[0]
            def stage_1():
                self.lights[row][col].set_selected(True)
                self.after(delay, stage_2)
            def stage_2():
                self.lights[row][col].set_selected(False)
                self.puzzle.perform_move(row, col)
                self.update_lights()
                self.after(delay, stage_3)
            def stage_3():
                self.animate_moves(moves[1:], delay=delay)
            stage_1()

class LightsOutGUI(Tkinter.Frame):

    def __init__(self, master, rows, cols):

        Tkinter.Frame.__init__(self, master)

        self.puzzle = homework2.create_puzzle(rows, cols)

        self.board = Board(self, self.puzzle, rows, cols)
        self.board.pack(side=Tkinter.LEFT, padx=1, pady=1)

        menu = Tkinter.Frame(self)
        Tkinter.Button(menu, text="Scramble", command=self.scramble_click).pack(
            fill=Tkinter.X, padx=1, pady=1)
        Tkinter.Button(menu, text="Solve", command=self.solve_click).pack(
            fill=Tkinter.X, padx=1, pady=1)
        menu.pack(side=Tkinter.RIGHT)

    def scramble_click(self):
        self.puzzle.scramble()
        self.board.update_lights()

    def solve_click(self):
        self.board.animate_moves(self.puzzle.find_solution())

if __name__ == "__main__":
    root = Tkinter.Tk()
    root.title("Lights Out")
    rows, cols = sys.argv[1:]
    LightsOutGUI(root, int(rows), int(cols)).pack()
    root.resizable(height=False, width=False)
    root.mainloop()
