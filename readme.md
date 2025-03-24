

# -[O-O]- Kanbuddy 
A micro-kanban worktime buddy to help you keep on track during a work session.

![buddy](https://github.com/user-attachments/assets/917514e5-8f72-42ac-8461-ae4413108d78)

## Installation

#### Release (Reccomended)
1. Download build for your OS from [Releases](https://github.com/Nosler/kanbuddy/releases) (when it exists)
2. Launch it.

#### Python
1. Clone git repository
2. run ``pip install requirements.txt`` (when it exists)
3. ``python3 kanbuddy.py``

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
- Line Dashes
- Sections (The last section will always have the final card spot replaced with the point counter.)

The Default font is [GNU Unifont](https://www.unifoundry.com/unifont/index.html). Kanbuddy will work with any installed font. Do not use spaces when entering font name. 

### Philosophy
I use kanbuddy as an auto-launching companion for my workspace. On my Linux setup, I like to create [.desktop](https://wiki.archlinux.org/title/Desktop_entries) files that will call scripts to open all relevant programs at once to reduce as much friction as possible when starting a work session.

For example, when I want to work on my soda-themed horror game, I click the .desktop file that then launches all relevant programs, including Kanbuddy.
```bash
code "{home}/sodagame/" & # Open Code Editor & Git Client 
/usr/bin/godot "{home}/sodagame/project.godot" & # Open Game Editor
cd "{home}/sodagame/kanbuddy/" & # Navigate to the Kanbuddy Directory
./kanbuddy" # Open Kanbuddy
```
 If calling kanbuddy from within a script, you **must** cd to it first for it to look within the correct directory for its configuration files. This allows you to have as many different Kanbuddy instances as you have directories. I personally use a different kanbuddy instance for every project I have.
