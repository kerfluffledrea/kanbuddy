import json
import yaml
import sys
import csv
import os.path
from inspect import getsourcefile, getframeinfo, currentframe
from pathlib import Path
from datetime import date
import tkinter as tk
from tkinter.constants import BOTH, CENTER
from tkinter import E, W, Frame, Text, Button, Label, font, LAST, Menu, FLAT, CENTER, RIDGE

print("abspath: " + str(os.path.abspath(getsourcefile(lambda:0))))
filename = getframeinfo(currentframe()).filename
print("path : " + str(os.path.dirname(os.path.abspath(filename))))
print('__path__: ' + str(Path(__file__).parent))
print('pathlib __file__: ' + str(Path(globals().get("__file__", "./_")).absolute().parent))
print('other one :' + str(os.path.dirname(os.path.abspath(__file__))))

# Read Config File
mod_path = str(Path(__file__).parent)
settings = open(mod_path + "/settings.yaml")
cards_filepath = mod_path + "/.cards.csv"
archive_filepath = mod_path + "/.archive.csv"
settings = yaml.safe_load(settings)

WIDTH = settings['width']
HEIGHT = settings['height']
MARGIN = settings['margin']
HEADERSIZE = settings['headersize']

HEADERFONT = settings['headerfont']
CARDFONT = settings['cardfont']
COUNTERFONT = settings['counterfont']

BGCOLOR = settings['colors']['bg']
MAINCOLOR = settings['colors']['main']
SECONDARYCOLOR = settings['colors']['secondary']
EMPTYSLOTCOLOR = settings['colors']['emptyslot']
BUTTONHIGHLIGHT = settings['colors']['buttonhighlight']
SECTIONHIGHLIGHT = settings['colors']['sectionhighlight']
PALETTE = [settings['colors']['pal0'],
        settings['colors']['pal1'],
        settings['colors']['pal2'],
        settings['colors']['pal3'],
        settings['colors']['pal4'],
        settings['colors']['pal5'],
        settings['colors']['pal6'],
    ]

DRAGTHRESHOLD = 30
DAYCOUNTER = settings['daycounter']
POINTVALS = [1,5,15,30,60,120,180,360,500,1000,2500]

