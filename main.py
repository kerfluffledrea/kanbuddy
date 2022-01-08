import tkinter as tk
from tkinter.constants import ANCHOR, BOTH, BOTTOM, CENTER, FLAT, LEFT, NW, W
from tkinter import Frame, Toplevel, simpledialog
from tkinter import Entry, Text, Button

HEADERFONT = 'Courier'
CARDFONT = 'Consolas'
MAINCOLOR = 'blueviolet'
SECONDARYCOLOR = 'cyan'
MARGIN = 10
WIDTH = 800
HEIGHT = 480
HEADERSIZE = 25

class Card:
    def __init__(self, canvas):
        self.canvas = canvas
        self.points = 1
        self.position = (0,0)
        self.width = 180
        self.height = 100

        self.description = '-[O-O]- Hello'
        self.color = SECONDARYCOLOR
        self.points = 1

        self.canvas_text = None
        self.canvas_rect = None
        self.section_index = 0
        self.draw()
    
    def setColor(self, color):
        self.color = color
        self.canvas.itemconfig(self.canvas_text, fill=color)
        self.canvas.itemconfig(self.canvas_rect, outline=color)

    def setDescription(self, desc):
        self.description = desc
        self.canvas.itemconfig(self.canvas_text, text=desc)
    
    def draw(self):
        self.canvas_text = self.canvas.create_text(self.position[0] + self.width/2, self.position[1] + self.height/2, anchor=CENTER, text=self.description, fill=self.color, width=self.width-MARGIN*2, font=CARDFONT)
        self.canvas_rect = self.canvas.create_rectangle(self.position[0], self.position[1], self.position[0] + self.width, self.position[1] + self.height, outline=self.color)

    def move(self, x, y):
        self.position = (x,y)
        self.canvas.itemconfig(self.canvas_text, width=self.width-MARGIN*2)
        self.canvas.coords(self.canvas_text, x + self.width/2, y + self.height/2)
        self.canvas.coords(self.canvas_rect, x, y, x + self.width, y + self.height)

class DropZone:
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

class Section:
    def __init__(self, canvas, title, w, x, ch):
        self.canvas = canvas
        self.title = title
        self.width = w
        self.x_pos = x
        self.card_height = ch
        self.drop_zones = []
        self.cards = []
        self.draw()
        self.createDropZones()

    def draw(self):
        self.canvas_line = self.canvas.create_line(self.x_pos, HEADERSIZE, self.x_pos+self.width, HEADERSIZE, fill=MAINCOLOR)
        self.canvas_text = self.canvas.create_text(self.x_pos + self.width/2, 15, anchor=CENTER, text=self.title, fill=MAINCOLOR, width=self.width, font=(HEADERFONT, 15, 'bold'))
        self.canvas_rect = self.canvas.create_rectangle(self.x_pos, 0, self.x_pos + self.width, HEIGHT, outline=MAINCOLOR)

    def createDropZones(self):
        i = 0
        while True:
            xpos = self.x_pos + MARGIN
            ypos = HEADERSIZE + self.card_height * i + MARGIN * (i + 1)
            if ypos + self.card_height > HEIGHT:
                break
            self.drop_zones.append(DropZone(xpos, ypos, self.width - MARGIN * 2, self.card_height))
            self.canvas.create_rectangle(xpos, ypos, xpos + self.width - MARGIN * 2, ypos + self.card_height, outline = 'grey4')
            i += 1

    def addCard(self, card):
        dz_index = len(self.cards)
        card.width = self.drop_zones[dz_index].width
        card.height = self.drop_zones[dz_index].height
        card.move(self.drop_zones[dz_index].x_pos, self.drop_zones[dz_index].y_pos)
        self.cards.append(card)

    def removeCard(self, card):
        self.cards.remove(card)
        i = 0
        for card in self.cards:
            card.width = self.drop_zones[i].width
            card.height = self.drop_zones[i].height
            card.move(self.drop_zones[i].x_pos, self.drop_zones[i].y_pos)
            i += 1

