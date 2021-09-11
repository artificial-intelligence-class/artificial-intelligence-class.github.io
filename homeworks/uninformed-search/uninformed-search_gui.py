import tkinter as tk
from functools import partial
from tkinter import simpledialog, messagebox

from homework2 import *

QUEEN_IMAGE = 'R0lGODlhPAA8AKIHANDQ0Ojo6KioqDg4OHV1dfj4+P///wAAACH/C1hNUCBEYXRhWE1QPD94cGFja2V0IGJlZ2luPSLvu78iIGlkP' \
              'SJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQW' \
              'RvYmUgWE1QIENvcmUgNi4wLWMwMDIgNzkuMTY0NDYwLCAyMDIwLzA1LzEyLTE2OjA0OjE3ICAgICAgICAiPiA8cmRmOlJERiB4bWx' \
              'uczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjph' \
              'Ym91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvY' \
              'mUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUm' \
              'VmIyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMiAoV2luZG93cykiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5' \
              'paWQ6MjZCQzVEOTdCNTk5MTFFQUI2NjQ4RjZFMkJGNkREQkEiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6MjZCQzVEOThCNTk5' \
              'MTFFQUI2NjQ4RjZFMkJGNkREQkEiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoyNkJDNUQ5N' \
              'UI1OTkxMUVBQjY2NDhGNkUyQkY2RERCQSIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoyNkJDNUQ5NkI1OTkxMUVBQjY2NDhGNk' \
              'UyQkY2RERCQSIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PgH' \
              '//v38+/r5+Pf29fTz8vHw7+7t7Ovq6ejn5uXk4+Lh4N/e3dzb2tnY19bV1NPS0dDPzs3My8rJyMfGxcTDwsHAv769vLu6ubi3trW0' \
              's7KxsK+urayrqqmop6alpKOioaCfnp2cm5qZmJeWlZSTkpGQj46NjIuKiYiHhoWEg4KBgH9+fXx7enl4d3Z1dHNycXBvbm1sa2ppa' \
              'GdmZWRjYmFgX15dXFtaWVhXVlVUU1JRUE9OTUxLSklIR0ZFRENCQUA/Pj08Ozo5ODc2NTQzMjEwLy4tLCsqKSgnJiUkIyIhIB8eHR' \
              'wbGhkYFxYVFBMSERAPDg0MCwoJCAcGBQQDAgEAACH5BAEAAAcALAAAAAA8ADwAAAP/eLrc/jDKSau9OOvNu/9gKI7MYE4nWZlEmzY' \
              's8arPQABGLsyHHeSBHa1GyBkKukGpmEMaZEMYrkClBqCKwa+aAyijC+2RaggEv7Ym2YwFi9eAc5YJv37dgnE53h5M9wFeYGFiR4Ft' \
              'PQQ/BnF2g4QCW0IwTEGIISY8PX5dd2F5ZZqZmigDAgAClz04R5eFjiWmqKoRJos5rreTc0dliDZOuJ4SnFywWVuMnqa9Bb9ba6SUa' \
              'oa7PclPdwNITn1FVd3DRNRm1tt6k2lk2Z9jZM7iNdBlxwcE3EgBaFNkiPe99Gg5SNPMizY64XrgQ/ILVIEABayhEMCt1UE1SAx+47' \
              'LL/8cRAKikQTCRJ2EijEdM8COT7t/DHSJrvRGmYCMXGRiRCAEGpF4GZutkqANnIJU7lpmgBYp3gWDQoeAeHs1oqxcbpk1X5oDKZar' \
              'OYh8BCGxqM1/JqGjJgNQTRyKHN13TynVSZywGoHPzRv0oB9M5vYDz8cGqAW9guYAEjXB6GG3YvotXNn4HcrAKro3DtiXcAW7mApUt' \
              '0zAcWHMcxaMR6gUSWvSQYuuMyGbd2qAbJkasmNndendRziBMtRA6qnjx4cA7jxouoLnz586RZxpt41Sw2dizB4JJgll2r3uz28ake' \
              'jJi1B9gm59LMzi09eztNl0IPy07ELi/69+fJISihyK7BSjggATuBo9fxiWo4IJCIbjggxAm98iEFFZo4YUYDpIAADs='


