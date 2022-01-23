import json
import csv
import os.path
from datetime import date
import tkinter as tk
from tkinter.constants import BOTH, CENTER
from tkinter import W, Frame, Text, Button

HEADERFONT = 'Courier'
CARDFONT = 'Consolas'
COUNTERFONT = 'Consolas'
MAINCOLOR = 'blueviolet'
SECONDARYCOLOR = 'white'
MARGIN = 10
WIDTH = 800
HEIGHT = 480
HEADERSIZE = 25
DAYCOUNTER = 1

class Card:
    def __init__(self, canvas, desc='-[O-O]- Hello', color=SECONDARYCOLOR, points=1, creation_date = date.today()):
        self.canvas = canvas
        self.description = desc
        self.color = color
        self.points = points
        self.creation_date = creation_date
        self.position = (0,0)
        self.width = 5
        self.height = 5
        self.canvas_text = None
        self.canvas_rect = None
        self.canvas_lines = []
        self.section_index = 0
        self.draw()
    
    def clearCanvas(self):
        self.canvas.delete(self.canvas_text)
        self.canvas.delete(self.canvas_rect)
        for l in self.canvas_lines:
            self.canvas.delete(l)
        if DAYCOUNTER:
            self.canvas.delete(self.canvas_dayctr)

    def setColor(self, color):
        self.color = color
        self.canvas.itemconfig(self.canvas_text, fill=color)
        self.canvas.itemconfig(self.canvas_rect, outline=color)
        for l in self.canvas_lines:
            self.canvas.itemconfig(l, fill=color)
        if DAYCOUNTER:
            self.canvas.itemconfig(self.canvas_dayctr, fill=color)

    def updateCounter(self):
        self.canvas.itemconfig(self.canvas_dayctr, text=(date.today() - self.creation_date).days)

    def setDescription(self, desc):
        self.description = desc
        self.canvas.itemconfig(self.canvas_text, text=desc)
    
    def increasePoints(self):
        if self.points < 10:
            self.points += 1
            self.canvas_lines.append(self.canvas.create_line(self.position[0] + self.width, self.position[1] + self.height - self.points*MARGIN,
                    self.position[0] + self.width - self.points*MARGIN, self.position[1] + self.height, fill=self.color))

    def decreasePoints(self):
        if self.points > 0:
            self.points -= 1
            self.canvas.delete(self.canvas_lines.pop())

    def draw(self):
        self.canvas_text = self.canvas.create_text(self.position[0] + self.width/2, self.position[1] + self.height/2, anchor=CENTER, text=self.description, fill=self.color, width=self.width-MARGIN*2, font=CARDFONT)
        self.canvas_rect = self.canvas.create_rectangle(self.position[0], self.position[1], self.position[0] + self.width, self.position[1] + self.height, outline=self.color)
        i = 0
        if DAYCOUNTER:
            self.canvas_dayctr = self.canvas.create_text(self.position[0] + 5, self.position[1] + 7, anchor=W, text=(date.today() - self.creation_date).days, fill=self.color, width=self.width-MARGIN*2, font=(COUNTERFONT, 9))
        while i < self.points+1:
            self.canvas_lines.append(self.canvas.create_line(self.position[0] + self.width, self.position[1] + self.height - i*MARGIN,
                self.position[0] + self.width - i*MARGIN, self.position[1] + self.height, fill=self.color))
            i += 1

    def move(self, x, y):
        self.position = (x,y)
        self.canvas.itemconfig(self.canvas_text, width=self.width-MARGIN*2)
        self.canvas.coords(self.canvas_text, x + self.width/2, y + self.height/2)
        self.canvas.coords(self.canvas_rect, x, y, x + self.width, y + self.height)
        i = 0
        for l in self.canvas_lines:
            self.canvas.coords(l, self.position[0] + self.width, self.position[1] + self.height - i*MARGIN,
                self.position[0] + self.width - i*MARGIN, self.position[1] + self.height)
            i += 1
        if DAYCOUNTER:
            self.canvas.coords(self.canvas_dayctr, x + 5, y + 10)

class DropZone:
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

