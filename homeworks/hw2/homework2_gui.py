import tkinter as tk
from functools import partial
from tkinter import simpledialog, messagebox

from homework2_sol import *

QUEEN_IMAGE = 'R0lGODlhPAA8AKIHANDQ0Ojo6KioqDg4OHV1dfj4+P///wAAACH/C1hNUCBEYXRhWE1QPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNi4wLWMwMDIgNzkuMTY0NDYwLCAyMDIwLzA1LzEyLTE2OjA0OjE3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMiAoV2luZG93cykiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MjZCQzVEOTdCNTk5MTFFQUI2NjQ4RjZFMkJGNkREQkEiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6MjZCQzVEOThCNTk5MTFFQUI2NjQ4RjZFMkJGNkREQkEiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoyNkJDNUQ5NUI1OTkxMUVBQjY2NDhGNkUyQkY2RERCQSIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoyNkJDNUQ5NkI1OTkxMUVBQjY2NDhGNkUyQkY2RERCQSIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PgH//v38+/r5+Pf29fTz8vHw7+7t7Ovq6ejn5uXk4+Lh4N/e3dzb2tnY19bV1NPS0dDPzs3My8rJyMfGxcTDwsHAv769vLu6ubi3trW0s7KxsK+urayrqqmop6alpKOioaCfnp2cm5qZmJeWlZSTkpGQj46NjIuKiYiHhoWEg4KBgH9+fXx7enl4d3Z1dHNycXBvbm1sa2ppaGdmZWRjYmFgX15dXFtaWVhXVlVUU1JRUE9OTUxLSklIR0ZFRENCQUA/Pj08Ozo5ODc2NTQzMjEwLy4tLCsqKSgnJiUkIyIhIB8eHRwbGhkYFxYVFBMSERAPDg0MCwoJCAcGBQQDAgEAACH5BAEAAAcALAAAAAA8ADwAAAP/eLrc/jDKSau9OOvNu/9gKI7MYE4nWZlEmzYs8arPQABGLsyHHeSBHa1GyBkKukGpmEMaZEMYrkClBqCKwa+aAyijC+2RaggEv7Ym2YwFi9eAc5YJv37dgnE53h5M9wFeYGFiR4FtPQQ/BnF2g4QCW0IwTEGIISY8PX5dd2F5ZZqZmigDAgAClz04R5eFjiWmqKoRJos5rreTc0dliDZOuJ4SnFywWVuMnqa9Bb9ba6SUaoa7PclPdwNITn1FVd3DRNRm1tt6k2lk2Z9jZM7iNdBlxwcE3EgBaFNkiPe99Gg5SNPMizY64XrgQ/ILVIEABayhEMCt1UE1SAx+47LL/8cRAKikQTCRJ2EijEdM8COT7t/DHSJrvRGmYCMXGRiRCAEGpF4GZutkqANnIJU7lpmgBYp3gWDQoeAeHs1oqxcbpk1X5oDKZarOYh8BCGxqM1/JqGjJgNQTRyKHN13TynVSZywGoHPzRv0oB9M5vYDz8cGqAW9guYAEjXB6GG3YvotXNn4HcrAKro3DtiXcAW7mApUt0zAcWHMcxaMR6gUSWvSQYuuMyGbd2qAbJkasmNndendRziBMtRA6qnjx4cA7jxouoLnz586RZxpt41Sw2dizB4JJgll2r3uz28akejJi1B9gm59LMzi09eztNl0IPy07ELi/69+fJISihyK7BSjggATuBo9fxiWo4IJCIbjggxAm98iEFFZo4YUYDpIAADs='


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Homework 2 GUI')

        self.__queen_image = tk.PhotoImage(data=QUEEN_IMAGE)
        self.__menu = tk.Menu(self)
        self.config(menu=self.__menu)
        self.__menu.add_command(label='N-Queens', command=self.init_n_queens)
        self.__canvas = tk.Canvas(self)
        self.__buttons = tk.Frame(self)
        self.__cur_sol = 0

    def init_n_queens(self):
        n = simpledialog.askinteger('Input number', 'N', parent=self)
        if not n or n <= 0:
            return
        self.__canvas.delete(tk.ALL)
        for c in self.__buttons.winfo_children():
            c.destroy()
        pixel_per_block = self.__queen_image.width()
        self.__canvas.config(width=n * pixel_per_block, height=n * pixel_per_block)
        self.__canvas.pack()

        for i in range(n):
            for j in range(n):
                self.__canvas.create_rectangle(
                    i * pixel_per_block, j * pixel_per_block,
                    (i + 1) * pixel_per_block, (j + 1) * pixel_per_block,
                    fill='gray50' if (i & 1) ^ (j & 1) else 'white', outline='')

        solutions = n_queens_solutions(n)
        if not solutions:
            messagebox.showwarning('Warning', 'No solutions returned!')
            return

        queens = []
        self.__cur_sol = 0
        label = tk.StringVar()

        def display(proc):
            while queens:
                self.__canvas.delete(queens.pop())
            self.__cur_sol += proc
            if self.__cur_sol <= 0:
                prev_btn.config(state=tk.DISABLED)
            else:
                prev_btn.config(state=tk.NORMAL)
            if self.__cur_sol + 1 >= len(solutions):
                next_btn.config(state=tk.DISABLED)
            else:
                next_btn.config(state=tk.NORMAL)
            label.set('%d/%d' % (self.__cur_sol + 1, len(solutions)))
            for i, pos in enumerate(solutions[self.__cur_sol]):
                queens.append(self.__canvas.create_image(
                    (i * pixel_per_block, pos * pixel_per_block), image=self.__queen_image, anchor=tk.NW))

        prev_btn = tk.Button(self.__buttons, text='Previous solution', command=partial(display, -1))
        next_btn = tk.Button(self.__buttons, text='Next solution', command=partial(display, 1))

        display(0)

        prev_btn.grid(row=0, column=0, padx=2, pady=2)
        next_btn.grid(row=0, column=1, padx=2, pady=2)
        tk.Label(self.__buttons, textvariable=label).grid(row=0, column=2, padx=2, pady=2)
        self.__buttons.pack(side=tk.BOTTOM)


if __name__ == '__main__':
    GUI().mainloop()
