from multiprocessing import pool
import tkinter as tk
import config


class TickerWindow:
    """
    Template class for a ticker window. All/most of the code here
    is "backend" and widgets are not drawn via tk.grid(). This is intended
    to be inherited in the GUI classes where objects will be drawn and
    functions/widgets overridden if needed.

    Args:
        app(the main tkinter object)

    Required Overrides(inside child object):
        on_click_help(needs custom dialogue in help windows)
        timer_update(needs different values/behavior for countdown timers)
        timerValue(set to maximum timer rate value)
    Required widget draw(grid()) calls(inside child object):
        labelName
        labelChange
        labelVol
        labelBuf
        sortByName
        sortByChange
        sortByVol
        notifyBell
        help
        yScroll
        listName
        listChange
        listVol
        timerLabel
        timerFrame
        timerDisp
    """
    def __init__(self, app):
        self.app = app
        self.pool = pool.ThreadPool(processes=1)
        self.async = pool.AsyncResult
        self.ticker_data = []

        self.create_labels()
        self.create_buttons()
        self.create_lists()
        self.create_timer()

    def create_labels(self):
        color_options = {'bg': config.MAIN_BG,
                         'fg': config.TEXT_COLOR}

        self.labelName = tk.Label(text='Market Name', **color_options)

        self.labelChange = tk.Label(text='Change', **color_options)

        self.labelVol = tk.Label(text='Volume', **color_options)

        self.labelBuf = tk.Frame(width=120, height=42, bg=config.MAIN_BG)

    def create_buttons(self):
        color_options = {'bg': config.MAIN_BG,
                         'activebackground': config.CLICKED_BG}

        self.sortByName = tk.Button(relief='raised', image=self.app.noArrow,
                                    command=lambda: self.on_click_sort('sortByName'),
                                    **color_options)

        self.sortByChange = tk.Button(relief='raised', image=self.app.downArrow,
                                      command=lambda: self.on_click_sort('sortByChange'),
                                      **color_options)

        self.sortByVol = tk.Button(relief='raised', image=self.app.noArrow,
                                   command=lambda: self.on_click_sort('sortByVol'),
                                   **color_options)

        self.buttons = {'sortByName': ['none', 0],
                        'sortByChange': ['desc', 1],
                        'sortByVol': ['none', 2]}

        self.notifyBell = tk.Button(relief='raised', image=self.app.notifyBell,
                                    command=lambda: self.on_click_notif(),
                                    **color_options)
        self.notifyIsActive = False

        self.help = tk.Button(relief='flat', image=self.app.questionMark,
                              command=lambda: self.on_click_help(),
                              **color_options)

    def on_click_sort(self, pressed_name):
        for b_name in self.buttons:
            if b_name == pressed_name:
                sort_direction = self.buttons[b_name][0]
                if sort_direction == 'desc':
                    self.buttons[b_name][0] = 'asc'
                    getattr(self, b_name).config(image=self.app.upArrow)
                    self.ticker_data.sort(key=lambda x: x[self.buttons[b_name][1]])
                if sort_direction == 'asc' or sort_direction == 'none':
                    self.buttons[b_name][0] = 'desc'
                    getattr(self, b_name).config(image=self.app.downArrow)
                    self.ticker_data.sort(key=lambda x: x[self.buttons[b_name][1]],
                                          reverse=True)
            else:
                self.buttons[b_name][0] = 'none'
                getattr(self, b_name).config(image=self.app.noArrow)
        self.display_ticker()
        
    def on_click_notif(self):
        if self.notifyBell.cget('relief') == 'raised':
            self.notifyBell.config(relief='sunken')
            self.notifyIsActive = True
        else:
            self.notifyBell.config(relief='raised')
            self.notifyIsActive = False

    def on_click_help(self):
        pass
        
    def create_lists(self):
        self.yScroll = tk.Scrollbar(orient=tk.VERTICAL, command=self.on_vsb)

        color_options = {'bg': config.LIGHT_BG,
                         'fg': config.TEXT_COLOR,
                         'selectbackground': config.LIGHT_BG,
                         'selectforeground': config.TEXT_COLOR,
                         'highlightcolor': config.LIGHT_BG,
                         'highlightbackground': config.LIGHT_BG}

        self.listName = tk.Listbox(activestyle='none', relief='sunken',
                                   yscrollcommand=self.yScroll.set,
                                   width=40, height=6, **color_options)
        self.listName.bind('<MouseWheel>', self.on_mouse_wheel)

        self.listChange = tk.Listbox(activestyle='none', relief='sunken',
                                     yscrollcommand=self.yScroll.set,
                                     width=8, height=6, **color_options)
        self.listChange.bind('<MouseWheel>', self.on_mouse_wheel)

        self.listVol = tk.Listbox(activestyle='none', relief='sunken',
                                  yscrollcommand=self.yScroll.set,
                                  width=8, height=6, **color_options)
        self.listVol.bind('<MouseWheel>', self.on_mouse_wheel)

    def on_vsb(self, *args):
        self.listName.yview(*args)
        self.listChange.yview(*args)
        self.listVol.yview(*args)

    def on_mouse_wheel(self, event):
        if event.delta < 0:
            self.listName.yview('scroll', 1, 'units')
            self.listChange.yview('scroll', 1, 'units')
            self.listVol.yview('scroll', 1, 'units')
        if event.delta > 0:
            self.listName.yview('scroll', -1, 'units')
            self.listChange.yview('scroll', -1, 'units')
            self.listVol.yview('scroll', -1, 'units')
        return 'break'

    def create_timer(self):
        self.timerLabel = tk.Label(text='Time until update:', bg=config.MAIN_BG, fg=config.TEXT_COLOR)

        self.timerFrame = tk.LabelFrame(width=120, height=120, bg=config.MAIN_BG)

        self.timerDisp = tk.Label(font=('', 20), bg=config.MAIN_BG, fg=config.TEXT_COLOR)

        self.timerValue = 0

    def timer_update(self):
        pass

    def sort_ticker(self):
        if self.ticker_data:
            for b_name in self.buttons:
                if self.buttons[b_name][0] == 'desc':
                    self.ticker_data.sort(key=lambda x: x[self.buttons[b_name][1]],
                                          reverse=True)
                if self.buttons[b_name][0] == 'asc':
                    self.ticker_data.sort(key=lambda x: x[self.buttons[b_name][1]])
        self.display_ticker()

    def display_ticker(self):
        self.listName.delete(0, tk.END)
        self.listChange.delete(0, tk.END)
        self.listVol.delete(0, tk.END)
        for i in self.ticker_data:
            self.listName.insert(tk.END, f'{i[0]}')
            self.listChange.insert(tk.END, f'+{i[1]:.02f}%')
            self.listVol.insert(tk.END, f'{i[2]:.02f}')
        self.app.update()
