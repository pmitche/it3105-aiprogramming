from tkinter import *

from Modul6.board import Board

GRID_LEN              = 4
GRID_PADDING          = 10
SIZE                  = 500

BACKGROUND_COLOR_GAME       = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
FONT                        = ("Verdana", 40, "bold")
BACKGROUND_COLOR_DICT       = { 
                                2  : '#eee4da',
                                4  : '#ede0c8',
                                8  : '#f2b179',
                                16  : '#f59563',
                                32 : '#f67c5f',
                                64  : '#f65e3b',
                                128  : '#edcf72',
                                256  : '#edcc61',
                                512  : '#edc850',
                                1024 : '#edc53f',
                                2048 : '#FFAE00',
                                4096 : '#FFAE00',
                                8192 : '#FFAE00',

                            }





class GameWindow(Frame):
    def __init__(self):
        Frame.__init__(self)


        self.grid()
        self.master.title('2048')
        self.board = Board()

        self.board.place_tile(self.board.state)
        self.grid_cells = []
        self.init_grid()
        self.update_view(self.board.state.board)
        self.bind("<KeyPress>", self.onKeyPress)




    #end
    def onKeyPress(self,direction):
        if self.board.move(direction, self.board.state):
            self.update_view(self.board.state.board)
            self.board.place_tile(self.board.state)
            self.update_view(self.board.state.board)



    def do_one_move(self):
        move = self.expectimax.recommend_move(self.board.state, 3)
        if self.board.move(move,self.board.state):

            self.board.place_tile(self.board.state)
            self.update_view(self.board.state.board)
            self.after(10, lambda  : self.do_one_move())
        else:

            print ("FAIL")




    def init_grid(self):
        background = Frame(self, bg = BACKGROUND_COLOR_GAME, width = SIZE, height = SIZE )
        background.grid()
        
        for i in range(GRID_LEN):
            # Loop rows
            grid_row = []
            
            for j in range(GRID_LEN):
                # Loop columns
                cell = Frame( 
                            background, 
                            bg     = BACKGROUND_COLOR_CELL_EMPTY, 
                            width  = SIZE/GRID_LEN, 
                            height = SIZE/GRID_LEN)

                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            
            self.grid_cells.append(grid_row)
    #end
    
    def update_view(self, board ):
        for i in range( GRID_LEN ):
            for j in range( GRID_LEN ):
                digit = board[i][j]
                if digit == 0:
                    self.grid_cells[i][j].configure(
                                                text = "",
                                                bg   = BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    foreground_color = '#f9f6f2' if digit > 4 else '#776e65'
                    number = digit # the human friendly representation
                    
                    self.grid_cells[i][j].configure(
                                                text = str( digit),
                                                bg   = BACKGROUND_COLOR_DICT[ digit ],
                                                fg   = foreground_color )
        self.update_idletasks()






