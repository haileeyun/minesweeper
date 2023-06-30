import sys
from tkinter import *
import random

#import minesweeper
import minesweeper_settings
import ctypes
import os


class Cell:
    all = []
    cell_count = minesweeper_settings.cell_count
    cell_count_label_object = None
    retry = False

    def __init__(self, x, y, is_mine = False):
        self.is_mine = is_mine
        self.is_opened = False
        self.flag = False
        self.cell_button_object = None
        self.x = x
        self.y = y

        #appemd the object to the Cell.all list
        Cell.all.append(self)

    def create_button_object(self, location):
        #make adjustable later for grid size
        button = Button(
            location,
            width = 10,
            height = 4

        )
        # "<Button-1>" means left click
        button.bind("<Button-1>", self.left_click_actions) #left click
        button.bind("<Button-3>", self.right_click_actions) #right click
        self.cell_button_object = button

    @staticmethod #has to be static because you don't want to call it for every single cell
    def create_cell_count_label(location):
        label = Label(
            location,
            bg = minesweeper_settings.background_color,
            fg = "white",
            text = f"cells left: {Cell.cell_count}",
            width = 12,
            height = 5,
            font = ("Lexend", 30, "bold")
        )
        Cell.cell_count_label_object = label

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.num_of_mines == 0:
                for cell_object in self.surrounded_cells:
                    cell_object.show_cell()
            self.show_cell()
            #if mines count == cells left count, then player won
            if Cell.cell_count == minesweeper_settings.mines_count:
                ctypes.windll.user32.MessageBoxW(0, "yay!!! u won!!!", "game over", 0)
        #cancel left and right click events if the cell is already opened
        self.cell_button_object.unbind("<Button-1>")
        self.cell_button_object.unbind("<Button-3>")

    def get_cell_by_axis(self, x, y):
        #return a cell object based on the value of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]
        cells = [cell for cell in cells if cell]  # elimates the Nones
        return cells

    @property
    def num_of_mines(self):
        count = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                count += 1
        return count

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            #testing font weight
            #myFont = font.Font(weight="bold")
            self.cell_button_object.configure(text = self.num_of_mines,)
            #self.cell_button_object.configure(fg = "red")
            #update cell count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text = f"cells left: {Cell.cell_count}")
            #if this was flagged, we should change the background color to SystemButtonFase
            self.cell_button_object.configure(bg = "SystemButtonFace")
        self.is_opened = True


    def show_mine(self):
        global retry
        # a logic to interrupt game and display message that player lost
        self.cell_button_object.configure(bg="red")
        result  = ctypes.windll.user32.MessageBoxW(0, "you clicked on a mine!", "GAME OVER", 5)
        if result == 4: #if the user presses retry
            print("retry")
            Cell.retry = True

            #os.execl(sys.executable, sys.executable, *sys.argv)

        else:
            sys.exit()
        # 4 = yes no
        # 5 = retry, cancel


    def right_click_actions(self, event):
        if not self.flag:
            self.cell_button_object.configure(bg = "red")

            self.flag = True
        else:
            self.cell_button_object.configure(bg = "SystemButtonFace")
            self.flag = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, minesweeper_settings.mines_count)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

