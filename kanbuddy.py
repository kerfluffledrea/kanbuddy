import sys
import csv
import os
import yaml
import webbrowser
import datetime
from datetime import date
import tkinter as tk
from tkinter.constants import BOTH, CENTER
from tkinter import W, Frame, Text, Button, Label, CENTER

# Read Config File
mod_path = str(str(os.getcwd()))
SETTINGS_PATH = (mod_path + "/settings.yaml") 
settings = open(SETTINGS_PATH)
cards_filepath = mod_path + "/.cards.csv"
archive_filepath = mod_path + "/.archive.csv"
settings = yaml.safe_load(settings)


DASH = None
if bool(settings['dashed']):
    DASH = (5,)

WIDTH = settings['width']
HEIGHT = settings['height']
MARGIN = settings['margin']
HEADERSIZE = settings['headersize']

HEADERFONT = settings['font']['header']
CARDFONT = settings['font']['card']
COUNTERFONT = settings['font']['counter']
TIMERFONT = settings['font']['timer']

GLOBALRELIEF = tk.FLAT

THEMES = dict()
THEMES['custom'] = {
    'name' : 'custom',
    'bg' : settings['customtheme']['bg'],
    'main' : settings['customtheme']['main'],
    'secondary' : settings['customtheme']['secondary'],
    'emptyslot' : settings['customtheme']['emptyslot'],
    'buttonhighlight' : settings['customtheme']['buttonhighlight'],
    'sectionhighlight' : settings['customtheme']['sectionhighlight'],
    'palette' : [settings['customtheme']['palette0'],
                 settings['customtheme']['palette1'],
                 settings['customtheme']['palette2'],
                 settings['customtheme']['palette3'],
                 settings['customtheme']['palette4'],
                 settings['customtheme']['palette5'],
                 settings['customtheme']['palette6']]
}

THEMES['prime'] = {
    'name' : 'prime',
    'bg' : 'black',
    'main' : 'blueviolet',
    'secondary' : '#00ffcc',
    'emptyslot' : '#1F0030',
    'buttonhighlight' : '#090020',
    'sectionhighlight' : '#100020',
    'palette' : ['white',
                 'lime',
                 'cyan',
                 'dodgerblue',
                 'magenta',
                 'yellow',
                 'orangered']
}

THEMES['fortress'] = {
    'name' : 'fortress',
    'bg' : 'black',
    'main' : 'white',
    'secondary' : 'grey50',
    'emptyslot' : 'grey20',
    'buttonhighlight' : 'grey10',
    'sectionhighlight' : 'grey5',
    'palette' : ['lime',
                 'cyan',
                 'blue',
                 'yellow',
                 'red',
                 'magenta',
                 'grey80']
}


THEMES['ihaveahax'] = {
    'name' : 'ihaveahax',
    'bg' : '#CCD0E5',
    'main' : '#5E6490',
    'secondary' : '#5E7D90',
    'emptyslot' : '#A5B0D6',
    'buttonhighlight' : '#B6BCDA',
    'sectionhighlight' : '#BAC0DC',
    'palette' : ['#3F3B97',
                 '#765776',
                 '#715E90',
                 '#884CB9',
                 '#B23CC3',
                 '#BE1800',
                 '#FF9500']
}

THEMES['trioptimum'] = {
    'name' : 'trioptimum',
    'bg' : 'black',
    'main' : '#53538c',
    'secondary' : '#00FFAA',
    'emptyslot' : '#1b1a20',
    'buttonhighlight' : '#014131',
    'sectionhighlight' : '#014131',
    'palette' : ['#00FFAA',
                 '#40fe1f',
                 '#3d01fc',
                 '#b0a2a7',
                 '#6e66d4',
                 '#d21540',
                 '#ff8300']
}

THEMES['uplink'] = {
    'name' : 'uplink',
    'bg' : 'black',
    'main' : '#0320aa',
    'secondary' : '#081f6f',
    'emptyslot' : '#111542',
    'buttonhighlight' : '#4864c8',
    'sectionhighlight' : '#4864c8',
    'palette' : ['#5795e6',
                 '#4b4cb8',
                 '#0600FF',
                 '#FFFFFF',
                 '#41c09f',
                 '#00FF00',
                 '#FF0000']
}