class Section:
    def __init__(self, canvas, name, w, x, ch):
        self.canvas = canvas
        self.name = name
        self.width = w
        self.x_pos = x
        self.card_height = ch
        self.drop_zones = []
        self.cards = []
        self.draw()
        self.createDropZones()

    def draw(self):
        self.canvas_line = self.canvas.create_line(self.x_pos, HEADERSIZE, self.x_pos+self.width, HEADERSIZE, fill=MAINCOLOR)
        self.canvas_text = self.canvas.create_text(self.x_pos + self.width/2, 15, anchor=CENTER, text=self.name, fill=MAINCOLOR, width=self.width, font=(HEADERFONT))
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
        self.root.resizable(False, False)
        #self.root.attributes('-fullscreen', True)
        self.root.title("Kanbuddy")
        self.root.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.root.configure(background='red')
        self.canvas = tk.Canvas(self.root, bg='black', width=WIDTH, height=HEIGHT, highlightthickness=1, highlightbackground=MAINCOLOR)
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
        self.grab_location = None
        self.grabbed_card_section = None

    # --- File Reading/Writing ---
    def saveCardstoFile(self):
        with open('cards.csv', 'w', newline='\n') as cardfile:
            with open('archive.csv', 'a', newline='\n') as archivefile:
                cardwriter = csv.writer(cardfile, delimiter="|")
                archivewriter = csv.writer(archivefile, delimiter="|")
                cardwriter.writerow(['section_index', 'description', 'color', 'points', 'creation_date'])
                for c in self.cards:
                    if c.section_index == len(self.sections)-1:
                        archivewriter.writerow([c.description, c.points, (date.today() - self.creation_date).days])
                    else:
                        cardwriter.writerow([c.section_index, c.description, c.color, c.points, c.creation_date])

    def addSectionFromFile(self, name, width, xpos, cardheight):
        s = Section(self.canvas, name, width,  xpos, cardheight)
        self.sections.append(s)

    def addCardFromFile(self, section_index, description, color, points, creation_date):
        c = Card(self.canvas, description, color, points, creation_date)
        c.section_index = section_index
        self.sections[section_index].addCard(c)
        self.cards.append(c)

    # --- Collision Functions ---
    def getCollidingSections(self, mx, my):
        for s in self.sections:
            if mx > s.x_pos and mx < s.x_pos + s.width:
                return s
            
    def getColldingCards(self, mx, my):
        for c in self.cards:
            if mx > c.position[0] and mx < c.position[0] + c.width and my > c.position[1] and my < c.position[1] + c.height:
                return c

    # --- Card Editing ---
    def openEditMenu(self, edit_card):
        self.edit_menu = Frame(self.root, bg='black', highlightcolor=MAINCOLOR, highlightbackground=MAINCOLOR, highlightthickness=1, height=edit_card.height-1, width=edit_card.width-1)
        self.edit_menu.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        description_entry = Text(self.edit_menu, height=3, width=32, bg='black', bd=0, highlightbackground=MAINCOLOR, highlightcolor=MAINCOLOR, fg=MAINCOLOR)
        description_entry.insert(tk.END, edit_card.description)
        description_entry.pack(padx=MARGIN, pady=MARGIN)
        
        color_button_grid = Frame(self.edit_menu)
        color_button_grid.pack(padx=MARGIN, pady=0)
        b0 = Button(color_button_grid, bg=PALETTE[0], width=4, height=2, highlightbackground=MAINCOLOR, command=lambda: edit_card.setColor(PALETTE[0])).grid(column=0, row=0)
        b1 = Button(color_button_grid, bg=PALETTE[1], width=4, height=2, highlightbackground=MAINCOLOR, command=lambda: edit_card.setColor(PALETTE[1])).grid(column=1, row=0)
        b2 = Button(color_button_grid, bg=PALETTE[2], width=4, height=2, highlightbackground=MAINCOLOR, command=lambda: edit_card.setColor(PALETTE[2])).grid(column=2, row=0)
        b3 = Button(color_button_grid, bg=PALETTE[3], width=4, height=2, highlightbackground=MAINCOLOR, command=lambda: edit_card.setColor(PALETTE[3])).grid(column=3, row=0)
        b4 = Button(color_button_grid, bg=PALETTE[4], width=4, height=2, highlightbackground=MAINCOLOR, command=lambda: edit_card.setColor(PALETTE[4])).grid(column=4, row=0)
        b5 = Button(color_button_grid, bg=PALETTE[5], width=4, height=2, highlightbackground=MAINCOLOR, command=lambda: edit_card.setColor(PALETTE[5])).grid(column=5, row=0)
        b6 = Button(color_button_grid, bg=PALETTE[6], width=4, height=2, highlightbackground=MAINCOLOR, command=lambda: edit_card.setColor(PALETTE[6])).grid(column=6, row=0)

        bottom_button_grid = Frame(self.edit_menu, background='black')
        bottom_button_grid.pack(expand=True, fill=BOTH, pady=MARGIN/2, padx=MARGIN)
        decrease_points = Button(bottom_button_grid, text='-', fg='white', bg='black', width=4, height=2, highlightbackground=MAINCOLOR, command=lambda: edit_card.decreasePoints()).grid(column=1, row=0)
        increase_points = Button(bottom_button_grid, text='+', fg='white', bg='black', width=4, height=2, highlightbackground=MAINCOLOR, command=lambda: edit_card.increasePoints()).grid(column=2, row=0)
        close_button = Button(bottom_button_grid, text='SAVE', fg='white', bg='black', width=20, height=2, highlightbackground=MAINCOLOR, command=lambda: self.closeEditMenu(edit_card, description_entry.get("1.0","end-1c"))).grid(column=3, row=0, sticky='nesw')
        delete_button = Button(bottom_button_grid, text='DELETE', fg='white', bg='black', width=5, height=2, highlightbackground=MAINCOLOR, command=lambda: self.deleteCard(edit_card)).grid(column=4, row=0, sticky='nesw')
        self.canvas.create_window(WIDTH/2, HEIGHT/2, anchor=CENTER, window=self.edit_menu)

    def closeEditMenu(self, edit_card, desc):
        edit_card.setDescription(desc)
        self.edit_menu.destroy()
        self.edit_menu = None
        self.saveCardstoFile()

    def deleteCard(self, card):
        self.cards.remove(card)
        self.sections[card.section_index].cards.remove(card)
        self.edit_menu.destroy()
        self.edit_menu = None
        card.clearCanvas()
        del card
        self.saveCardstoFile()

    def updateCounters(self):
        for c in self.cards:
            c.updateCounter()

    # --- Event Handlers ---
    def addNewCard(self, event):
        if not self.edit_menu:
            if len(self.sections[0].cards) < len(self.sections[0].drop_zones):
                c = Card(self.canvas)
                self.cards.append(c)
                self.sections[0].addCard(c)
                self.saveCardstoFile()
                return c

    def handleClickDown(self, event):
        if not self.edit_menu:
            self.grabbed_card = self.getColldingCards(event.x, event.y)
            if self.grabbed_card:
                self.grab_offset = (event.x - self.grabbed_card.position[0], event.y - self.grabbed_card.position[1])
                self.grabbed_card_section = self.sections[self.grabbed_card.section_index]
                self.grab_location = (event.x, event.y)

    def handleClickUp(self, event):
        if DAYCOUNTER:
            self.updateCounters()
        if not self.edit_menu:
            if self.grabbed_card:
                drop_section = self.getCollidingSections(event.x, event.y)
                if drop_section and len(drop_section.cards) < len(drop_section.drop_zones) and self.sections.index(drop_section) != self.grabbed_card.section_index:
                    self.grabbed_card.section_index = self.sections.index(drop_section)
                    drop_section.addCard(self.grabbed_card)
                    self.grabbed_card_section.removeCard(self.grabbed_card)
                    if self.grabbed_card.section_index == len(self.sections)-1:
                        self.grabbed_card.setColor(SECONDARYCOLOR)
                else:
                    # This prevents the tiny movements during double clicks from moving cards around within a section
                    drag_vector = (event.x - self.grab_location[0],  event.y- self.grab_location[1])
                    if (drag_vector[0]**2 + drag_vector[1]**2) ** (1/2) > MARGIN:
                        self.grabbed_card_section.removeCard(self.grabbed_card)
                        self.grabbed_card_section.addCard(self.grabbed_card)
                    else:
                        og_position = (self.grab_location[0] - self.grab_offset[0], self.grab_location[1] - self.grab_offset[1])
                        self.grabbed_card.move(og_position[0], og_position[1])
                self.grabbed_card = None
                self.grab_offset = None
                self.grabbed_card_section = None
                self.grab_location = None
                self.saveCardstoFile()
    
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
settings_file = open('settings.json')
settings = json.load(settings_file)
HEADERFONT = settings['headerfont']
CARDFONT = settings['cardfont']
COUNTERFONT = settings['counterfont']
MAINCOLOR = settings['colors']['main']
SECONDARYCOLOR = settings['colors']['secondary']
MARGIN = settings['margin']
WIDTH = settings['width']
HEIGHT = settings['height']
HEADERSIZE = settings['headersize']
PALETTE = [settings['colors']['pal0'],
        settings['colors']['pal1'],
        settings['colors']['pal2'],
        settings['colors']['pal3'],
        settings['colors']['pal4'],
        settings['colors']['pal5'],
        settings['colors']['pal6'],
    ]
DAYCOUNTER = settings['daycounter']
k = Kanban()

# Import sections
sections = settings['sections']
sum_width = 0
for sec in sections:
    k.addSectionFromFile(sec['name'], int(sec['width']), sum_width, int(sec['cardheight']))
    sum_width += int(sec['width'])

# Import cards
if os.path.isfile('cards.csv'):
    with open('cards.csv', 'r', newline='\n') as csvfile:
        cards = csv.DictReader(csvfile, delimiter='|')
        for c in cards:
            k.addCardFromFile(int(c['section_index']), c['description'], c['color'], int(c['points']), date.fromisoformat(c['creation_date']))
    csvfile.close()
k.root.mainloop()
