from playsound import playsound
import tkinter as tk
import slowtick


class SlowMarket:
    def __init__(self, app, cfg):
        self.app = app
        self.cfg = cfg

        slowtick.delete_ancient_pickles()
        self.create_labels()
        self.create_buttons()
        self.create_lists()
        self.create_timer()

        self.timer_update()

    def create_labels(self):
        self.slowLabelName = tk.Label(text='Market Name', bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.slowLabelName.grid(row=0, column=0, sticky='NSWE')

        self.slowLabelChange = tk.Label(text='Change', bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.slowLabelChange.grid(row=0, column=1, sticky='NSWE')

        self.slowLabelVol = tk.Label(text='Volume', bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.slowLabelVol.grid(row=0, column=2, sticky='NSWE')

        self.slowLabelBuf = tk.Frame(width=120, height=42, bg=self.cfg.MAIN_BG)
        self.slowLabelBuf.grid(row=0, rowspan=2, column=4, columnspan=3)

    def create_buttons(self):
        self.slowSortByName = tk.Button(name='slowSortByName', image=self.cfg.noArrow,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='raised',
            command=lambda: self.on_click_sort('slowSortByName', self.slowButtons))
        self.slowSortByName.grid(row=1, column=0, sticky='NSWE')

        self.slowSortByChange = tk.Button(name='slowSortByChange', image=self.cfg.downArrow,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='raised',
            command=lambda: self.on_click_sort('slowSortByChange', self.slowButtons))
        self.slowSortByChange.grid(row=1, column=1, sticky='NSWE')

        self.slowSortByVol = tk.Button(name='slowSortByVol', image=self.cfg.noArrow,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='raised',
            command=lambda: self.on_click_sort('slowSortByVol', self.slowButtons))
        self.slowSortByVol.grid(row=1, column=2, sticky='NSWE')

        self.slowButtons = {self.slowSortByName: ['none', 0],
                            self.slowSortByChange: ['desc', 1],
                            self.slowSortByVol: ['none', 2]}

        self.slowNotifyBell = tk.Button(name='slowNotifyBell', image=self.cfg.notifyBell,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='raised',
            command=lambda: self.on_click_notif())
        self.slowNotifyBell.grid(row=1, column=3, sticky='NSWE')

        self.slowNotifyIsActive = False

        self.slowHelp = tk.Button(name='slowHelp', image=self.cfg.questionMark,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='flat',
            command=lambda: self.on_click_help())
        self.slowHelp.grid(row=0, column=4, sticky='E')

    def on_click_sort(self, pressed_name, buttons):
        for b_name in buttons:
            if str(b_name) == ('.' + pressed_name):
                sort_direction = buttons[b_name][0]
                if sort_direction == 'desc':
                    buttons[b_name][0] = 'asc'
                    b_name.config(image=self.cfg.upArrow)
                    self.slow_ticker_data.sort(key=lambda x: x[buttons[b_name][1]])
                if sort_direction == 'asc' or sort_direction == 'none':
                    buttons[b_name][0] = 'desc'
                    b_name.config(image=self.cfg.downArrow)
                    self.slow_ticker_data.sort(key=lambda x: x[buttons[b_name][1]],
                                          reverse=True)
            else:
                buttons[b_name][0] = 'none'
                b_name.config(image=self.cfg.noArrow)
        self.output_ticker()
        self.app.update()

    def on_click_notif(self):
        if self.slowNotifyBell.cget('relief') == 'raised':
            self.slowNotifyBell.config(relief='sunken')
            self.slowNotifyIsActive = True
        else:
            self.slowNotifyBell.config(relief='raised')
            self.slowNotifyIsActive = False

    def on_click_help(self):
        helpWindow = tk.Toplevel()
        helpWindow.title('Help')

        frameBuf = tk.Frame(helpWindow,
            width=203, height=185, bg=self.cfg.MAIN_BG)
        frameBuf.grid(row=0, rowspan=4, column=0, columnspan=3)

        msg1 = tk.Message(helpWindow,
            bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR, width=192,
            text='This section shows % change over '
                '{0} measurements. Recorded once '
                'every {1} minutes.'
                .format(abs(self.cfg.SLOWTICK_LB)+1,
                        self.cfg.SLOWTICK_RATE/60))
        msg1.grid(row=0, columnspan=3)

        msg2 = tk.Message(helpWindow,
            bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR, width=200,
            text='The arrow buttons can be used to '
                'sort data according to the '
                'label it is under.')
        msg2.grid(row=1, columnspan=3)

        msg3 = tk.Message(helpWindow,
            bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR, width=200,
            text='The bell button can be toggled '
                'on and off to play a notification '
                'when the ticker has been updated.')
        msg3.grid(row=2, columnspan=3)

        dismissButton = tk.Button(helpWindow, text='Dismiss',
            command=helpWindow.destroy)
        dismissButton.grid(row=3, column=1, sticky='WE')

    def create_lists(self):
        self.slow_ticker_data = []

        self.slowYBarBuf = tk.Frame(bg=self.cfg.MAIN_BG, width=24)
        self.slowYBarBuf.grid(row=0, column=3, sticky='NS')

        self.slowYScroll = tk.Scrollbar(orient=tk.VERTICAL, command=self.on_vsb)
        self.slowYScroll.grid(row=2, column=3, sticky='NS')

        self.slowListName = tk.Listbox(activestyle='none',
            bg=self.cfg.LIGHT_BG, fg=self.cfg.TEXT_COLOR, selectbackground=self.cfg.LIGHT_BG,
            selectforeground=self.cfg.TEXT_COLOR, relief='sunken',
            highlightcolor=self.cfg.LIGHT_BG, highlightbackground=self.cfg.LIGHT_BG,
            width=40, height=6, yscrollcommand=self.slowYScroll.set)
        self.slowListName.bind('<MouseWheel>', self.on_mouse_wheel)
        self.slowListName.grid(row=2, column=0, sticky='NSWE')

        self.slowListChange = tk.Listbox(activestyle='none',
            bg=self.cfg.LIGHT_BG, fg=self.cfg.TEXT_COLOR, selectbackground=self.cfg.LIGHT_BG,
            selectforeground=self.cfg.TEXT_COLOR, relief='sunken',
            highlightcolor=self.cfg.LIGHT_BG, highlightbackground=self.cfg.LIGHT_BG,
            width=8, height=6, yscrollcommand=self.slowYScroll.set)
        self.slowListChange.bind('<MouseWheel>', self.on_mouse_wheel)
        self.slowListChange.grid(row=2, column=1, sticky='NSWE')

        self.slowListVol = tk.Listbox(activestyle='none',
            bg=self.cfg.LIGHT_BG, fg=self.cfg.TEXT_COLOR, selectbackground=self.cfg.LIGHT_BG,
            selectforeground=self.cfg.TEXT_COLOR, relief='sunken',
            highlightcolor=self.cfg.LIGHT_BG, highlightbackground=self.cfg.LIGHT_BG,
            width=8, height=6, yscrollcommand=self.slowYScroll.set)
        self.slowListVol.bind('<MouseWheel>', self.on_mouse_wheel)
        self.slowListVol.grid(row=2, column=2, sticky='NSWE')

    def on_vsb(self, *args):
        self.slowListName.yview(*args)
        self.slowListChange.yview(*args)
        self.slowListVol.yview(*args)

    def on_mouse_wheel(self, event):
        if event.delta < 0:
            self.slowListName.yview('scroll', 1, 'units')
            self.slowListChange.yview('scroll', 1, 'units')
            self.slowListVol.yview('scroll', 1, 'units')
        if event.delta > 0:
            self.slowListName.yview('scroll', -1, 'units')
            self.slowListChange.yview('scroll', -1, 'units')
            self.slowListVol.yview('scroll', -1, 'units')
        return 'break'

    def create_timer(self):
        self.slowTimerLabel = tk.Label(text='Time until update:',
            bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.slowTimerLabel.grid(row=1, column=4, ipadx=8)

        self.slowTimerFrame1 = tk.LabelFrame(width=120, height=120, bg=self.cfg.MAIN_BG)
        self.slowTimerFrame1.grid(row=2, column=4, columnspan=3)

        self.slowTimerDisp = tk.Label(font=('', 20), bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.slowTimerDisp.grid(row=2, column=4)

        self.slowTimerValue = self.cfg.SLOWTICK_RATE

    def timer_update(self):
        if self.slowTimerValue == 0:
            self.update_slow_ticker_data()
            self.slowTimerValue = self.cfg.SLOWTICK_RATE
            if self.slowNotifyIsActive and self.slow_ticker_data:
                playsound('media/notification_sound.mp3')
        values = divmod(self.slowTimerValue, 60)
        minutes = values[0]
        seconds = values[1]
        self.slowTimerDisp.config(text='{}:{:0>2}'.format(minutes, seconds))
        self.slowTimerValue -= 1
        self.app.after(1000, self.timer_update)

    def update_slow_ticker_data(self):
        self.slow_ticker_data = slowtick.heartbeat(self.cfg)
        if self.slow_ticker_data:
            for b_name in self.slowButtons:
                if self.slowButtons[b_name][0] == 'desc':
                    self.slow_ticker_data.sort(key=lambda x: x[self.slowButtons[b_name][1]],
                                          reverse=True)
                if self.slowButtons[b_name][0] == 'asc':
                    self.slow_ticker_data.sort(key=lambda x: x[self.slowButtons[b_name][1]])
        self.output_ticker()

    def output_ticker(self):
        self.slowListName.delete(0, tk.END)
        self.slowListChange.delete(0, tk.END)
        self.slowListVol.delete(0, tk.END)
        for i in self.slow_ticker_data:
            self.slowListName.insert(tk.END, i[0])
            self.slowListChange.insert(tk.END, '{}{}{}'.format('+', i[1], '%'))
            self.slowListVol.insert(tk.END, i[2])
        self.app.update()