THEMES['peach'] = {
    'name' : 'peach',
    'bg' : '#fee0c9',
    'main' : '#fc008b',
    'secondary' : '#ff6699',
    'emptyslot' : '#ffb0d7',
    'buttonhighlight' : 'pink',
    'sectionhighlight' : '#ffb0d7',
    'palette' : [
                 '#4c3e17',
                 '#f4bb0d',
                 '#FF7766',
                 '#FF0d80',
                 '#c20717',
                 '#9f4299',
                 '#1488fe']
}

DRAGTHRESHOLD = 30
DAYCOUNTER = settings['daycounter']
POINTVALS = [1,5,15,30,60,120,180,360,500,1000,2500]

class Card:
    def __init__(self, canvas, theme, desc='-[O-O]-', color_index=0, points=1, creation_date = date.today()):
        self.canvas = canvas
        self.theme = theme
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
        self.canvas_rect = self.canvas.create_rectangle(self.position[0], self.position[1], self.position[0] + self.width, self.position[1] + self.height, outline=self.theme['palette'][self.color_index], tag='card')
        self.canvas_text = self.canvas.create_text(self.position[0] + self.width/2, self.position[1] + self.height/2, anchor=CENTER, text=self.description, fill=self.theme['palette'][self.color_index], width=self.width-MARGIN*2, justify=CENTER, font=CARDFONT, tag='card')
        i = 0
        if DAYCOUNTER:
            self.canvas_dayctr = self.canvas.create_text(self.position[0] + 5, self.position[1] + 8, anchor=W, text=(date.today() - self.creation_date).days, fill=self.theme['palette'][self.color_index], width=self.width-MARGIN*2, justify=CENTER, font=(COUNTERFONT, 9))
        while i < self.points+1:
            self.canvas_lines.append(self.canvas.create_line(self.position[0] + self.width, self.position[1] + self.height - i*MARGIN,
                self.position[0] + self.width - i*MARGIN, self.position[1] + self.height, fill=self.theme['palette'][self.color_index]))
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

    def displayPoints(self):
        self.canvas.itemconfig(self.canvas_rect, fill=self.theme['buttonhighlight'])
        self.canvas.itemconfig(self.canvas_text, text="+{}".format(POINTVALS[self.points]), font=TIMERFONT)

    def undisplayPoints(self):
        self.canvas.itemconfig(self.canvas_rect, fill=self.theme['bg'])
        self.canvas.itemconfig(self.canvas_text, text=self.description, font=CARDFONT)

    def hover(self):
        self.canvas.itemconfig(self.canvas_rect, fill=self.theme['buttonhighlight'], tag='hover_card')
        self.canvas.itemconfig(self.canvas_text, tag='hover_card')
        for l in self.canvas_lines:
            self.canvas.itemconfig(l, tag='hover_card')
        self.canvas.tag_raise("hover_card")
    
    def drag(self):
        self.canvas.tag_raise("hover_card")

    def undrag(self):
        self.canvas.tag_lower("hover_card")

    def unhover(self):
        for l in self.canvas_lines:
            self.canvas.itemconfig(l, tag='card')
        self.canvas.itemconfig(self.canvas_rect, fill=self.theme['bg'], tag='card')
        self.canvas.itemconfig(self.canvas_text, tag='card')

    def setColor(self, color_index):
        self.color_index = color_index
        self.canvas.itemconfig(self.canvas_text, fill=self.theme['palette'][color_index])
        self.canvas.itemconfig(self.canvas_rect, outline=self.theme['palette'][color_index])
        for l in self.canvas_lines:
            self.canvas.itemconfig(l, fill=self.theme['palette'][color_index])
        if DAYCOUNTER:
            self.canvas.itemconfig(self.canvas_dayctr, fill=self.theme['palette'][color_index])

    def setDescription(self, desc):
        self.description = desc
        self.canvas.itemconfig(self.canvas_text, text=desc)
    
    def increasePoints(self):
        if self.points < 10 and self.points * MARGIN < self.height:
            self.points += 1
            self.canvas_lines.append(self.canvas.create_line(self.position[0] + self.width, self.position[1] + self.height - self.points*MARGIN,
                    self.position[0] + self.width - self.points*MARGIN, self.position[1] + self.height, fill=self.theme['palette'][self.color_index]))
            self.canvas.tag_raise('line')

    def decreasePoints(self):
        if self.points > 0:
            self.points -= 1
            self.canvas.delete(self.canvas_lines.pop())
    
