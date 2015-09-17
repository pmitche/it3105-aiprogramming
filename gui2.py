import Tkinter as tk

##GameBoard class taken and modified from http://stackoverflow.com/questions/4954395/create-board-game-like-grid-in-python

class GameBoard(tk.Frame):
    def __init__(self, parent, rows, columns, size=32, color1="gray", color2="gray"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2



        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<ButtonPress-1>",self.test)

    def test(self,event):
        xsize = int((self.canvas.winfo_width()-1/self.columns))
        ysize = int((self.canvas.winfo_height()/self.rows))
        self.size= min(xsize,ysize)
        rowCount = 0
        colCount = 0
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                if x2 > event.x > x1 and y2>event.y>y1:
                    print rowCount,colCount
                colCount +=1
            colCount = 0
            rowCount +=1








    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        print event.width
        print self.canvas.winfo_width()



        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        print xsize
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2






def readmap():
    rows = int(raw_input("Rows:"))
    columns= int(raw_input("Columns:"))
    obstacleList = []

    while True:
        answer = raw_input("Do you want to add another obstacle? Y/N ")
        if (answer =="y"or answer == "y"):
            obstacleList.append(raw_input("Give an obstacle on the form (x,x,x,x)"))
        else:
            break

    print obstacleList




    grid = [[None for x in range (columns)]for x in range(rows)]
    for i in grid:
        print i



def main():
    root = tk.Tk()
    board = GameBoard(root,16,16)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    root.mainloop()




main()