class Card:
    def __init__(self, canvas, desc='-[O-O]-', color_index=0, points=1, creation_date = date.today()):
        self.canvas = canvas
        self.description = desc
        self.color_index = color_index
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

    def draw(self):
        self.canvas_rect = self.canvas.create_rectangle(self.position[0], self.position[1], self.position[0] + self.width, self.position[1] + self.height, outline=PALETTE[self.color_index], tag='card')
        self.canvas_text = self.canvas.create_text(self.position[0] + self.width/2, self.position[1] + self.height/2, anchor=CENTER, text=self.description, fill=PALETTE[self.color_index], width=self.width-MARGIN*2, justify=CENTER, font=CARDFONT, tag='card')
        i = 0
        if DAYCOUNTER:
            self.canvas_dayctr = self.canvas.create_text(self.position[0] + 5, self.position[1] + 8, anchor=W, text=(date.today() - self.creation_date).days, fill=PALETTE[self.color_index], width=self.width-MARGIN*2, justify=CENTER, font=(COUNTERFONT, 9))
        while i < self.points+1:
            self.canvas_lines.append(self.canvas.create_line(self.position[0] + self.width, self.position[1] + self.height - i*MARGIN,
                self.position[0] + self.width - i*MARGIN, self.position[1] + self.height, fill=PALETTE[self.color_index]))
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
            self.canvas.coords(self.canvas_dayctr, x + 4, y + 11)

    def delete(self):
        self.canvas.delete(self.canvas_text)
        self.canvas.delete(self.canvas_rect)
        for l in self.canvas_lines:
            self.canvas.delete(l)
        if DAYCOUNTER:
            self.canvas.delete(self.canvas_dayctr)

    def updateCounter(self):
        self.canvas.itemconfig(self.canvas_dayctr, text=(date.today() - self.creation_date).days)

    def hover(self):
        self.canvas.itemconfig(self.canvas_rect, fill=BUTTONHIGHLIGHT, tag='hover_card')
        self.canvas.itemconfig(self.canvas_text, tag='hover_card')
        for l in self.canvas_lines:
            self.canvas.itemconfig(l, tag='hover_card')
        self.canvas.tag_raise("hover_card")

    def unhover(self):
        self.canvas.itemconfig(self.canvas_rect, fill=BGCOLOR, tag='card')
        self.canvas.itemconfig(self.canvas_text, tag='card')
        for l in self.canvas_lines:
            self.canvas.itemconfig(l, tag='card')

    def setColor(self, color_index):
        self.color_index = color_index
        self.canvas.itemconfig(self.canvas_text, fill=PALETTE[color_index])
        self.canvas.itemconfig(self.canvas_rect, outline=PALETTE[color_index])
        for l in self.canvas_lines:
            self.canvas.itemconfig(l, fill=PALETTE[color_index])
        if DAYCOUNTER:
            self.canvas.itemconfig(self.canvas_dayctr, fill=PALETTE[color_index])

    def setDescription(self, desc):
        self.description = desc
        self.canvas.itemconfig(self.canvas_text, text=desc)
    
    def increasePoints(self):
        if self.points < 10 and self.points * MARGIN < self.height:
            self.points += 1
            self.canvas_lines.append(self.canvas.create_line(self.position[0] + self.width, self.position[1] + self.height - self.points*MARGIN,
                    self.position[0] + self.width - self.points*MARGIN, self.position[1] + self.height, fill=PALETTE[self.color_index]))

    def decreasePoints(self):
        if self.points > 0:
            self.points -= 1
            self.canvas.delete(self.canvas_lines.pop())
    
class DropZone:
    def __init__(self, canvas, x_pos, y_pos, width, height):
        self.canvas = canvas
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.canvas_rect = self.canvas.create_rectangle(x_pos, y_pos, x_pos + width, y_pos + self.height, outline = EMPTYSLOTCOLOR)

class PointsDisplay(DropZone):
    def __init__(self, canvas, x_pos, y_pos, width, height):
        self.canvas = canvas
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.canvas_rect = self.canvas.create_rectangle(x_pos, y_pos, x_pos + width, y_pos + self.height, outline=SECONDARYCOLOR)
        self.point_counter = self.canvas.create_text(x_pos + self.width/2, y_pos + self.height/2, anchor=CENTER, text="{:,}".format(self.getPointsFromFile()), fill=SECONDARYCOLOR, width=self.width-MARGIN*2, font=COUNTERFONT)
    
    def updatePointCounter(self):
        self.canvas.itemconfig(self.point_counter, text="{:,}".format(self.getPointsFromFile()))

    def getPointsFromFile(self):
        point_sum = 0
        if os.path.isfile(archive_filepath):
            with open(archive_filepath, 'r', newline='\n') as csvfile:
                cards = csv.DictReader(csvfile, delimiter='|')
                for c in cards:
                    point_sum += POINTVALS[int(c['points'])]
            return point_sum
        else:
            with open(archive_filepath, 'w', newline='\n') as archivefile:
                archivewriter = csv.writer(archivefile, delimiter="|")
                archivewriter.writerow(['description', 'points', 'color_index', 'creation_date', 'completion_date'])
            return 0

