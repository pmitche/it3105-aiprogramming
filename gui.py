__author__ = 'sondredyvik'
from Tkinter import *
import sys



class astarGui(Frame):
    def __init__(self, parent,rows,columns,size=32,color1="white",color2="white"):
        self.color_to_type_map = {"ordinary":"white","wall":"black","goal":"green","start":"blue"}
        self.parent = Frame(parent,width =300, height = 300)
        self.parent.pack()
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        canvas_width = columns * size
        canvas_height = rows * size
        self.nodes = [[Node("ordinary", j, i) for j in range(columns)] for i in range (rows)]

        self.left_frame = Frame(self.parent)
        self.right_frame = Frame(self.parent,borderwidth = 5, relief =RIDGE)
        self.canvas = Canvas(master=self.right_frame, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        #Creating buttons and entry fields
        self.run_button = Button(self.left_frame,text="Run")
        self.add_start_button = Button(self.left_frame,text="start")
        self.start_entry = Entry(self.left_frame)
        self.add_end_button = Button(self.left_frame,text="end")
        self.goal_entry = Entry(self.left_frame)
        self.add_obstacle_button=Button(self.left_frame,text="obstacle")
        self.obstacle_entry = Entry(self.left_frame)

        #Packing buttons to UI
        self.add_start_button.pack()
        self.start_entry.pack()
        self.add_end_button.pack()
        self.goal_entry.pack()
        #Packing buttons and displaying text on entryfields
        self.start_entry.insert(0,"Startpos(0,0)")
        self.goal_entry.insert(0,"Goalpos (0,0)")
        self.add_obstacle_button.pack()
        self.obstacle_entry.pack()
        self.run_button.pack()
        self.obstacle_entry.insert(0,"Obstacle(0,0,0,0)")


        #Binding buttons
        self.add_end_button.bind("<Button-1>",self.goalbuttonclick)
        self.add_start_button.bind("<Button-1>",self.startbuttonclick)
        self.add_obstacle_button.bind("<Button-1>",self.obstaclebuttonclick)
        self.run_button.bind("<Button-1>",self.runprogram)
        #Pack GUI
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)
        self.parent.bind("<Configure>", self.refresh_a)

    def getGoalNode(self):
        for i in self.nodes:
            for j in i:
                if j.type =="goal":
                    return j

    def runprogram(self,event):
        self.obstacle_entry.destroy()
        self.add_obstacle_button.destroy()
        for i in self.nodes:
            for j in i:
                j.calculateHeuristic(self.getGoalNode())
        return
    def obstaclebuttonclick(self,event):
        pos = self.obstacle_entry.get()
        if len(self.readInput(pos))!= 4:
            print "Wrong input"
            return
        values = self.readInput(pos)
        x = int(values[0])
        y = int(values[1])
        width = int(values[2])
        height = int(values[3])
        for i in range(x, x+width):
            for j in range(y,y+height):
                self.nodes[i][j].type ="wall"
        self.refresh(self.canvas.winfo_width(),self.canvas.winfo_height())

    #startbuttonclick handler
    def startbuttonclick(self,event):
        pos = self.start_entry.get()
        if len(self.readInput(pos))!= 2:
            print "Wrong input"
            return
        coords = self.readInput(pos)
        x = int(coords[0])
        y = int(coords[1])
        self.nodes[x][y].type="start"
        self.refresh(self.canvas.winfo_width(),self.canvas.winfo_height())
        self.add_start_button.destroy()
        self.start_entry.destroy()

    #Goalbuttonclick handler
    def goalbuttonclick(self,event):
        pos = self.goal_entry.get()
        if len(self.readInput(pos))!= 2:
            print "Wrong input"
            return
        coords = self.readInput(pos)
        x = int(coords[0])
        y=int(coords[1])
        self.nodes[x][y].type="goal"
        print type(self.canvas.winfo_width()-1),self.canvas.winfo_height()
        self.refresh(self.canvas.winfo_width(),self.canvas.winfo_height())
        self.add_end_button.destroy()
        self.goal_entry.destroy()

    def readInput(self,string):
        return string.translate(None,'()').split(',')


    def refresh_a(self,event):
        self.refresh(event.width-1,event.height-1)

    def refresh(self, width,height):
        '''Redraw the board, possibly in response to window being resized'''

        xsize = int(width / self.columns)
        ysize = int(height / self.rows)
        print xsize
        self.size = min(xsize, ysize)

        self.canvas.delete("square")

        for row in range(self.rows):
            for col in range(self.columns):
                #draws squares
                x1 = (col * self.size)
                y1 = (row *self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                ##QUICK HACK TO PUT ORIGO IN LOWER LEFT CORNER
                color = self.color_to_type_map[self.nodes[self.rows-1-row][col].type]
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")


class Node():
    def __init__(self,type,xpos,ypos):
        self.f = None
        self.g = float('inf')
        self.h = None
        self.type =type
        self.xpos = xpos
        self.ypos = ypos
        self.parent = None
    def __repr__(self):
        return self.type
    def reparent(self, parent):
        self.parent = parent
    def calculateHeuristic(self,goalnode):
        self.h = abs(self.xpos - goalnode.xpos)+ abs (self.ypos - goalnode.ypos)
    def calculateNeighbours(self):
        return





class astar():
    def __init__(self,nodes):
        return


root =Tk()
gui = astarGui(root,int(sys.argv[1]),int(sys.argv[2]))
root.mainloop()