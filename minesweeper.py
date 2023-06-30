from tkinter import *
import minesweeper_settings
import minesweeper_utilities
from minesweeper_cell import Cell
import os

root = Tk()
#override the settings of the window
root.configure(bg = minesweeper_settings.background_color) #sets background color
root.geometry(f"{minesweeper_settings.width}x{minesweeper_settings.height}") #change the size of the window
root.title("minesweeper!")
root.resizable(False, False) #freezes resizing

#frame is like a coordinate system
top_frame = Frame(
    root,
    bg = minesweeper_settings.background_color, #change later to black
    width = minesweeper_settings.width,
    height = minesweeper_utilities.height_percentage(20) #25% of the window
                  )
top_frame.place(x = 0, y = 0)

game_title = Label(
    top_frame,
    bg = minesweeper_settings.background_color,
    fg = "white",
    text = "minesweeper",
    font = ("Lexend", 48, "bold")

)

game_title.place(x = minesweeper_utilities.width_percentage(35), y = minesweeper_utilities.height_percentage(5))

#side bar
left_frame = Frame(
    root,
    bg = minesweeper_settings.background_color,
    width = minesweeper_utilities.width_percentage(25),
    height = minesweeper_utilities.height_percentage(75)
)
left_frame.place(x = 0, y = minesweeper_utilities.height_percentage(25))

center_frame = Frame(
    root,
    bg = minesweeper_settings.background_color,
    width = minesweeper_utilities.width_percentage(75),
    height = minesweeper_utilities.height_percentage(75)

)

#try to center this
center_frame.place(
    x = minesweeper_utilities.width_percentage(30),
    y = minesweeper_utilities.height_percentage(20)
)

def restart_program():
    # python = sys.executable
    # os.execl(sys.executable, sys.executable, *sys.argv)
    root.destroy()
    os.startfile("minesweeper.py")


for x in range(minesweeper_settings.grid_size):
    for y in range(minesweeper_settings.grid_size):
        c = Cell(x, y)
        c.create_button_object(center_frame)
        c.cell_button_object.grid(column = x, row = y)




# call the label from the Cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x = 0, y = 0)

Cell.randomize_mines()

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

if Cell.retry == True:
    print("foeeee")
    restart_program()
print(Cell.retry)

#run the window
root.mainloop() #makes the screen until the x is pressed