class Section:
    def __init__(self, canvas, name, w, x, ch, last_column_flag):
        self.canvas = canvas
        self.name = name
        self.width = w
        self.x_pos = x
        self.card_height = ch
        self.drop_zones = []
        self.canvas_rect = None
        self.cards = []
        self.draw()            
        self.createDropZones(last_column_flag)

    def draw(self):
        self.canvas_rect = self.canvas.create_rectangle(self.x_pos, 0, self.x_pos + self.width, HEIGHT, outline=MAINCOLOR)
        self.canvas_line = self.canvas.create_line(self.x_pos, HEADERSIZE, self.x_pos+self.width, HEADERSIZE, fill=MAINCOLOR)
        self.canvas_text = self.canvas.create_text(self.x_pos + self.width/2, 15, anchor=CENTER, text=self.name, fill=MAINCOLOR, width=self.width, font=(HEADERFONT))

    def addCard(self, card):
        dz_index = len(self.cards)
        card.width = self.drop_zones[dz_index].width
        card.height = self.drop_zones[dz_index].height
        card.move(self.drop_zones[dz_index].x_pos, self.drop_zones[dz_index].y_pos)
        self.cards.append(card)

    def removeCard(self, card):
        self.cards.remove(card)
        self.reorderCards()

    def reorderCards(self):
        i = 0
        for card in self.cards:
            card.width = self.drop_zones[i].width
            card.height = self.drop_zones[i].height
            card.move(self.drop_zones[i].x_pos, self.drop_zones[i].y_pos)
            i += 1

    def setColor(self, COLOR):
        self.canvas.itemconfig(self.canvas_rect, fill=COLOR)

    def createDropZones(self, last_column_flag):
        i = 0
        while True:
            if last_column_flag:
                xpos = self.x_pos + MARGIN
                ypos = HEADERSIZE + self.card_height * i + MARGIN * (i + 1)
                self.drop_zones.append(DropZone(self.canvas, xpos, ypos, self.width - MARGIN * 2, self.card_height))
                i += 1
                ypos = HEADERSIZE + self.card_height * (i+1) + MARGIN * (i + 2)
                if ypos + self.card_height > HEIGHT:
                    self.addPointCounter()
                    break
            else: 
                xpos = self.x_pos + MARGIN
                ypos = HEADERSIZE + self.card_height * i + MARGIN * (i + 1)
                if ypos + self.card_height > HEIGHT:
                    break
                self.drop_zones.append(DropZone(self.canvas, xpos, ypos, self.width - MARGIN * 2, self.card_height))
                i += 1

    def addPointCounter(self):
        xpos = self.x_pos + MARGIN
        ypos = HEADERSIZE + self.card_height * len(self.drop_zones) + MARGIN * (len(self.drop_zones) + 1)
        self.archive_dropzone = PointsDisplay(self.canvas, xpos, ypos, self.width - MARGIN * 2, self.card_height)