class DropZone:
    def __init__(self, canvas, theme, x_pos, y_pos, width, height):
        self.canvas = canvas
        self.theme = theme
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.canvas_rect = self.canvas.create_rectangle(x_pos, y_pos, x_pos + width, y_pos + self.height, dash=DASH, outline = self.theme['emptyslot'])
    
    def draw(self):
        self.canvas.itemconfig(self.canvas_rect, outline=self.theme['emptyslot'])
    
class PointsDisplay(DropZone):
    def __init__(self, canvas, theme, x_pos, y_pos, width, height):
        self.canvas = canvas
        self.theme = theme
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.start_time = datetime.datetime.now()
        self.canvas_rect = self.canvas.create_rectangle(x_pos, y_pos, x_pos + width, y_pos + self.height, dash=DASH, outline=self.theme['secondary'])
        self.point_counter = self.canvas.create_text(x_pos + self.width/2, y_pos + self.height - MARGIN *2, anchor=CENTER, text="{:,}".format(self.getPointsFromFile()), fill=self.theme['secondary'], width=self.width-MARGIN*2, font=COUNTERFONT)
        self.timer = self.canvas.create_text(x_pos + self.width/2, y_pos + self.height/2 - MARGIN/2, anchor=CENTER, text="00:00:00", fill=self.theme['secondary'], width=self.width-MARGIN*2, font=TIMERFONT)
        
        #self.point_counter = self.canvas.create_text(x_pos + self.width/2, y_pos + self.height/2 - MARGIN/2, anchor=CENTER, text="{:,}".format(self.getPointsFromFile()), fill=self.theme['secondary'], width=self.width-MARGIN*2, font=COUNTERFONT)
        #self.timer = self.canvas.create_text(x_pos + self.width/2, y_pos + self.height - MARGIN *2, anchor=CENTER, text="00:00:00", fill=self.theme['secondary'], width=self.width-MARGIN*2, font=TIMERFONT)
        self.time()

    def draw(self):
        self.canvas.itemconfig(self.canvas_rect, outline=self.theme['secondary'])
        self.canvas.itemconfig(self.point_counter, fill=self.theme['secondary'])
        self.canvas.itemconfig(self.timer, fill=self.theme['secondary'])

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
    

    def time(self):
        time_delta = datetime.datetime.now() - self.start_time
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.canvas.itemconfig(self.timer, text=('{:02}:{:02}:{:02}'.format(hours, minutes, seconds)))
        self.canvas.after(1000, self.time)

    def resetTime(self):
        self.start_time = datetime.datetime.now()

    def resetArchive(self):
        os.remove(archive_filepath)
        self.getPointsFromFile()
        self.updatePointCounter()

