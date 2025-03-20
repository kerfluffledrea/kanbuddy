![Screenshot of Kanbuddy interface]()

# Kanbuddy
A micro-kanban board for people who need help focusing on the short-term stuff.

## Installation

#### Release (Reccomended)
1. Download respective build from [Releases](https://github.com/Nosler/kanbuddy/releases)
2. Launch it.

#### Python
1. Clone git repository
2. run ```pip install requirements.txt```
3. this isnt done so dont worry it wont work

## Operation
- CTRL-A : New Card
- Double-Click : Edit Card
- Middle-Click : Cycle Card Color (+CTRL to Reverse)
- Middle-Click + Drag : Adjust Card Points

Once a card has been completed, drop it in the bottom-right spot and watch your points go up!

Kanbuddy will populate its settings and cards from ``settings.yaml``, ``.cards.csv``, and ``.archive.csv`` files located within the **current working directory** that the program was launched from.

#### Settings
Within ``settings.yaml``, you can adjust:
- Fonts
- Custom Theme (Any hex code, or [Tkinter Color](https://www.wikipython.com/wp-content/uploads/Color-chart-capture-082321.jpg))
- Window size
- Margin/Header size
- Day counter
- Sections (The last section will always have the final card spot replaced with the point counter.)

### Philosophy
I use kanbuddy as an auto-launching companion for my workspace. On my Linux setup, I like to create [.desktop](https://wiki.archlinux.org/title/Desktop_entries) files that will call scripts to open all relevant programs at once to reduce as much friction as possible when starting a work session.

For example, when I want to work on my soda-themed horror game, I click the .desktop file that then launches all relevant programs, including Kanbuddy.
```bash
code "{home}/sodagame/" & # Code Editor & Git Client 
/usr/bin/godot "{home}/sodagame/project.godot" & # Game Editor
cd "{home}/sodagame/kanbuddy/" & # Navigate to the Kanbuddy Directory
./kanbuddy" # Kanbuddy
```
 If calling kanbuddy from within a script, you **must** cd to it first for it to look within the correct directory for its configuration files. This allows you to have as many different Kanbuddy instances as you have directories. I personally use a different kanbuddy instance for every project I have.

