![Screenshot of Kanbuddy interface](https://i.imgur.com/5TRPGwr.png)

# Kanbuddy
A micro-kanban board for people who need help focusing on the short-term stuff.

## Installation

### Release (Reccomended)
- Download respective build from Releases
- Launch it.

### Python
- Clone git repository
- run ```pip install requirements.txt```
- this isnt done so dont worry it wont work

## Operation
- CTRL-A : New Card
- Double-Click : Edit Card
- Middle-Click : Cycle Card Color (+CTRL to Reverse)
- Middle-Click + Drag : Adjust Card Points

Once a card has been completed, drop it in the bottom-right spot and watch your points go up!

## Settings
Within ``settings.yaml``, the following can be adjusted:
- Fonts
- Custom Theme (Any hex code, or [Tkinter Color](https://www.wikipython.com/wp-content/uploads/Color-chart-capture-082321.jpg))
- Window size
- Margin/Header size
- Day counter

Sections can also be added or removed from the board. You can adjust the section title, width and number of cards within the section. The last section will always have the final card spot replaced with the point counter.
