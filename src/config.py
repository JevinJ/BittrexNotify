import tkinter as tk

class Config(tk.Frame):
    def __init__(self):
        # Slowtick constants
        self.SLOWTICK_RATE = 600
        self.SLOWTICK_LB = -1
        self.SLOWTICK_MIN_PRICE = 0.00001000
        self.SLOWTICK_MIN_CHANGE = 3
        self.SLOWTICK_MIN_VOL = 350

        # Fasttick constants
        self.FASTTICK_RATE = 15
        self.FASTTICK_LB = -9
        self.FASTTICK_MIN_PRICE = 0.00001000
        self.FASTTICK_MIN_RATE = .2
        self.FASTTICK_MIN_VOL = 350

        # Color constants for GUI
        self.CLICKED_BG = '#3D3D3D'
        self.MAIN_BG = '#262626'
        self.LIGHT_BG = '#2B2B2B'
        self.TEXT_COLOR = '#AFBDCC'

        # Images used by GUI
        self.downArrow = tk.PhotoImage(file='media/down_arrow.png')
        self.upArrow = tk.PhotoImage(file='media/up_arrow.png')
        self.noArrow = tk.PhotoImage(file='media/no_arrow.png')
        self.notifyBell = tk.PhotoImage(file='media/notification_bell.png')
        self.questionMark = tk.PhotoImage(file='media/question_mark.png')