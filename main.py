import tkinter as tk
from tkinter.constants import ANCHOR, CENTER
from tkinter import simpledialog

HEADERFONT = 'Consolas'
CARDFONT = 'Courier'
SECTIONCOLOR = 'red'
CARDCOLOR = 'cyan'

class Card:
    def __init__(self, canvas):
        self.canvas = canvas
        self.points = 1
        self.position = (10,35)
        self.width = 180
        self.height = 100
        self.desc = 'Description'
        self.canvas_text = None
        self.canvas_rect = None
        self.draw()
    
    def setDescription(self, desc):
        self.desc = desc
        self.canvas.itemconfig(self.canvas_text, text=desc)
    
    def draw(self):
        self.canvas_text = self.canvas.create_text(self.position[0] + self.width/2, self.position[1] + self.height/2, anchor=CENTER, text=self.desc, fill=CARDCOLOR, width=self.width, font=CARDFONT)
        self.canvas_rect = self.canvas.create_rectangle(self.position[0], self.position[1], self.position[0] + self.width, self.position[1] + self.height, outline=CARDCOLOR, dash=(1,150))

    def move(self, x, y):
        self.position = (x,y)
        self.canvas.coords(self.canvas_text, x + self.width/2, y + self.height/2)
        self.canvas.coords(self.canvas_rect, x, y, x + self.width, y + self.height)

class Section:
    def __init__(self, canvas, title, w, x, h, ch):
        self.canvas = canvas
        self.title = title
        self.width = w
        self.x_pos = x
        self.height = h
        self.card_height = ch
        self.draw()

    def draw(self):
        self.canvas_line = self.canvas.create_line(self.x_pos, 25, self.x_pos+self.width, 25, fill=SECTIONCOLOR)
        self.canvas_text = self.canvas.create_text(self.x_pos + self.width/2, 15, anchor=CENTER, text=self.title, fill=SECTIONCOLOR, width=self.width, font=HEADERFONT)
        self.canvas_rect = self.canvas.create_rectangle(self.x_pos, 0, self.x_pos + self.width, self.height, outline=SECTIONCOLOR)

    def setCard(self, card):
        card.width = self.width - 20
        card.height = self.card_height

class Kanban:
    def __init__(self):
        self.root = tk.Tk()
        #self.root.attributes('-fullscreen', True)
        self.root.title("True Kanban")
        self.root.geometry("800x480")
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
        self.sections = []
        # For debugging purposes
        s = Section(self.canvas, 'Ideation', 200,  0, self.root.winfo_screenheight(), 50)
        s2 = Section(self.canvas, 'In Progress', 400, 200, self.root.winfo_screenheight(), 150)
        s3 = Section(self.canvas, 'Finished', 200, 600, self.root.winfo_screenheight(), 100)
        self.sections.append(s)
        self.sections.append(s2)
        self.sections.append(s3)

        c = Card(self.canvas)
        self.cards.append(c)
        c2 = Card(self.canvas)
        self.cards.append(c2)
        c3 = Card(self.canvas)
        self.cards.append(c3)
        c4 = Card(self.canvas)
        self.cards.append(c4)
        c5 = Card(self.canvas)
        self.cards.append(c5)
        c6 = Card(self.canvas)
        self.cards.append(c6)
        c7 = Card(self.canvas)
        self.cards.append(c7)
        c8 = Card(self.canvas)
        self.cards.append(c8)
        c9 = Card(self.canvas)
        self.cards.append(c9)

        self.root.mainloop()

    def getCollidingSections(self, mx, my):
        for s in self.sections:
            if mx > s.x_pos and mx < s.x_pos + s.width:
                print("DROP | ", s.title)
                return s

    def getColldingCards(self, mx, my):
        for c in self.cards:
            if mx > c.position[0] and mx < c.position[0] + c.width and my > c.position[1] and my < c.position[1] + c.height:
                print("HIT | ", c.desc)
                return c

    def handleClickDown(self, event):
        print("DOWN: ",event.x, event.y)
        self.grabbed_card = self.getColldingCards(event.x, event.y)
        if self.grabbed_card:
            self.grab_offset = (event.x - self.grabbed_card.position[0], event.y - self.grabbed_card.position[1])

    def handleClickUp(self, event):
        print("UP: ", event.x, event.y)
        if self.grabbed_card:
            drop_zone = self.getCollidingSections(event.x, event.y)
            drop_zone.setCard(self.grabbed_card)
            self.grabbed_card.move(drop_zone.x_pos+10, 35)
            #self.root.update()
            self.grabbed_card = None
            self.grab_offset = None

    def handleDoubleClick(self, event):
        print("Double-Click: ", event.x, event.y)
        edit_card = self.getColldingCards(event.x, event.y)
        if edit_card:
            # add a color selector
            description = simpledialog.askstring(title="Test",prompt="What's your Name?:")  
            if description:
                edit_card.setDescription(description)

    def handleMouseMove(self, event):
        if self.grabbed_card:
            move_pos = (event.x - self.grab_offset[0], event.y - self.grab_offset[1])
            self.grabbed_card.move(move_pos[0], move_pos[1])

# Read Config File

k = Kanban()

# Load stuff onto the board

k.root.mainloop()
