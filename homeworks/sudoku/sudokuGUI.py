### Author: Yue Yang ###
import argparse
import copy
import numpy as np
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT, X, OUTSIDE, Label, StringVar, Entry
import tkinter as tk
from sudoku import Sudoku

# Define Canvas Size
canvas_margin = 20
grid_size = 50
canvas_width = canvas_height = canvas_margin * 2 + grid_size * 9

class SudokuError(Exception):
    """
    An application specific error.
    """
    pass

class SudokuBoard(object):
    """
    Sudoku Board representation
    """
    def __init__(self, board_string):
        self.board = self.create_board(board_string)

    def create_board(self, board_string):
        '''
        board string is a string of length 81
        The board is a list of list with size 9x9
        '''
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                ind = i * 9 + j
                value = int(board_string[ind])
                row.append(value)
            board.append(row)
        return board

class SudokuGame(object):
    def __init__(self, board_string):
        self.board_string = board_string
        self.start_puzzle = SudokuBoard(board_string).board

    def start(self):
        self.game_over = False
        self.puzzle = copy.deepcopy(self.start_puzzle)

    def check_valid(self):
        try:
            row_valid = self.check_row()
            col_valid = self.check_col()
            box_valid = self.check_box()
            if row_valid == False or col_valid == False or box_valid == False:
                return False
            else:
                return True
        except:
            return False


    def check_row(self):
        row_valid = True
        for i in range(9):
            current_row = self.puzzle[i]
            if set(current_row) != set(range(1,10)):
                row_valid = False
                break
        return row_valid

    def check_col(self):
        col_valid = True
        for i in range(9):
            current_col = []
            for j in range(9):
                current_col.append(self.puzzle[j][i])
            if set(current_col) != set(range(1,10)):
                col_valid = False
                break
        return col_valid

    def check_box(self):
        box_valid = True
        for i in range(3):
            start_row = i*3
            for j in range(3):
                start_col = j*3
                current_box = []
                for ii in range(3):
                    for jj in range(3):
                        current_box.append(self.puzzle[start_row + ii][start_col+jj])
                if set(current_box) != set(range(1,10)):
                    box_valid = False
                    break
            if box_valid == False:
                break
        return box_valid

class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, master, game):
        self.game = game
        self.master = master
        Frame.__init__(self, master)
        self.startUI()

    def startUI(self):
        self.master.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=canvas_width, height=canvas_width)
        self.canvas.pack(side = LEFT)
        self.clear_button = Button(self,
                              text="Clear Solutions",
                              command=self.clear_click)
        self.clear_button.pack()
        self.clear_button.place(bordermode=OUTSIDE, height=30, width=100, x = 550, y = 100)

        # AC3
        self.solve_button_infer_ac3 = Button(self,
                              text="Solve (infer_ac3)",
                              command=self.solve_click_infer_ac3)
        self.solve_button_infer_ac3.pack()
        self.solve_button_infer_ac3.place(bordermode=OUTSIDE, height=30, width=200, x = 495, y = 150)

        # AC3 IMPROVE
        self.solve_button_infer_improved = Button(self,
                              text="Solve (infer_improved)",
                              command=self.solve_click_infer_improved)
        self.solve_button_infer_improved.pack()
        self.solve_button_infer_improved.place(bordermode=OUTSIDE, height=30, width=200, x = 495, y = 185)

        # AC3 GUESSING
        self.solve_button_infer_with_guessing = Button(self,
                              text="Solve (infer_with_guessing)",
                              command=self.solve_click_infer_with_guessing)
        self.solve_button_infer_with_guessing.pack()
        self.solve_button_infer_with_guessing.place(bordermode=OUTSIDE, height=30, width=200, x = 495, y = 220)

        self.puzzleEntry = Entry(self, width=20)
        self.puzzleEntry.pack()
        self.puzzleEntry.place(x = 500, y = 270)

        self.setpuzzle_button = Button(self,
                              text="Reset Puzzle",
                              command=self.get_puzzle)
        self.setpuzzle_button.pack()
        self.setpuzzle_button.place(bordermode=OUTSIDE, height=30, width=100, x = 550, y = 300)



        self.draw_grid()
        self.draw_puzzle()

    def draw_grid(self):
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"
            line_width = 3 if i % 3 == 0 else 1

            x0 = canvas_margin + i * grid_size
            y0 = canvas_margin
            x1 = canvas_margin + i * grid_size
            y1 = canvas_height - canvas_margin
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width = line_width)

            x0 = canvas_margin
            y0 = canvas_margin + i * grid_size
            x1 = canvas_width - canvas_margin
            y1 = canvas_margin + i * grid_size
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width = line_width)

    def draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = canvas_margin + j * grid_size + grid_size / 2
                    y = canvas_margin + i * grid_size + grid_size / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color, font=("Arial", 16)
                    )

    def list2dict(self):
        board_dict = {}
        for i in range(9):
            for j in range(9):
                value = self.game.start_puzzle[i][j]
                if value == 0:
                    board_dict[(i, j)] = set(range(1, 10))
                else:
                    board_dict[(i, j)] = {value}
        return board_dict

    def dict2list(self, board_dict):
        for key, value in board_dict.items():
            if len(value) == 1:
                self.game.puzzle[key[0]][key[1]] = list(value)[0]
            else:
                self.game.puzzle[key[0]][key[1]] = list(value)

    def solve_click_infer_ac3(self):
        board_dict = self.list2dict()
        SUDOKU = Sudoku(board_dict)
        SUDOKU.infer_ac3()
        self.dict2list(SUDOKU.board)
        self.draw_puzzle()
        self.draw_victory()

    def solve_click_infer_improved(self):
        board_dict = self.list2dict()
        SUDOKU = Sudoku(board_dict)
        SUDOKU.infer_improved()
        self.dict2list(SUDOKU.board)
        self.draw_puzzle()
        self.draw_victory()

    def solve_click_infer_with_guessing(self):
        board_dict = self.list2dict()
        SUDOKU = Sudoku(board_dict)
        SUDOKU.infer_with_guessing()
        self.dict2list(SUDOKU.board)
        self.draw_puzzle()
        self.draw_victory()
        

    def clear_click(self):
        self.game.start()
        self.canvas.delete("winner")
        self.draw_puzzle()

    def get_puzzle(self):
        board_string = self.puzzleEntry.get()
        if len(board_string.split('\n')) > 1:
            board_list = board_string.split('\n')
            board_string_new = ''.join(board_list)
            board_string = ''
            for i in board_string_new:
                if i == '*':
                    board_string += '0'
                else:
                    board_string += i

        if len(board_string) != 81:
            print('Invalid Puzzle')
        else:
            self.game = SudokuGame(board_string)
            self.game.start()
            self.draw_puzzle()

    def draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = canvas_margin + grid_size * 2
        x1 = y1 = canvas_margin + grid_size * 7
        x = y = canvas_margin + 4 * grid_size + grid_size / 2
        if self.game.check_valid() == True:
            self.canvas.create_text(
                x, y,
                text="You win!", tags="winner",
                fill="orange", font=("Arial", 32)
            )
        else:
            self.canvas.create_text(
                x, y,
                text="You lose!", tags="winner",
                fill="orange", font=("Arial", 32)
            )


if __name__ == '__main__':
    game = SudokuGame('004300209005009001070060043006002087190007400050083000600000105003508690042910300')
    game.start()
    root = Tk()
    SudokuUI(root, game)
    root.geometry("700x500")
    root.mainloop()