class Section:
    def __init__(self, canvas, theme, name, w, x, cards, last_column_flag=False):
        self.canvas = canvas
        self.theme = theme
        self.name = name
        self.width = w
        self.x_pos = x
        self.drop_zones = []
        self.canvas_rect = None
        self.cards = []
        self.draw()            
        self.createDropZones(last_column_flag, cards)

    def draw(self):
        self.canvas_rect = self.canvas.create_rectangle(self.x_pos, 0, self.x_pos + self.width, HEIGHT, outline=self.theme['main'])
        self.canvas_line = self.canvas.create_line(self.x_pos, HEADERSIZE, self.x_pos+self.width, HEADERSIZE, fill=self.theme['main'])
        self.canvas_text = self.canvas.create_text(self.x_pos + self.width/2, HEADERSIZE/2, anchor=CENTER, text=self.name, fill=self.theme['main'], width=self.width, font=(HEADERFONT))

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
        self.canvas.itemconfig(self.canvas_rect, outline=self.theme['main'], fill=COLOR)
        self.canvas.itemconfig(self.canvas_line, fill=self.theme['main'])
        self.canvas.itemconfig(self.canvas_text, fill=self.theme['main'])

    def createDropZones(self, last_column_flag, cards):
        card_height = (HEIGHT-HEADERSIZE-(MARGIN*(cards+1)))/cards
        i = 0
        for i in range(cards):
            if i == cards-1 and last_column_flag:
                self.addPointCounter(card_height)
            else:
                xpos = self.x_pos + MARGIN
                ypos = HEADERSIZE + card_height * i + MARGIN * (i + 1)
                if ypos + card_height > HEIGHT:
                    break
                self.drop_zones.append(DropZone(self.canvas, self.theme, xpos, ypos, self.width - MARGIN * 2, card_height))
                i += 1

    def addPointCounter(self, ch):
        xpos = self.x_pos + MARGIN
        ypos = HEADERSIZE + ch * len(self.drop_zones) + MARGIN * (len(self.drop_zones) + 1)
        self.archive_dropzone = PointsDisplay(self.canvas, self.theme, xpos, ypos, self.width - MARGIN * 2, ch)

