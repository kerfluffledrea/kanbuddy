![Screenshot of Kanbuddy interface](https://i.imgur.com/5TRPGwr.png)

## Kanbuddy
A micro-kanban board for people who need help focusing on the short-term stuff.

### Operation
Launch: ``python3 kanbuddy.py``
- Create a new card with CTRL-A
- Double click card to edit.
- Once a card has been completed, drop it in the bottom-right spot and watch your points go up!

### Settings
Within ``settings.json``, the following can be adjusted:
- Fonts (Any [tkinter fonts](https://stackoverflow.com/a/64301819))
- Color Scheme (Any hex code, or [Tkinter Color](https://www.wikipython.com/wp-content/uploads/Color-chart-capture-082321.jpg))
- Window size
- Margin/Header size
- Day counter

Sections can also be added or removed from the board. You can adjust the section title, width and card height within the section. The last section will always have the final card spot replaced with the point counter.
