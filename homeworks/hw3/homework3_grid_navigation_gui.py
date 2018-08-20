import sys
import Tkinter

import homework3

class Grid(Tkinter.Canvas):

    def __init__(self, master, scene, start_and_goal):
        self.rows, self.cols = len(scene), len(scene[0])
        self.square_size = min(40, 500 / self.rows, 500 / self.cols)
        Tkinter.Canvas.__init__(self, master,
            height=self.square_size * self.rows + 1,
            width=self.square_size * self.cols + 1, background="white")
        self.draw_scene(scene)
        self.scene = scene
        self.start_and_goal = start_and_goal
        self.bind("<Button-1>", self.left_click)
        self.bind("<Button-2>", self.right_click)
        self.bind("<Button-3>", self.right_click)
        self.focus_set()
        self.configure(highlightthickness=0)

    def draw_scene(self, scene):
        for row in range(len(scene)):
            for col in range(len(scene[0])):
                x0, y0 = col * self.square_size, row * self.square_size
                x1, y1 = x0 + self.square_size, y0 + self.square_size
                self.create_rectangle(x0, y0, x1, y1, width=1, outline="black",
                    fill="gray50" if scene[row][col] else "white")

    def transform(self, (row, col)):
        x = self.square_size * (col + 0.5)
        y = self.square_size * (row + 0.5)
        return (x, y)

    def inverse_transform(self, event):
        row = event.y / self.square_size
        col = event.x / self.square_size
        return (row, col)

    def left_click(self, event):
        row, col = point = self.inverse_transform(event)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if not self.scene[row][col]:
                self.delete("start")
                self.draw_point(point, color="red", tags="start")
                self.start_and_goal[0] = point
                if point == self.start_and_goal[1]:
                    self.delete("goal")
                    self.start_and_goal[1] = None

    def right_click(self, event):
        row, col = point = self.inverse_transform(event)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if not self.scene[row][col]:
                self.delete("goal")
                self.draw_point(point, color="green", tags="goal")
                self.start_and_goal[1] = point
                if point == self.start_and_goal[0]:
                    self.delete("start")
                    self.start_and_goal[0] = None

    def draw_point(self, point, color="black", tags=""):
        x, y = self.transform(point)
        radius = self.square_size / 4.0
        return self.create_oval(x - radius, y - radius, x + radius, y + radius,
            fill=color, tags=tags)

    def draw_line(self, p, q, color="black", width=1, arrow=None, tags=""):
        p_x, p_y = self.transform(p)
        q_x, q_y = self.transform(q)
        return self.create_line(p_x, p_y, q_x, q_y, fill=color, width=width,
            arrow=arrow, tags=tags)

    def draw_path(self, path):
        for p, q in zip(path, path[1:]):
            self.draw_line(p, q, color="blue", width=2, arrow=Tkinter.LAST,
                tags="path")

    def clear_paths(self):
        self.delete("path")

class GridNavigationGUI(Tkinter.Frame):

    def __init__(self, master, scene):

        Tkinter.Frame.__init__(self, master)

        self.scene = scene
        self.start_and_goal = [None, None]

        self.grid = Grid(self, scene, self.start_and_goal)
        self.grid.pack(side=Tkinter.LEFT, padx=1, pady=1)

        menu = Tkinter.Frame(self)

        Tkinter.Label(menu, text="Left click to specify the start point.").pack(
            padx=1, pady=1, anchor=Tkinter.W)
        Tkinter.Label(menu, text="Right click to specify the goal point.").pack(
            padx=1, pady=1, anchor=Tkinter.W)

        Tkinter.Button(menu, text="Find Path", command=self.find_path_click).pack(
            fill=Tkinter.X, padx=1, pady=1)
        Tkinter.Button(menu, text="Clear Paths", command=self.clear_paths_click).pack(
            fill=Tkinter.X, padx=1, pady=1)
        
        menu.pack(side=Tkinter.RIGHT)

    def find_path_click(self):
        start, goal = self.start_and_goal
        if start is not None and goal is not None:
            path = homework3.find_path(start, goal, self.scene)
            if path:
                self.grid.draw_path(path)

    def clear_paths_click(self):
        self.grid.clear_paths()

def load_scene(scene_path):
    scene = []
    with open(scene_path) as infile:
        for row, line in enumerate(infile, start=1):
            scene.append([])
            for col, char in enumerate(line.strip(), start=1):
                if char == ".":
                    scene[-1].append(False)
                elif char == "X":
                    scene[-1].append(True)
                else:
                    print ("Unrecognized character '%s' at line %d, column %d" %
                        (char, row, col))
                    return None
    if len(scene) < 1:
        print "Scene must have at least one row"
        return None
    if len(scene[0]) < 1:
        print "Scene must have at least one column"
        return None
    if not all(len(row) == len(scene[0]) for row in scene):
        print "Not all rows are of equal length"
        return None
    return scene

if __name__ == "__main__":
    root = Tkinter.Tk()
    root.title("Grid Navigation")
    scene = load_scene(sys.argv[1])
    if scene is not None:
        GridNavigationGUI(root, scene).pack()
        root.resizable(height=False, width=False)
        root.mainloop()