class NQueens(tk.Frame):
    def __init__(self, parent, n):
        super().__init__(parent)
        self.__n = n
        self.__canvas = tk.Canvas(self)
        self.__buttons = tk.Frame(self)

        self.__queen_image = tk.PhotoImage(data=QUEEN_IMAGE)
        self.__ppb = self.__queen_image.width()
        self.__canvas.config(width=n * self.__ppb, height=n * self.__ppb)
        self.__canvas.pack()

        for i in range(n):
            for j in range(n):
                self.__canvas.create_rectangle(
                    i * self.__ppb, j * self.__ppb, (i + 1) * self.__ppb, (j + 1) * self.__ppb,
                    fill='gray50' if (i & 1) ^ (j & 1) else 'white', outline='')

        self.__solutions = n_queens_solutions(n)
        self.__queens = []
        self.__cur_sol = 0
        self.__label = tk.StringVar()

        self.__prev_btn = tk.Button(self.__buttons, text='Previous solution', command=partial(self.__display, -1))
        self.__next_btn = tk.Button(self.__buttons, text='Next solution', command=partial(self.__display, 1))

        self.__display(0)

        self.__prev_btn.grid(row=0, column=0, padx=2, pady=2)
        self.__next_btn.grid(row=0, column=1, padx=2, pady=2)
        tk.Label(self.__buttons, textvariable=self.__label).grid(row=0, column=2, padx=2, pady=2)
        self.__buttons.pack(side=tk.BOTTOM)

        if not self.__solutions:
            messagebox.showwarning('Warning', 'No solutions returned!')

    def __display(self, delta):
        while self.__queens:
            self.__canvas.delete(self.__queens.pop())
        self.__cur_sol += delta
        if self.__cur_sol <= 0:
            self.__prev_btn.config(state=tk.DISABLED)
        else:
            self.__prev_btn.config(state=tk.NORMAL)
        if self.__cur_sol + 1 >= len(self.__solutions):
            self.__next_btn.config(state=tk.DISABLED)
            if delta == 0:
                return
        else:
            self.__next_btn.config(state=tk.NORMAL)
        self.__label.set('%d/%d' % (self.__cur_sol + 1, len(self.__solutions)))
        for i, pos in enumerate(self.__solutions[self.__cur_sol]):
            self.__queens.append(self.__canvas.create_image(
                (i * self.__ppb, pos * self.__ppb), image=self.__queen_image, anchor=tk.NW))


class LightsOutDialog(simpledialog.Dialog):
    def body(self, parent):
        row_label = tk.Label(parent, text='# of Rows', justify=tk.LEFT)
        row_label.grid(row=0, padx=5, sticky=tk.W)
        self.__row_entry = tk.Entry(parent, name='row')
        self.__row_entry.grid(row=1, padx=5, sticky=tk.EW)
        self.__row_entry.insert(0, 3)

        col_label = tk.Label(parent, text='# of Cols', justify=tk.LEFT)
        col_label.grid(row=2, padx=5, sticky=tk.W)
        self.__col_entry = tk.Entry(parent, name='col')
        self.__col_entry.grid(row=3, padx=5, sticky=tk.EW)
        self.__col_entry.insert(0, 3)

        return self.__row_entry

    def validate(self):
        try:
            n_rows = self.getint(self.__row_entry.get())
            n_cols = self.getint(self.__col_entry.get())
        except ValueError:
            messagebox.showwarning('Illegal value', 'Not an integer.\nPlease try again', parent=self)
            return 0
        if n_rows <= 0 or n_cols <= 0:
            messagebox.showwarning('Illegal value', 'Not a positive integer.\nPlease try again', parent=self)
            return 0
        self.result = (n_rows, n_cols)
        return 1


MOVE_DELAY = 500
SQUARE_SIZE = 100