class Kanban:
    def __init__(self, theme_name):
        self.root = tk.Tk()
        self.canvas = None
        self.root.resizable(False, False)
        self.root.wm_title("Kanbuddy")
        self.root.bind('<Control-a>', self.addNewCard)
        self.theme = {
            'name' : None,
            'bg' : None,
            'main' : None,
            'secondary' : None,
            'emptyslot' : None,
            'buttonhighlight' : None,
            'sectionhighlight' : None,
            'palette' : []
        }
        
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
        self.selected_theme = tk.StringVar(value=theme_name)
        self.setTheme(theme_name)
        
        if str(sys.platform).lower() == 'win32':
            self.root.overrideredirect(True)
        else:
            self.root.wm_attributes('-type', 'splash')
        self.root.wm_attributes('-topmost', 'true')

        self.root.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.root.configure(background=self.theme['bg'])
        self.canvas = tk.Canvas(self.root, bg=self.theme['bg'], width=WIDTH, height=HEIGHT, highlightthickness=1, highlightbackground=self.theme['main'])
        self.canvas.pack()
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

    # --- File Reading/Writing ---
    def addNewCard(self, event=None):
        if not self.edit_menu:
            if len(self.sections[0].cards) < len(self.sections[0].drop_zones):
                c = Card(self.canvas, self.theme)
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
        s = Section(self.canvas, self.theme, name, width, xpos, cardheight, last_column)
        self.sections.append(s)

    def addCardFromFile(self, section_index, description, color_index, points, creation_date):
        c = Card(self.canvas, self.theme, description, color_index, points, creation_date)
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
        self.edit_menu = Frame(self.root, name='edit_menu', pady=MARGIN/3, padx=MARGIN/3, relief=tk.SOLID, bg=self.theme['bg'], highlightcolor=self.theme['palette'][edit_card.color_index], highlightbackground=self.theme['palette'][edit_card.color_index], highlightthickness=1)
        self.edit_menu.pack(fill=BOTH, expand=True, padx=MARGIN*2, pady=MARGIN*2)
        
        description_entry = Text(self.edit_menu,name='edit_menu_text', wrap=tk.WORD, insertbackground=self.theme['secondary'], font=CARDFONT, height=5, width=34, padx=15, pady=5, bg=self.theme['bg'], bd=0, highlightbackground=self.theme['palette'][edit_card.color_index], highlightcolor=self.theme['palette'][edit_card.color_index], fg=self.theme['palette'][edit_card.color_index])
        description_entry.insert(tk.END, edit_card.description)
        description_entry.pack(padx=MARGIN, pady=MARGIN)
        
        button_grid = Frame(self.edit_menu, name='button_grid', background=self.theme['bg'])
        button_grid.pack(padx=MARGIN, pady=MARGIN/4)

        color_button_grid = Frame(button_grid, name='color_button_grid')
        color_button_grid.pack(side = tk.LEFT, padx=MARGIN)
        b0 = Button(color_button_grid, bg=self.theme['palette'][0], padx=8, width=1, height=1, highlightbackground=self.theme['palette'][0], command=lambda: self.changeColorButton(edit_card, 0)).grid(column=0, row=0)
        b1 = Button(color_button_grid, bg=self.theme['palette'][1], padx=8, width=1, height=1, highlightbackground=self.theme['palette'][1], command=lambda: self.changeColorButton(edit_card, 1)).grid(column=1, row=0)
        b2 = Button(color_button_grid, bg=self.theme['palette'][2], padx=8, width=1, height=1, highlightbackground=self.theme['palette'][2], command=lambda: self.changeColorButton(edit_card, 2)).grid(column=2, row=0)
        b3 = Button(color_button_grid, bg=self.theme['palette'][3], padx=8, width=1, height=1, highlightbackground=self.theme['palette'][3], command=lambda: self.changeColorButton(edit_card, 3)).grid(column=3, row=0)
        b4 = Button(color_button_grid, bg=self.theme['palette'][4], padx=8, width=1, height=1, highlightbackground=self.theme['palette'][4], command=lambda: self.changeColorButton(edit_card, 4)).grid(column=4, row=0)
        b5 = Button(color_button_grid, bg=self.theme['palette'][5], padx=8, width=1, height=1, highlightbackground=self.theme['palette'][5], command=lambda: self.changeColorButton(edit_card, 5)).grid(column=5, row=0)
        b6 = Button(color_button_grid, bg=self.theme['palette'][6], padx=8, width=1, height=1, highlightbackground=self.theme['palette'][6], command=lambda: self.changeColorButton(edit_card, 6)).grid(column=6, row=0)

        value_button_grid = Frame(button_grid, name='value_button_grid')
        value_button_grid.pack(side = tk.RIGHT, padx=MARGIN)
        decrease_points = Button(value_button_grid, activebackground=self.theme['buttonhighlight'], activeforeground=self.theme['palette'][edit_card.color_index], relief=GLOBALRELIEF, name='decrease_button', text='-', fg=self.theme['palette'][edit_card.color_index], bg=self.theme['bg'], width=1, height=1, highlightbackground=self.theme['palette'][edit_card.color_index], command=lambda: edit_card.decreasePoints()).grid(column=8, row=0)
        increase_points = Button(value_button_grid, activebackground=self.theme['buttonhighlight'], activeforeground=self.theme['palette'][edit_card.color_index], relief=GLOBALRELIEF, name='increase_button', text='+', fg=self.theme['palette'][edit_card.color_index], bg=self.theme['bg'], width=1, height=1, highlightbackground=self.theme['palette'][edit_card.color_index], command=lambda: edit_card.increasePoints()).grid(column=9, row=0)

        bottom_button_grid = Frame(self.edit_menu, name='bottom_button_grid', background=self.theme['bg'])
        bottom_button_grid.pack(pady=MARGIN, padx=MARGIN/10)
        close_button = Button(bottom_button_grid, activeforeground=self.theme['palette'][edit_card.color_index], activebackground=self.theme['buttonhighlight'], relief=GLOBALRELIEF, name='close_button', text='SAVE', fg=self.theme['palette'][edit_card.color_index], bg=self.theme['bg'], width=20, height=1, highlightbackground=self.theme['palette'][edit_card.color_index], command=lambda: self.closeEditMenu(edit_card, description_entry.get("1.0","end-1c"))).grid(column=3, row=0)
        delete_button = Button(bottom_button_grid, activeforeground=self.theme['palette'][edit_card.color_index], activebackground=self.theme['buttonhighlight'], relief=GLOBALRELIEF, name='delete_button', text='DELETE', fg=self.theme['palette'][edit_card.color_index], bg=self.theme['bg'], width=5, height=1, highlightbackground=self.theme['palette'][edit_card.color_index], command=lambda: self.deleteCard(edit_card, True)).grid(column=4, row=0)
        self.canvas.create_window(WIDTH/2, HEIGHT/2, anchor=CENTER, window=self.edit_menu)

    def changeColorButton(self, edit_card, color_index):
        edit_card.setColor(color_index)
        self.edit_menu.config(highlightbackground=self.theme['palette'][color_index], highlightcolor=self.theme['palette'][color_index])
        self.edit_menu.nametowidget('edit_menu_text').config(highlightcolor=self.theme['palette'][color_index], highlightbackground=self.theme['palette'][color_index], fg=self.theme['palette'][color_index])
        self.edit_menu.nametowidget('button_grid').nametowidget('value_button_grid').nametowidget('increase_button').config(activeforeground=self.theme['palette'][color_index], highlightbackground=self.theme['palette'][color_index], fg=self.theme['palette'][color_index])
        self.edit_menu.nametowidget('button_grid').nametowidget('value_button_grid').nametowidget('decrease_button').config(activeforeground=self.theme['palette'][color_index], highlightbackground=self.theme['palette'][color_index], fg=self.theme['palette'][color_index])
        self.edit_menu.nametowidget('bottom_button_grid').nametowidget('close_button').config(activeforeground=self.theme['palette'][color_index], highlightbackground=self.theme['palette'][color_index], fg=self.theme['palette'][color_index])
        self.edit_menu.nametowidget('bottom_button_grid').nametowidget('delete_button').config(activeforeground=self.theme['palette'][color_index], highlightbackground=self.theme['palette'][color_index], fg=self.theme['palette'][color_index])

    def closeEditMenu(self, edit_card, desc):
        edit_card.setDescription(desc)
        self.edit_menu.destroy()
        self.edit_menu = None
        self.saveCardstoFile()

    def deleteCard(self, card, editing=False):
        self.cards.remove(card)
        self.sections[card.section_index].cards.remove(card)
        card.delete()
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
            self.root.wm_attributes("-topmost", "true")
        else:
            self.root.wm_attributes("-topmost", "false")

    # --- Event Handlers ---
    def handleMouseMove(self, event):
        card = self.getColldingCards(event.x, event.y)
        for c in self.cards:
            if c == card:
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
            s.setColor(self.theme['bg'])
        if DAYCOUNTER:
            self.updateCardCounters()
        if not self.edit_menu:
            if self.grabbed_card:
                drop_section = self.getCollidingSections(event.x, event.y)
                if not drop_section:
                    drop_section = self.getCollidingSections(self.grab_location[0], self.grab_location[1])
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
            if self.isInArchiveDropzone(event.x, event.y):
                self.grabbed_card.displayPoints()
            else:
                self.grabbed_card.undisplayPoints()
            self.canvas.config(cursor='fleur')
            move_pos = (event.x - self.grab_offset[0], event.y - self.grab_offset[1])
            self.grabbed_card.move(move_pos[0], move_pos[1])
            section = self.getCollidingSections(event.x, event.y)
            for s in self.sections:
                s.setColor(self.theme['bg'])
            if section:
                section.setColor(self.theme['sectionhighlight'])

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
                self.grabbed_card.undrag()
                self.grabbed_card.hover()
                total_drag_distance = self.grab_location[0] - event.x, self.grab_location[1] - event.y
                if abs(total_drag_distance[1]) < DRAGTHRESHOLD/2:
                    if event.state & 0x4: # Check if Ctrl-Key is held, maybe i should make this bindable one day, who's to say, truly we do not know what life has in store for us on this crazy world so perhaps it would be best to leave this for another day such that I have plenty of time to ruminate on the ramifications of hardcoding this value in an event call, whos to say. Not I. Yippee.
                        if self.grabbed_card.color_index > 0:
                            self.grabbed_card.setColor(self.grabbed_card.color_index - 1)
                        else:
                            self.grabbed_card.setColor(len(self.theme['palette'])-1)
                    else:
                        if self.grabbed_card.color_index < len(self.theme['palette'])-1:
                            self.grabbed_card.setColor(self.grabbed_card.color_index + 1)
                        else:
                            self.grabbed_card.setColor(0)
                    og_position = (self.grab_location[0] - self.grab_offset[0], self.grab_location[1] - self.grab_offset[1])
                    self.grabbed_card.move(og_position[0], og_position[1])
                    self.grabbed_card.hover()
                    self.grabbed_card.unhover()
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
        
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=self.theme['bg'], fg=self.theme['secondary'], selectcolor=self.theme['secondary'], font=CARDFONT)
        themes_menu = tk.Menu(self.context_menu, tearoff=0, bg=self.theme['bg'], fg=self.theme['secondary'], selectcolor=self.theme['secondary'], font=CARDFONT)
        themes_menu.add_radiobutton(label="KB-Prime", variable=self.selected_theme, value='prime', command=lambda: self.setTheme('prime'))
        themes_menu.add_radiobutton(label="Tri.Optimum", variable=self.selected_theme, value='trioptimum', command=lambda: self.setTheme('trioptimum'))
        #themes_menu.add_radiobutton(label="Uplink", variable=self.selected_theme, value='uplink', command=lambda: self.setTheme('uplink'))
        #themes_menu.add_radiobutton(label="Peachy", variable=self.selected_theme, value='peach', command=lambda: self.setTheme('peach'))
        themes_menu.add_radiobutton(label="Fortress", variable=self.selected_theme, value='fortress', command=lambda: self.setTheme('fortress'))
        themes_menu.add_radiobutton(label="ihaveahax", variable=self.selected_theme, value='ihaveahax', command=lambda: self.setTheme('ihaveahax'))
        themes_menu.add_radiobutton(label="Custom", variable=self.selected_theme, value='custom', command=lambda: self.setTheme('custom'))

        if self.isInArchiveDropzone(event.x, event.y):
            self.context_menu.add_command(label="Reset Timer", command=lambda: self.archive_dropzone.resetTime())
            self.context_menu.add_command(label="Reset Points", command=lambda: self.archive_dropzone.resetArchive())
        elif self.grabbed_card:
                self.grab_location = (event.x, event.y)
                self.context_menu.add_command(label="Edit", command=lambda: self.openEditMenu(self.grabbed_card))
                self.context_menu.add_command(label="Delete", command=lambda: self.deleteCard(self.grabbed_card))
        else:
            self.context_menu.add_command(label="New Card", command=lambda: self.addNewCard())
        self.context_menu.add_separator()
        self.context_menu.add_checkbutton(label="Stay On Top", variable=self.pinned, onvalue=1, offvalue=0, command=lambda: self.setPinned())
        self.context_menu.add_cascade(label="Theme...", menu=themes_menu)
        self.context_menu.add_command(label="About", command=lambda: self.openWelcomeScreen())
        self.context_menu.add_command(label="Quit", command=lambda: sys.exit())
        self.context_menu.post(event.x_root, event.y_root)
    
    def setTheme(self, theme):
        self.selected_theme.set(theme)
        self.theme['name'] = theme
        self.theme['bg'] = THEMES[theme]['bg']
        self.theme['main'] = THEMES[theme]['main']
        self.theme['secondary'] = THEMES[theme]['secondary']
        self.theme['emptyslot'] = THEMES[theme]['emptyslot']
        self.theme['buttonhighlight'] = THEMES[theme]['buttonhighlight']
        self.theme['sectionhighlight'] = THEMES[theme]['sectionhighlight']
        self.theme['palette'] = [THEMES[theme]['palette'][0],
                THEMES[theme]['palette'][1],
                THEMES[theme]['palette'][2],
                THEMES[theme]['palette'][3],
                THEMES[theme]['palette'][4],
                THEMES[theme]['palette'][5],
                THEMES[theme]['palette'][6],
            ]
        if self.canvas:
            self.canvas.config(self.canvas, highlightbackground=self.theme['main'])
            for s in self.sections:
                s.theme = self.theme
                s.setColor(self.theme['bg'])
                for d in s.drop_zones:
                    d.theme = self.theme
                    d.draw()
            for c in self.cards:
                c.theme = self.theme
                c.setColor(c.color_index)
            self.archive_dropzone.draw()


        settings_yaml = None
        with open(SETTINGS_PATH, 'r') as file:
            settings_yaml = yaml.safe_load(file)
        settings['theme'] = self.theme['name']
        with open(SETTINGS_PATH, 'w') as file:
            yaml.safe_dump(settings, file, sort_keys=False)
    # --- Welcome Screen ---
    def openWelcomeScreen(self):
        self.edit_menu = Frame(self.root, name='welcome_screen', relief=GLOBALRELIEF, bg=self.theme['bg'], padx=MARGIN*2, pady=MARGIN*2, highlightcolor=self.theme['secondary'], highlightbackground=self.theme['secondary'], highlightthickness=1, height=HEIGHT-(MARGIN*2), width=WIDTH-(MARGIN*2))        
        self.edit_menu.pack(fill=BOTH, expand=False, padx=MARGIN, pady=MARGIN)
        
        welcome_grid = Frame(self.edit_menu, name='welcome_grid', background=self.theme['bg'])
        welcome_grid.pack(padx=MARGIN, pady=MARGIN/4)

        welcome = Label(welcome_grid, text="Welcome to Kanbuddy!", font=HEADERFONT, bg=self.theme['bg'], fg=self.theme['secondary'], padx=MARGIN, pady=MARGIN).grid(column=0, row=0)
        byline = Label(welcome_grid, text="by kerfluffle", font=HEADERFONT, bg=self.theme['bg'], fg=self.theme['secondary'], padx=MARGIN, pady=MARGIN).grid(column=0, row=1)

        instructions = Label(welcome_grid, font=CARDFONT, text=
'''
- CTRL-A : New Card
- Double-Click : Edit Card
- Middle-Click : Cycle Card Color (+CTRL to Reverse)
- Middle-Click + Drag : Adjust Card Points
- Drag card to bottom-right box to mark as complete.

- Fonts, colors and more can be changed in settings.yaml
''', bg=self.theme['bg'], fg=self.theme['secondary'], justify=tk.LEFT).grid(column=0, row=2)
        bottom_button_grid = Frame(self.edit_menu, name='bottom_button_grid', background=self.theme['bg'])
        bottom_button_grid.pack(pady=MARGIN, padx=MARGIN/10)
        close_button = Button(bottom_button_grid, text="Enter the World of Kanbuddy", activeforeground=self.theme['secondary'], activebackground=self.theme['buttonhighlight'], relief=GLOBALRELIEF, bg=self.theme['bg'], fg=self.theme['secondary'], padx=MARGIN, highlightbackground=self.theme['secondary'], command=lambda: self.closeWelcomeScreen()).grid(column=0,row=0)
        website_button = Button(bottom_button_grid, text="Kerflufflespace↗", activeforeground=self.theme['secondary'], activebackground=self.theme['buttonhighlight'], relief=GLOBALRELIEF, bg=self.theme['bg'], fg=self.theme['secondary'], padx=MARGIN, highlightbackground=self.theme['secondary'], command=lambda: webbrowser.open_new_tab('https://kerfluffle.space')).grid(column=1,row=0, padx=10)
        self.canvas.create_window(WIDTH/2, HEIGHT/2, anchor=CENTER, window=self.edit_menu)

    def closeWelcomeScreen(self):
        self.edit_menu.destroy()
        self.edit_menu = None

# Import sections
k = Kanban(settings['theme'])

sections = settings['sections']
sum_width = 0
if not os.path.isfile(archive_filepath):
    k.openWelcomeScreen()

for sec in sections:
    if sec == sections[-1]:
        last_section_flag = True
        k.addSectionFromFile(sec['name'], int(sec['width']), sum_width, int(sec['cards']), True)
        k.archive_dropzone = k.sections[len(k.sections)-1].archive_dropzone
    else:   
        k.addSectionFromFile(sec['name'], int(sec['width']), sum_width, int(sec['cards']))
    sum_width += int(sec['width'])

# Import cards
if os.path.isfile(cards_filepath):
    with open(cards_filepath, 'r', newline='\n') as csvfile:
        cards = csv.DictReader(csvfile, delimiter='|')
        for c in cards:
            k.addCardFromFile(int(c['section_index']), c['description'], int(c['color_index']), int(c['points']), date.fromisoformat(c['creation_date']))
    csvfile.close()
k.root.mainloop()
