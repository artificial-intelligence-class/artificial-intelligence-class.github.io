import sys
import tkinter

import homework3

class Tile(tkinter.Canvas):

    BACKGROUND_NORMAL = "white"
    BACKGROUND_EMPTY = "black"

    def __init__(self, master, tile, size=60):
        tkinter.Canvas.__init__(self, master, height=size, width=size,
            highlightthickness=2, highlightbackground="black")
        self.text = self.create_text(size / 2, size / 2, font=("Arial", 24))
        self.set_state(tile)

    def set_state(self, tile):
        color = Tile.BACKGROUND_EMPTY if tile == 0 else Tile.BACKGROUND_NORMAL
        self.configure(background=color)
        self.itemconfig(self.text, text=tile)

class Board(tkinter.Frame):

    def __init__(self, master, puzzle, rows, cols):

        tkinter.Frame.__init__(self, master)

        self.puzzle = puzzle
        self.rows = rows
        self.cols = cols

        puzzle_board = puzzle.get_board()
        self.tiles = []
        for row in range(rows):
            row_tiles = []
            for col in range(cols):
                tile = Tile(self, puzzle_board[row][col])
                tile.grid(row=row, column=col, padx=1, pady=1)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

        self.bind("<Up>", lambda event: self.perform_move("up"))
        self.bind("<Down>", lambda event: self.perform_move("down"))
        self.bind("<Left>", lambda event: self.perform_move("left"))
        self.bind("<Right>", lambda event: self.perform_move("right"))
        self.focus_set()

    def perform_move(self, direction):
        self.puzzle.perform_move(direction)
        self.update_tiles()

    def update_tiles(self):
        puzzle_board = self.puzzle.get_board()
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].set_state(puzzle_board[row][col])

    def animate_moves(self, moves, delay=100):
        if moves:
            def stage_1():
                self.puzzle.perform_move(moves[0])
                self.update_tiles()
                self.after(delay, stage_2)
            def stage_2():
                self.animate_moves(moves[1:], delay=delay)
            stage_1()

class TilePuzzleGUI(tkinter.Frame):

    def __init__(self, master, rows, cols):

        tkinter.Frame.__init__(self, master)

        self.rows = rows
        self.cols = cols
        self.puzzle = homework3.create_tile_puzzle(rows, cols)

        self.board = Board(self, self.puzzle, rows, cols)
        self.board.pack(side=tkinter.LEFT, padx=1, pady=1)

        menu = tkinter.Frame(self)

        tkinter.Label(menu, text="Manipulate the empty tile\nusing the arrow keys.").pack(
            padx=1, pady=1)

        tkinter.Button(menu, text="Scramble", command=self.scramble_click).pack(
            fill=tkinter.X, padx=1, pady=1)
        tkinter.Button(menu, text="Solve Using IDDFS",
            command=self.solve_iddfs_click).pack(fill=tkinter.X, padx=1, pady=1)
        tkinter.Button(menu, text="Solve Using A*",
            command=self.solve_a_star_click).pack(fill=tkinter.X, padx=1, pady=1)

        menu.pack(side=tkinter.RIGHT)

    def scramble_click(self):
        self.puzzle.scramble(self.rows * self.cols * 20)
        self.board.update_tiles()

    def solve_iddfs_click(self):
        self.board.animate_moves(next(self.puzzle.find_solutions_iddfs()))

    def solve_a_star_click(self):
        self.board.animate_moves(self.puzzle.find_solution_a_star())

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Tile Puzzle")
    rows, cols = sys.argv[1:]
    TilePuzzleGUI(root, int(rows), int(cols)).pack()
    root.resizable(height=False, width=False)
    root.mainloop()