class LightsOut(tk.Frame):
    def __init__(self, parent, rows, cols):
        super().__init__(parent)
        self.__puzzle = create_puzzle(rows, cols)
        self.__rows = rows
        self.__cols = cols
        self.__canvas = tk.Canvas(self)
        self.__buttons = tk.Frame(self)
        self.__squares = {}

        self.__canvas.config(width=cols * SQUARE_SIZE, height=rows * SQUARE_SIZE)
        self.__canvas.pack()
        self.__update()

        self.__canvas.bind('<Button-1>', self.__click)
        self.__solving = False
        self.__cur_sol = 0

        tk.Button(self.__buttons, text='Scramble', command=self.__scramble).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(self.__buttons, text='Solve', command=self.__solve).grid(row=0, column=1, padx=2, pady=2)
        self.__buttons.pack(side=tk.BOTTOM)

    def __solve_lock(self):
        self.__solving = True
        for child in self.__buttons.winfo_children():
            child.config(state=tk.DISABLED)

    def __solve_finish(self):
        self.__solving = False
        for child in self.__buttons.winfo_children():
            child.config(state=tk.NORMAL)

    def __update(self):
        self.__canvas.delete(tk.ALL)
        board = self.__puzzle.get_board()
        for j, rows in enumerate(board):
            for i, ele in enumerate(rows):
                self.__canvas.create_rectangle(
                    i * SQUARE_SIZE, j * SQUARE_SIZE, (i + 1) * SQUARE_SIZE, (j + 1) * SQUARE_SIZE,
                    fill='white' if ele else 'grey50')

    def __click(self, event):
        if not self.__solving:
            col, row = event.x // SQUARE_SIZE, event.y // SQUARE_SIZE
            self.__puzzle.perform_move(row, col)
            self.__update()

    def __scramble(self):
        self.__puzzle.scramble()
        self.__update()

    def __solve(self):
        moves = self.__puzzle.find_solution()
        self.__cur_sol = 0

        def highlight():
            j, i = moves[self.__cur_sol]
            self.__canvas.create_rectangle(
                i * SQUARE_SIZE, j * SQUARE_SIZE, (i + 1) * SQUARE_SIZE, (j + 1) * SQUARE_SIZE,
                fill='', outline='red', width=5)
            self.after(MOVE_DELAY, move)

        def move():
            self.__puzzle.perform_move(*moves[self.__cur_sol])
            self.__update()
            self.__cur_sol += 1
            if self.__cur_sol < len(moves):
                self.after(MOVE_DELAY, highlight)
            else:
                self.__solve_finish()

        self.__solve_lock()
        highlight()


class LinearDisksDialog(simpledialog.Dialog):
    def body(self, parent):
        length_label = tk.Label(parent, text='# of Cells (length)', justify=tk.LEFT)
        length_label.grid(row=0, padx=5, sticky=tk.W)
        self.__length_entry = tk.Entry(parent, name='length')
        self.__length_entry.grid(row=1, padx=5, sticky=tk.EW)

        n_label = tk.Label(parent, text='# of disks (N)', justify=tk.LEFT)
        n_label.grid(row=2, padx=5, sticky=tk.W)
        self.__n_entry = tk.Entry(parent, name='n')
        self.__n_entry.grid(row=3, padx=5, sticky=tk.EW)

        self.__check = tk.BooleanVar()
        tk.Checkbutton(parent, text='Distinct disks', variable=self.__check).grid(row=4)

        return self.__length_entry

    def validate(self):
        try:
            length = self.getint(self.__length_entry.get())
            n = self.getint(self.__n_entry.get())
        except ValueError:
            messagebox.showwarning('Illegal value', 'Not an integer.\nPlease try again', parent=self)
            return 0
        if length <= 0 or n <= 0:
            messagebox.showwarning('Illegal value', 'Not a positive integer.\nPlease try again', parent=self)
            return 0
        if length < n:
            messagebox.showwarning('Illegal value', 'Length is less than N.\nPlease try again', parent=self)
            return 0
        self.result = (length, n, self.__check.get())
        return 1


MARGIN = 10