class Kanban:
    def __init__(self):
        self.root = tk.Tk()
        #self.root.attributes('-fullscreen', True)
        self.root.title("Kanbuddy")
        self.root.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.root.configure(background='red')
        self.canvas = tk.Canvas(self.root, bg='black', width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.bind('<Control-a>', self.addNewCard)
        self.canvas.bind('<Button-1>', self.handleClickDown)
        self.canvas.bind('<ButtonRelease-1>', self.handleClickUp)
        self.canvas.bind('<Double-Button-1>', self.handleDoubleClick)
        self.canvas.bind('<B1-Motion>', self.handleMouseMove)
        self.canvas.pack()
        self.cards = []
        self.sections = []

        self.edit_menu = None
        self.grabbed_card = None
        self.grab_offset = None
        self.grabbed_card_section = None

        # For debugging purposes
        s = Section(self.canvas, 'TODO', 200,  0, 100)
        s2 = Section(self.canvas, 'IN PROGRESS', 400, 200, 135)
        s3 = Section(self.canvas, 'FINISHED', 200, 600, 100)
        self.sections.append(s)
        self.sections.append(s2)
        self.sections.append(s3)
        # ---

        self.root.mainloop()

    def getCollidingSections(self, mx, my):
        for s in self.sections:
            if mx > s.x_pos and mx < s.x_pos + s.width:
                return s
            
    def getColldingCards(self, mx, my):
        for c in self.cards:
            if mx > c.position[0] and mx < c.position[0] + c.width and my > c.position[1] and my < c.position[1] + c.height:
                return c
    
    def openEditMenu(self, edit_card):
        self.edit_menu = Frame(self.root, bg='black', highlightcolor=MAINCOLOR, highlightbackground=MAINCOLOR, highlightthickness=1, height=edit_card.height-1, width=edit_card.width-1)
        self.edit_menu.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        description_entry = Text(self.edit_menu, height=3, width=30, bg='black', bd=0, highlightcolor=MAINCOLOR, fg=MAINCOLOR)
        description_entry.insert(tk.END, edit_card.description)
        description_entry.pack(padx=MARGIN, pady=MARGIN)
        
        button_grid = Frame(self.edit_menu)
        button_grid.pack(padx=MARGIN, pady=MARGIN)
        wb = Button(button_grid, bg='white', width=5, height=2, command=lambda: edit_card.setColor('white')).grid(column=0, row=0)
        lb = Button(button_grid, bg='lime', width=5, height=2, command=lambda: edit_card.setColor('lime')).grid(column=1, row=0)
        cb = Button(button_grid, bg='cyan', width=5, height=2, command=lambda: edit_card.setColor('cyan')).grid(column=2, row=0)
        vb = Button(button_grid, bg='violetred1', width=5, height=2, command=lambda: edit_card.setColor('violetred1')).grid(column=3, row=0)
        rb = Button(button_grid, bg='magenta', width=5, height=2, command=lambda: edit_card.setColor('magenta')).grid(column=4, row=0)
        yb = Button(button_grid, bg='yellow', width=5, height=2, command=lambda: edit_card.setColor('yellow')).grid(column=5, row=0)

        close_button = Button(self.edit_menu, text='Save', fg='white', bg='black', width=10, height=2,highlightbackground='white', command=lambda: self.closeEditMenu(edit_card, description_entry.get("1.0","end-1c")))
        close_button.pack(expand=True, fill=BOTH, pady=MARGIN, padx=MARGIN)
        self.canvas.create_window(WIDTH/2, HEIGHT/2, anchor=CENTER, window=self.edit_menu)

    def closeEditMenu(self, edit_card, desc):
        edit_card.setDescription(desc)
        self.edit_menu.destroy()
        self.edit_menu = None

    def addNewCard(self, event):
        if not self.edit_menu:
            if len(self.sections[0].cards) < len(self.sections[0].drop_zones):
                c = Card(self.canvas)
                self.cards.append(c)
                self.sections[0].addCard(c)
                return c

    def handleClickDown(self, event):
        if not self.edit_menu:
            self.grabbed_card = self.getColldingCards(event.x, event.y)
            if self.grabbed_card:
                self.grab_offset = (event.x - self.grabbed_card.position[0], event.y - self.grabbed_card.position[1])
                self.grabbed_card_section = self.sections[self.grabbed_card.section_index]

    def handleClickUp(self, event):
        if not self.edit_menu:
            if self.grabbed_card:
                drop_section = self.getCollidingSections(event.x, event.y)
                if drop_section and len(drop_section.cards) < len(drop_section.drop_zones) and self.sections.index(drop_section) != self.grabbed_card.section_index:
                    self.grabbed_card.section_index = self.sections.index(drop_section)
                    drop_section.addCard(self.grabbed_card)
                    self.grabbed_card_section.removeCard(self.grabbed_card)
                else:
                    self.grabbed_card_section.removeCard(self.grabbed_card)
                    self.grabbed_card_section.addCard(self.grabbed_card)
                self.grabbed_card = None
                self.grab_offset = None
                self.grabbed_card_section = None
    
    def handleDoubleClick(self, event):
        if not self.edit_menu:
            edit_card = self.getColldingCards(event.x, event.y)
            if edit_card:
                self.openEditMenu(edit_card)

    def handleMouseMove(self, event):
        if self.grabbed_card:
            move_pos = (event.x - self.grab_offset[0], event.y - self.grab_offset[1])
            self.grabbed_card.move(move_pos[0], move_pos[1])

# Read Config File

k = Kanban()

# Load stuff onto the board

k.root.mainloop()
