import tkinter as tk
from tkinter.constants import ANCHOR, CENTER

class Card:
    def __init__(self, canvas):
        self.canvas = canvas
        self.points = 1
        self.position = (0,0)
        self.width = 200
        self.height = 100
        self.desc = 'Description'
        self.draw()
    
    def setDescription(self, desc):
        self.desc = desc
    
    def draw(self):
        self.canvas_text = self.canvas.create_text(self.position[0] + self.width/2, self.position[1] + self.height/2, anchor=CENTER, text=self.desc, fill='red')
        self.canvas_rect = self.canvas.create_rectangle(self.position[0], self.position[1], self.position[0] + self.width, self.position[1] + self.height, outline='red')

    def move(self, x, y):
        self.position = (x,y)
        self.canvas.coords(self.canvas_text, x + self.width/2, y + self.height/2)
        self.canvas.coords(self.canvas_rect, x, y, x + self.width, y + self.height)

class Kanban:
    def __init__(self):
        self.root = tk.Tk()
        #root.attributes('-fullscreen', True)
        self.root.title("True Kanban")
        self.root.configure(background='red')
        self.canvas = tk.Canvas(self.root, bg='black', width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.bind('<Button-1>', self.handleClickDown)
        self.canvas.bind('<ButtonRelease-1>', self.handleClickUp)
        self.canvas.bind('<Double-Button-1>', self.handleDoubleClick)
        self.canvas.bind('<B1-Motion>', self.handleMouseMove)
        self.canvas.pack()
        self.grabbed_card = None
        self.grab_offset = None
        self.cards = []

        # For debugging purposes
        c = Card(self.canvas)
        self.cards.append(c)
        self.root.mainloop()

    def getColldingRectangle(self, mx, my):
        for c in self.cards:
            if mx > c.position[0] and mx < c.position[0] + c.width and my > c.position[1] and my < c.position[1] + c.height:
                print("HIT | ", c.desc)
                return c

    def handleClickDown(self, event):
        print("DOWN: ",event.x, event.y)
        self.grabbed_card = self.getColldingRectangle(event.x, event.y)
        self.grab_offset = (event.x - self.grabbed_card.position[0], event.y - self.grabbed_card.position[1])

    def handleClickUp(self, event):
        print("UP: ",event.x, event.y)
        #self.grabbed_card.position = self.grabbed_card.canvas_rect.position
        self.grabbed_card = None
        self.grab_offset = None

    def handleDoubleClick(self, event):
        print("Double-Click: ", event.x, event.y)
        edit_card = self.getColldingRectangle(event.x, event.y)
        if edit_card:
            pass

    def handleMouseMove(self, event):
        if self.grabbed_card:
            move_pos = (event.x - self.grab_offset[0], event.y - self.grab_offset[1])
            self.grabbed_card.move(move_pos[0], move_pos[1])
            print("AAA")

k = Kanban()