class LinearDisks(tk.Frame):
    def __init__(self, parent, length, n, distinct):
        super().__init__(parent)
        self.__length = length
        self.__solutions = (solve_distinct_disks if distinct else solve_identical_disks)(length, n)
        self.__cur_sol = 0
        self.__canvas = tk.Canvas(self)
        self.__buttons = tk.Frame(self)
        self.__canvas.config(width=length * SQUARE_SIZE, height=SQUARE_SIZE)
        self.__canvas.pack()
        self.__disks = {}
        self.__arrow = None

        for i in range(length):
            self.__canvas.create_rectangle(i * SQUARE_SIZE, 0, (i + 1) * SQUARE_SIZE, SQUARE_SIZE, fill='white')

        for i in range(n):
            self.__disks[i] = (
                self.__canvas.create_oval(
                    i * SQUARE_SIZE + MARGIN, MARGIN, (i + 1) * SQUARE_SIZE - MARGIN, SQUARE_SIZE - MARGIN,
                    fill='black'),
                self.__canvas.create_text(
                    (i + .5) * SQUARE_SIZE, SQUARE_SIZE / 2, text=i, font=(None, MARGIN * 3),
                    fill='white' if distinct else ''))

        self.__next_btn = tk.Button(self.__buttons, text='Next move', command=self.__next,
                                    state=tk.NORMAL if self.__solutions else tk.DISABLED)
        self.__next_btn.pack()
        self.__buttons.pack(side=tk.BOTTOM)

    def __next(self):
        fr, to = self.__solutions[self.__cur_sol]
        if fr not in self.__disks:
            messagebox.showerror('Illegal move',
                                 'Cannot move a disk from position %d to %d\nCell is empty' % (fr, to), parent=self)
            self.__next_btn.config(state=tk.DISABLED)
            return
        if to in self.__disks:
            messagebox.showerror('Illegal move',
                                 'Cannot move a disk from position %d to %d\nCell is not empty' % (fr, to), parent=self)
            self.__next_btn.config(state=tk.DISABLED)
            return
        if to < 0 or to >= self.__length:
            messagebox.showerror('Illegal move',
                                 'Cannot move the disk to %d\nCell is out of bound' % to, parent=self)
            self.__next_btn.config(state=tk.DISABLED)
            return
        disk, label = self.__disks[to] = self.__disks.pop(fr)
        self.__canvas.move(disk, (to - fr) * SQUARE_SIZE, 0)
        self.__canvas.move(label, (to - fr) * SQUARE_SIZE, 0)
        if self.__arrow:
            self.__canvas.delete(self.__arrow)

        self.__arrow = self.__canvas.create_line(
            (fr + .5) * SQUARE_SIZE, SQUARE_SIZE / 2, (to + .5) * SQUARE_SIZE, SQUARE_SIZE / 2,
            arrow=tk.LAST, arrowshape=(MARGIN, MARGIN * 2, MARGIN), fill='orange', width=MARGIN / 2)

        self.__cur_sol += 1
        if self.__cur_sol >= len(self.__solutions):
            self.__next_btn.config(state=tk.DISABLED)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Homework 2 GUI')
        self.minsize(300, 200)
        self.resizable(height=False, width=False)
        self.__menu = tk.Menu(self)
        second_menu = tk.Menu(self.__menu)
        second_menu.add_command(label='N-Queens', command=self.n_queens)
        second_menu.add_command(label='Lights Out', command=self.lights_out)
        second_menu.add_command(label='Linear Disks', command=self.linear_disks)
        self.__menu.add_cascade(label='New', menu=second_menu)
        self.config(menu=self.__menu)
        self.__cur = None

    def draw_rect(self, i, j, size, color):
        return self.__canvas.create_rectangle(
            i * size, j * size, (i + 1) * size, (j + 1) * size, fill=color, outline='')

    def n_queens(self):
        n = simpledialog.askinteger('Input number', 'N', parent=self, minvalue=1, initialvalue=8)
        if not n:
            return
        if self.__cur:
            self.__cur.destroy()
        self.__cur = NQueens(self, n)
        self.__cur.pack(expand=True)

    def lights_out(self):
        result = LightsOutDialog(self, 'Input numbers').result
        if not result:
            return
        if self.__cur:
            self.__cur.destroy()
        self.__cur = LightsOut(self, *result)
        self.__cur.pack(expand=True)

    def linear_disks(self):
        result = LinearDisksDialog(self, 'Input options').result
        if not result:
            return
        if self.__cur:
            self.__cur.destroy()
        self.__cur = LinearDisks(self, *result)
        self.__cur.pack(expand=True)


if __name__ == '__main__':
    GUI().mainloop()