class Kanban:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.wm_title("Kanbuddy")
        self.root.wm_attributes('-type', 'splash', '-topmost', 'true')
        self.root.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.root.configure(background=BGCOLOR)
        self.canvas = tk.Canvas(self.root, bg=BGCOLOR, width=WIDTH, height=HEIGHT, highlightthickness=1, highlightbackground=MAINCOLOR)
        self.canvas.pack()

        self.root.bind('<Control-a>', self.addNewCard)
        self.canvas.bind('<Button-1>', self.handleClickDown)
        self.canvas.bind('<Button-2>', self.handleMiddleClickDown)
        self.canvas.bind('<Button-3>', self.handleRightClickDown)
        self.canvas.bind('<ButtonRelease-1>', self.handleClickUp)
        self.canvas.bind('<ButtonRelease-2>', self.handleMiddleClickUp)
        self.canvas.bind('<ButtonRelease-3>', self.handleRightClickUp)
        self.canvas.bind('<Double-Button-1>', self.handleDoubleClick)
        self.canvas.bind('<Motion>', self.handleMouseMove)
        self.canvas.bind('<B1-Motion>', self.handleClickDrag)
        self.canvas.bind('<B2-Motion>', self.handleMiddleClickDrag)
        
        self.cards = []
        self.sections = []
        self.archive_dropzone = None
        self.edit_menu = None
        self.context_menu = None
        self.grabbed_card = None
        self.grab_offset = None
        self.grab_location = None
        self.middle_click_origin = None
        self.grabbed_card_section = None
        self.control_held = False
        self.lmb_held = False
        self.rmb_held = False
        self.pinned = tk.BooleanVar()
        self.pinned.set(True)
        self.drag_origin = ()

    # --- File Reading/Writing ---
    def addNewCard(self, event=None):
        if not self.edit_menu:
            if len(self.sections[0].cards) < len(self.sections[0].drop_zones):
                c = Card(self.canvas)
                self.cards.append(c)
                self.sections[0].addCard(c)
                self.saveCardstoFile()
                return c

    def saveCardstoFile(self):
        with open(cards_filepath, 'w', newline='\n') as cardfile:
            with open(archive_filepath, 'a', newline='\n') as archivefile:
                cardwriter = csv.writer(cardfile, delimiter="|")
                cardwriter.writerow(['section_index', 'description', 'color_index', 'points', 'creation_date'])
                for c in self.cards:
                    cardwriter.writerow([c.section_index, c.description, c.color_index, c.points, c.creation_date])

    def addSectionFromFile(self, name, width, xpos, cardheight, last_column = False):
        s = Section(self.canvas, name, width, xpos, cardheight, last_column)
        self.sections.append(s)

    def addCardFromFile(self, section_index, description, color_index, points, creation_date):
        c = Card(self.canvas, description, color_index, points, creation_date)
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

    def isInArchiveDropzone(self, mx, my):
        if mx > self.archive_dropzone.x_pos and mx < self.archive_dropzone.x_pos + self.archive_dropzone.width and my > self.archive_dropzone.y_pos and my < self.archive_dropzone.y_pos + self.archive_dropzone.height:
            return True
        return False
    
    # --- Card Editing ---
    def openEditMenu(self, edit_card):
        self.edit_menu = Frame(self.root, name='edit_menu', pady=MARGIN/3, padx=MARGIN/3, relief=tk.SOLID, bg=BGCOLOR, highlightcolor=PALETTE[edit_card.color_index], highlightbackground=PALETTE[edit_card.color_index], highlightthickness=1)
        self.edit_menu.pack(fill=BOTH, expand=True, padx=MARGIN*2, pady=MARGIN*2)
        
        description_entry = Text(self.edit_menu,name='edit_menu_text', wrap=tk.WORD, insertbackground=SECONDARYCOLOR, font=CARDFONT, height=5, width=34, padx=15, pady=5, bg=BGCOLOR, bd=0, highlightbackground=PALETTE[edit_card.color_index], highlightcolor=PALETTE[edit_card.color_index], fg=PALETTE[edit_card.color_index])
        description_entry.insert(tk.END, edit_card.description)
        description_entry.pack(padx=MARGIN, pady=MARGIN)
        
        button_grid = Frame(self.edit_menu, name='button_grid', background=BGCOLOR)
        button_grid.pack(padx=MARGIN, pady=MARGIN/4)

        color_button_grid = Frame(button_grid, name='color_button_grid')
        color_button_grid.pack(side = tk.LEFT, padx=MARGIN)
        b0 = Button(color_button_grid, bg=PALETTE[0], padx=8, width=1, height=1, highlightbackground=PALETTE[0], command=lambda: self.changeColorButton(edit_card, 0)).grid(column=0, row=0)
        b1 = Button(color_button_grid, bg=PALETTE[1], padx=8, width=1, height=1, highlightbackground=PALETTE[1], command=lambda: self.changeColorButton(edit_card, 1)).grid(column=1, row=0)
        b2 = Button(color_button_grid, bg=PALETTE[2], padx=8, width=1, height=1, highlightbackground=PALETTE[2], command=lambda: self.changeColorButton(edit_card, 2)).grid(column=2, row=0)
        b3 = Button(color_button_grid, bg=PALETTE[3], padx=8, width=1, height=1, highlightbackground=PALETTE[3], command=lambda: self.changeColorButton(edit_card, 3)).grid(column=3, row=0)
        b4 = Button(color_button_grid, bg=PALETTE[4], padx=8, width=1, height=1, highlightbackground=PALETTE[4], command=lambda: self.changeColorButton(edit_card, 4)).grid(column=4, row=0)
        b5 = Button(color_button_grid, bg=PALETTE[5], padx=8, width=1, height=1, highlightbackground=PALETTE[5], command=lambda: self.changeColorButton(edit_card, 5)).grid(column=5, row=0)
        b6 = Button(color_button_grid, bg=PALETTE[6], padx=8, width=1, height=1, highlightbackground=PALETTE[6], command=lambda: self.changeColorButton(edit_card, 6)).grid(column=6, row=0)

        value_button_grid = Frame(button_grid, name='value_button_grid')
        value_button_grid.pack(side = tk.RIGHT, padx=MARGIN)
        decrease_points = Button(value_button_grid, activebackground=BUTTONHIGHLIGHT, activeforeground=PALETTE[edit_card.color_index], relief=tk.FLAT, name='decrease_button', text='-', fg=PALETTE[edit_card.color_index], bg=BGCOLOR, width=1, height=1, highlightbackground=PALETTE[edit_card.color_index], command=lambda: edit_card.decreasePoints()).grid(column=8, row=0)
        increase_points = Button(value_button_grid, activebackground=BUTTONHIGHLIGHT, activeforeground=PALETTE[edit_card.color_index], relief=tk.FLAT, name='increase_button', text='+', fg=PALETTE[edit_card.color_index], bg=BGCOLOR, width=1, height=1, highlightbackground=PALETTE[edit_card.color_index], command=lambda: edit_card.increasePoints()).grid(column=9, row=0)

        bottom_button_grid = Frame(self.edit_menu, name='bottom_button_grid', background=BGCOLOR)
        bottom_button_grid.pack(pady=MARGIN, padx=MARGIN/10)
        close_button = Button(bottom_button_grid, activeforeground=PALETTE[edit_card.color_index], activebackground=BUTTONHIGHLIGHT, relief=tk.FLAT, name='close_button', text='SAVE', fg=PALETTE[edit_card.color_index], bg=BGCOLOR, width=20, height=1, highlightbackground=PALETTE[edit_card.color_index], command=lambda: self.closeEditMenu(edit_card, description_entry.get("1.0","end-1c"))).grid(column=3, row=0)
        delete_button = Button(bottom_button_grid, activeforeground=PALETTE[edit_card.color_index], activebackground=BUTTONHIGHLIGHT, relief=tk.FLAT, name='delete_button', text='DELETE', fg=PALETTE[edit_card.color_index], bg=BGCOLOR, width=5, height=1, highlightbackground=PALETTE[edit_card.color_index], command=lambda: self.deleteCard(edit_card, True)).grid(column=4, row=0)
        self.canvas.create_window(WIDTH/2, HEIGHT/2, anchor=CENTER, window=self.edit_menu)

    def changeColorButton(self, edit_card, color_index):
        edit_card.setColor(color_index)
        self.edit_menu.config(highlightbackground=PALETTE[color_index], highlightcolor=PALETTE[color_index])
        self.edit_menu.nametowidget('edit_menu_text').config(highlightcolor=PALETTE[color_index], highlightbackground=PALETTE[color_index], fg=PALETTE[color_index])
        self.edit_menu.nametowidget('button_grid').nametowidget('value_button_grid').nametowidget('increase_button').config(activeforeground=PALETTE[color_index], highlightbackground=PALETTE[color_index], fg=PALETTE[color_index])
        self.edit_menu.nametowidget('button_grid').nametowidget('value_button_grid').nametowidget('decrease_button').config(activeforeground=PALETTE[color_index], highlightbackground=PALETTE[color_index], fg=PALETTE[color_index])
        self.edit_menu.nametowidget('bottom_button_grid').nametowidget('close_button').config(activeforeground=PALETTE[color_index], highlightbackground=PALETTE[color_index], fg=PALETTE[color_index])
        self.edit_menu.nametowidget('bottom_button_grid').nametowidget('delete_button').config(activeforeground=PALETTE[color_index], highlightbackground=PALETTE[color_index], fg=PALETTE[color_index])

    def closeEditMenu(self, edit_card, desc):
        edit_card.setDescription(desc)
        self.edit_menu.destroy()
        self.edit_menu = None
        self.saveCardstoFile()

    def deleteCard(self, card, editing=False):
        self.cards.remove(card)
        self.sections[card.section_index].cards.remove(card)
        card.clearCanvas()
        del card
        if editing:
            self.edit_menu.destroy()
            self.edit_menu = None
        self.saveCardstoFile()

    def updateCardCounters(self):
        for c in self.cards:
            c.updateCounter()
    
    def destroyContextMenu(self):
        if self.context_menu:
            self.context_menu.destroy()

    def setPinned(self):
        if self.pinned.get():
            self.root.wm_attributes('-type', 'splash', "-topmost", "true")
        else:
            self.root.wm_attributes('-type', 'splash', "-topmost", "false")

    # --- Event Handlers ---
    def handleMouseMove(self, event):
        self.grabbed_card = self.getColldingCards(event.x, event.y)
        for c in self.cards:
            if c == self.grabbed_card:
                c.hover()
            else:
                c.unhover()

    def handleClickDown(self, event):
        self.lmb_held = True
        self.destroyContextMenu()
        if event.y < HEADERSIZE:
            self.drag_origin = (event.x, event.y)
        if not self.edit_menu:
            self.grabbed_card = self.getColldingCards(event.x, event.y)
            if self.grabbed_card:
                self.grabbed_card.unhover()
                self.grab_offset = (event.x - self.grabbed_card.position[0], event.y - self.grabbed_card.position[1])
                self.grabbed_card_section = self.sections[self.grabbed_card.section_index]
                self.grab_location = (event.x, event.y)

    def handleClickUp(self, event):
        self.lmb_held = False
        self.canvas.config(cursor='')
        self.drag_origin = None
        for s in self.sections:
            s.setColor(BGCOLOR)
        if DAYCOUNTER:
            self.updateCardCounters()
        if not self.edit_menu:
            if self.grabbed_card:
                drop_section = self.getCollidingSections(event.x, event.y)
                if self.sections.index(drop_section) == len(self.sections)-1 and self.isInArchiveDropzone(event.x, event.y):
                    with open(archive_filepath, 'a', newline='\n') as archivefile:
                        archivewriter = csv.writer(archivefile, delimiter="|")
                        archivewriter.writerow([self.grabbed_card.description, self.grabbed_card.points, self.grabbed_card.color_index, self.grabbed_card.creation_date, date.today()])
                    self.archive_dropzone.updatePointCounter()
                    self.deleteCard(self.grabbed_card)
                    self.grabbed_card_section.reorderCards()
                elif drop_section and len(drop_section.cards) < len(drop_section.drop_zones) and self.sections.index(drop_section) != self.grabbed_card.section_index:
                    self.grabbed_card.section_index = self.sections.index(drop_section)
                    drop_section.addCard(self.grabbed_card)
                    self.grabbed_card_section.removeCard(self.grabbed_card)
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

    def handleClickDrag(self, event):
        if self.drag_origin:
            x, y = event.x - self.drag_origin[0] + self.root.winfo_x(), event.y - self.drag_origin[1] + self.root.winfo_y()
            self.root.geometry("+%s+%s" % (x , y))
        if self.grabbed_card:
            self.canvas.config(cursor='fleur')
            move_pos = (event.x - self.grab_offset[0], event.y - self.grab_offset[1])
            self.grabbed_card.move(move_pos[0], move_pos[1])
            section = self.getCollidingSections(event.x, event.y)
            for s in self.sections:
                s.setColor(BGCOLOR)
            if section:
                section.setColor(SECTIONHIGHLIGHT)

    def handleDoubleClick(self, event):
        if not self.edit_menu:
            edit_card = self.getColldingCards(event.x, event.y)
            if edit_card:
                self.openEditMenu(edit_card)

    def handleMiddleClickDown(self, event):
        if not self.edit_menu:
            self.grabbed_card = self.getColldingCards(event.x, event.y)
            if self.grabbed_card:
                self.grab_offset = (event.x - self.grabbed_card.position[0], event.y - self.grabbed_card.position[1])
                self.grabbed_card_section = self.sections[self.grabbed_card.section_index]
                self.grab_location = (event.x, event.y)
        self.middle_click_origin = (event.x, event.y)

    def handleMiddleClickUp(self, event):
        if not self.lmb_held:
            if not self.edit_menu and self.grabbed_card:
                total_drag_distance = self.grab_location[0] - event.x, self.grab_location[1] - event.y
                if abs(total_drag_distance[1]) < DRAGTHRESHOLD/2:
                    if event.state & 0x4: # Check if Ctrl-Key is held, maybe i should make this bindable one day, who's to say, truly we do not know what life has in store for us on this crazy world so perhaps it would be best to leave this for another day such that I have plenty of time to ruminate on the ramifications of hardcoding this value in an event call, whos to say. Not I. Yippee.
                        if self.grabbed_card.color_index > 0:
                            self.grabbed_card.setColor(self.grabbed_card.color_index - 1)
                        else:
                            self.grabbed_card.setColor(len(PALETTE)-1)
                    else:
                        if self.grabbed_card.color_index < len(PALETTE)-1:
                            self.grabbed_card.setColor(self.grabbed_card.color_index + 1)
                        else:
                            self.grabbed_card.setColor(0)
                    og_position = (self.grab_location[0] - self.grab_offset[0], self.grab_location[1] - self.grab_offset[1])
                    self.grabbed_card.move(og_position[0], og_position[1])
            self.grabbed_card = None
            self.grab_offset = None
            self.grabbed_card_section = None
            self.grab_location = None
            self.saveCardstoFile()

    def handleMiddleClickDrag(self, event):
        if not self.lmb_held and self.grabbed_card:
            drag_y_distance = event.y - self.middle_click_origin[1]
            if drag_y_distance > DRAGTHRESHOLD:
                self.grabbed_card.decreasePoints()
                self.middle_click_origin = (self.middle_click_origin[0], self.middle_click_origin[1] + DRAGTHRESHOLD)
            elif drag_y_distance < -DRAGTHRESHOLD:
                self.grabbed_card.increasePoints()
                self.middle_click_origin = (self.middle_click_origin[0], self.middle_click_origin[1] - DRAGTHRESHOLD)

    def handleRightClickDown(self, event):
        self.rmb_held = True
        self.destroyContextMenu()
        if not self.edit_menu:
            self.grabbed_card = self.getColldingCards(event.x, event.y)
            if self.grabbed_card:
                self.grab_offset = (event.x - self.grabbed_card.position[0], event.y - self.grabbed_card.position[1])
                self.grabbed_card_section = self.sections[self.grabbed_card.section_index]
                self.grab_location = (event.x, event.y)

    def handleRightClickUp(self, event):
        self.rmb_held = False
        self.grabbed_card = self.getColldingCards(event.x, event.y)
        
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=BGCOLOR, fg=SECONDARYCOLOR, selectcolor=SECONDARYCOLOR, font=COUNTERFONT)

        if self.isInArchiveDropzone(event.x, event.y): 
            #self.context_menu.add_command(label="Reset Archive", state='disabled', command=lambda: self.openEditMenu(self.grabbed_card))
            pass
        elif self.grabbed_card:
                self.grab_location = (event.x, event.y)
                self.context_menu.add_command(label="Edit", command=lambda: self.openEditMenu(self.grabbed_card))
                self.context_menu.add_command(label="Delete", command=lambda: self.deleteCard(self.grabbed_card))
        else:
            self.context_menu.add_command(label="New Card", accelerator='Ctrl-A', command=lambda: self.addNewCard())
        self.context_menu.add_separator()
        self.context_menu.add_checkbutton(label="Stay On Top", variable=self.pinned, onvalue=1, offvalue=0, command=lambda: self.setPinned())
        self.context_menu.add_command(label="Quit", command=lambda: quit())
        self.context_menu.post(event.x_root, event.y_root)
    
    # --- Welcome Screen ---
    def openWelcomeScreen(self):
        self.edit_menu = Frame(self.root, name='welcome_screen', relief=FLAT, bg=BGCOLOR, padx=MARGIN*2, pady=MARGIN*2, highlightcolor=SECONDARYCOLOR, highlightbackground=SECONDARYCOLOR, highlightthickness=1, height=HEIGHT-(MARGIN*2), width=WIDTH-(MARGIN*2))        
        self.edit_menu.pack(fill=BOTH, expand=False, padx=MARGIN, pady=MARGIN)
        
        welcome_grid = Frame(self.edit_menu, name='welcome_grid', background=BGCOLOR)
        welcome_grid.pack(padx=MARGIN, pady=MARGIN/4)

        welcome = Label(welcome_grid, text="Welcome to Kanbuddy!", font=(HEADERFONT, 24, "bold"), bg=BGCOLOR, fg=SECONDARYCOLOR, padx=MARGIN, pady=MARGIN).grid(column=0, row=0)
        byline = Label(welcome_grid, text="by kerfluffle", font=(HEADERFONT, 12, "bold"), bg=BGCOLOR, fg=SECONDARYCOLOR, padx=MARGIN, pady=MARGIN).grid(column=0, row=1)

        instructions = Label(welcome_grid, font=(CARDFONT, 12), text=
'''
- CTRL-A to make new Card
- Double-Click card to Edit
- Drag card to bottom-right box to mark as complete.
- Settings can be changed in settings.json
''', bg=BGCOLOR, fg=SECONDARYCOLOR, justify=CENTER).grid(column=0, row=2)

        close_button = Button(welcome_grid, text="Enter the World of Kanbuddy", activeforeground=SECONDARYCOLOR, activebackground=BUTTONHIGHLIGHT, relief=tk.FLAT, bg=BGCOLOR, fg=SECONDARYCOLOR, padx=MARGIN, highlightbackground=SECONDARYCOLOR, command=lambda: self.closeWelcomeScreen()).grid(column=0,row=3)
        self.canvas.create_window(WIDTH/2, HEIGHT/2, anchor=CENTER, window=self.edit_menu)

    def closeWelcomeScreen(self):
        self.edit_menu.destroy()
        self.edit_menu = None

# Import sections
k = Kanban()

sections = settings['sections']
sum_width = 0
if not os.path.isfile(archive_filepath):
    k.openWelcomeScreen()

for sec in sections:
    if sec == sections[-1]:
        k.addSectionFromFile(sec['name'], int(sec['width']), sum_width, int(sec['cardheight']), True)
        k.archive_dropzone = k.sections[len(k.sections)-1].archive_dropzone
    else:
        k.addSectionFromFile(sec['name'], int(sec['width']), sum_width, int(sec['cardheight']))
    sum_width += int(sec['width'])

# Import cards
if os.path.isfile(cards_filepath):
    with open(cards_filepath, 'r', newline='\n') as csvfile:
        cards = csv.DictReader(csvfile, delimiter='|')
        for c in cards:
            k.addCardFromFile(int(c['section_index']), c['description'], int(c['color_index']), int(c['points']), date.fromisoformat(c['creation_date']))
    csvfile.close()
k.root.mainloop()
