__author__ = 'sondredyvik'
from Tkinter import *
from tkFileDialog import askopenfilename

import astarmod1
import board


class astarGui(Frame):
    def __init__(self, parent, rows, columns, size=10, color1="white", color2="white"):
        #These are all variables for the gui
        self.parent = Frame(parent, width=300, height=300)
        self.parent.pack()
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.rect_dict = {}
        self.running = False
        canvas_width = columns * size
        canvas_height = rows * size
        menubar = Menu(parent)
        self.oldsnake = None
        self.searchsnake = None
        self.board = None
        self.left_frame = Frame(self.parent)
        self.right_frame = Frame(self.parent, borderwidth=5, relief=RIDGE)
        self.canvas = Canvas(master=self.right_frame, borderwidth=0, highlightthickness=0, width=canvas_width,
                             height=canvas_height, background="bisque")

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="A-star", command=lambda: self.run("astar"))
        filemenu.add_command(label="Depth First", command=lambda: self.run("dfs"))
        filemenu.add_command(label="Breadth First", command=lambda: self.run("bfs"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)
        menubar.add_cascade(label="Algorithm", menu=filemenu)

        # create more pulldown menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Board 1", command=lambda: self.setBoard("boards/board1.txt"))
        editmenu.add_command(label="Board 2", command=lambda: self.setBoard("boards/board2.txt"))
        editmenu.add_command(label="Board 3", command=lambda: self.setBoard("boards/board3.txt"))
        editmenu.add_command(label="Board 4", command=lambda: self.setBoard("boards/board4.txt"))
        editmenu.add_command(label="Board 5", command=lambda: self.setBoard("boards/board5.txt"))
        editmenu.add_command(label="Board 6", command=lambda: self.setBoard("boards/board6.txt"))
        editmenu.add_command(label="Custom", command=lambda: self.openfile())
        menubar.add_cascade(label="Board", menu=editmenu)



        # display the menu
        parent.config(menu=menubar)

        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        # Pack GUI
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)


    def run(self, type):
        if (not self.running):
            if self.board is None:
                self.setBoard("boards/board1.txt")
            else:
                self.setBoard(self.board.filename)
            self.searchsnake = [] #used for visualisation
            self.oldsnake = []      #used for visualisation
            self.alg = astarmod1.Astarmod1(type, self.board) #create an instance of astar
            self.running = True
            self.do_one_step()


    def do_one_step(self):
        self.searchsnake = self.alg.do_one_step() # Performs one iteration of astar. The rest is gui
        if not self.oldsnake is None:
            for el in self.oldsnake:
                self.canvas.itemconfig(self.rect_dict[(int(el.xpos), int(self.board.dimensions[1]) - 1 - int(el.ypos))],
                                       fill="white")
        for state in self.alg.closeddict.values():
            self.canvas.itemconfig(
                self.rect_dict[(int(state.xpos), int(self.board.dimensions[1]) - 1 - (int(state.ypos)))], fill="grey")

        for elem in self.searchsnake:
            # self.canvas.itemconfig(self.rect_dict[(int(elem.xpos),int (elem.ypos))],fill="red")
            self.canvas.itemconfig(self.rect_dict[(int(elem.xpos), int(self.board.dimensions[1]) - 1 - int(elem.ypos))],
                                   fill="red")
            self.oldsnake = self.searchsnake
        if self.searchsnake[-1].h == 0:
            self.running = False
            return True


        self.parent.after(10, lambda: self.do_one_step())

    #The rest is gui
    def openfile(self):
        self.setBoard(askopenfilename(parent=self.parent))

    def drawBoard(self, board):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        xsize = (int(width / int(board.dimensions[0])))
        ysize = (int(height / int(board.dimensions[1])))
        self.size = min(xsize, ysize)
        self.canvas.delete('square')
        for x in range(int(board.dimensions[0])):
            for y in reversed(range(int(board.dimensions[1]))):
                x1 = (x * self.size)
                y1 = (y * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.rect_dict[(x,y)] = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white",
                                                                      tags="square")
        for i in range(int(board.dimensions[0])):
            for j in range(int(board.dimensions[1])):
                if board.grid[i][j] == "#":
                    # self.canvas.itemconfig(self.rect_dict[i,j],fill="black")
                    self.canvas.itemconfig(self.rect_dict[(i, int(self.board.dimensions[1]) - 1 - j)], fill="black")
                if board.grid[i][j] == "G":
                    self.canvas.itemconfig(self.rect_dict[(i, int(self.board.dimensions[1]) - 1 - j)], fill="green")
                if board.grid[i][j] == "S":
                    self.canvas.itemconfig(self.rect_dict[(i, int(self.board.dimensions[1]) - 1 - j)], fill="blue")

    def setBoard(self, filename):
        self.board = board.Board(filename)
        self.drawBoard(self.board)
        self.running = False


root = Tk()
gui = astarGui(root, 32, 32)
root.mainloop()