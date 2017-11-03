from playsound import playsound
import tkinter as tk
import fasttick


class FastMarket:
    def __init__(self, app, cfg):
        self.app = app
        self.cfg = cfg

        fasttick.delete_ancient_pickles()
        self.create_labels()
        self.create_buttons()
        self.create_lists()
        self.create_timer()

        self.timer_update()

    def create_labels(self):
        self.fastLabelName = tk.Label(text='Market Name', bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.fastLabelName.grid(row=3, column=0, sticky='NSWE')

        self.fastLabelChange = tk.Label(text='Rate', bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.fastLabelChange.grid(row=3, column=1, sticky='NSWE')

        self.fastLabelVol = tk.Label(text='Volume', bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.fastLabelVol.grid(row=3, column=2, sticky='NSWE')

        self.fastLabelBuf = tk.Frame(width=120, height=42, bg=self.cfg.MAIN_BG)
        self.fastLabelBuf.grid(row=3, rowspan=2, column=4, columnspan=3)

    def create_buttons(self):
        self.fastSortByName = tk.Button(name='fastSortByName', image=self.cfg.noArrow,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='raised',
            command=lambda: self.on_click_sort('fastSortByName', self.fastButtons))
        self.fastSortByName.grid(row=4, column=0, sticky='NSWE')

        self.fastSortByRate = tk.Button(name='fastSortByRate', image=self.cfg.downArrow,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='raised',
            command=lambda: self.on_click_sort('fastSortByRate', self.fastButtons))
        self.fastSortByRate.grid(row=4, column=1, sticky='NSWE')

        self.fastSortByVol = tk.Button(name='fastSortByVol', image=self.cfg.noArrow,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='raised',
            command=lambda: self.on_click_sort('fastSortByVol', self.fastButtons))
        self.fastSortByVol.grid(row=4, column=2, sticky='NSWE')

        self.fastButtons = {self.fastSortByName: ['none', 0],
                            self.fastSortByRate: ['desc', 1],
                            self.fastSortByVol: ['none', 2]}

        self.fastNotifyBell = tk.Button(name='fastNotifyBell', image=self.cfg.notifyBell,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='raised',
            command=lambda: self.on_click_notif())
        self.fastNotifyBell.grid(row=4, column=3, sticky='NSWE')

        self.fastNotifyIsActive = False

        self.fastHelp = tk.Button(name='fastHelp', image=self.cfg.questionMark,
            bg=self.cfg.MAIN_BG, activebackground=self.cfg.CLICKED_BG, relief='flat',
            command=lambda: self.on_click_help())
        self.fastHelp.grid(row=3, column=4, sticky='E')

    def on_click_sort(self, pressed_name, buttons):
        for b_name in buttons:
            if str(b_name) == ('.' + pressed_name):
                sort_direction = buttons[b_name][0]
                if sort_direction == 'desc':
                    buttons[b_name][0] = 'asc'
                    b_name.config(image=self.cfg.upArrow)
                    self.fast_ticker_data.sort(key=lambda x: x[buttons[b_name][1]])
                if sort_direction == 'asc' or sort_direction == 'none':
                    buttons[b_name][0] = 'desc'
                    b_name.config(image=self.cfg.downArrow)
                    self.fast_ticker_data.sort(key=lambda x: x[buttons[b_name][1]],
                                          reverse=True)
            else:
                buttons[b_name][0] = 'none'
                b_name.config(image=self.cfg.noArrow)
        self.output_ticker()
        self.app.update()

    def on_click_notif(self):
        if self.fastNotifyBell.cget('relief') == 'raised':
            self.fastNotifyBell.config(relief='sunken')
            self.fastNotifyIsActive = True
        else:
            self.fastNotifyBell.config(relief='raised')
            self.fastNotifyIsActive = False

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
                'every {1} seconds.'
                .format(abs(self.cfg.FASTTICK_LB)+1,
                        self.cfg.FASTTICK_RATE))
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
        self.fast_ticker_data = []

        self.fastYBarBuf = tk.Frame(bg=self.cfg.MAIN_BG, width=24)
        self.fastYBarBuf.grid(row=3, column=3, sticky='NS')

        self.fastYScroll = tk.Scrollbar(orient=tk.VERTICAL, command=self.on_vsb)
        self.fastYScroll.grid(row=5, column=3, sticky='NS')

        self.fastListName = tk.Listbox(activestyle='none',
            bg=self.cfg.LIGHT_BG, fg=self.cfg.TEXT_COLOR, selectbackground=self.cfg.LIGHT_BG,
            selectforeground=self.cfg.TEXT_COLOR, relief='sunken',
            highlightcolor=self.cfg.LIGHT_BG, highlightbackground=self.cfg.LIGHT_BG,
            width=40, height=6, yscrollcommand=self.fastYScroll.set)
        self.fastListName.bind('<MouseWheel>', self.on_mouse_wheel)
        self.fastListName.grid(row=5, column=0, sticky='NSWE')

        self.fastListRate = tk.Listbox(activestyle='none',
            bg=self.cfg.LIGHT_BG, fg=self.cfg.TEXT_COLOR, selectbackground=self.cfg.LIGHT_BG,
            selectforeground=self.cfg.TEXT_COLOR, relief='sunken',
            highlightcolor=self.cfg.LIGHT_BG, highlightbackground=self.cfg.LIGHT_BG,
            width=8, height=6, yscrollcommand=self.fastYScroll.set)
        self.fastListRate.bind('<MouseWheel>', self.on_mouse_wheel)
        self.fastListRate.grid(row=5, column=1, sticky='NSWE')

        self.fastListVol = tk.Listbox(activestyle='none',
            bg=self.cfg.LIGHT_BG, fg=self.cfg.TEXT_COLOR, selectbackground=self.cfg.LIGHT_BG,
            selectforeground=self.cfg.TEXT_COLOR, relief='sunken',
            highlightcolor=self.cfg.LIGHT_BG, highlightbackground=self.cfg.LIGHT_BG,
            width=8, height=6, yscrollcommand=self.fastYScroll.set)
        self.fastListVol.bind('<MouseWheel>', self.on_mouse_wheel)
        self.fastListVol.grid(row=5, column=2, sticky='NSWE')

    def on_vsb(self, *args):
        self.fastListName.yview(*args)
        self.fastListRate.yview(*args)
        self.fastListVol.yview(*args)

    def on_mouse_wheel(self, event):
        if event.delta < 0:
            self.fastListName.yview('scroll', 1, 'units')
            self.fastListRate.yview('scroll', 1, 'units')
            self.fastListVol.yview('scroll', 1, 'units')
        if event.delta > 0:
            self.fastListName.yview('scroll', -1, 'units')
            self.fastListRate.yview('scroll', -1, 'units')
            self.fastListVol.yview('scroll', -1, 'units')
        return 'break'

    def create_timer(self):
        self.fastTimerLabel = tk.Label(text='Time until update:',
            bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.fastTimerLabel.grid(row=4, column=4, ipadx=8)

        self.fastTimerFrame2 = tk.LabelFrame(width=120, height=120, bg=self.cfg.MAIN_BG)
        self.fastTimerFrame2.grid(row=5, column=4, columnspan=3)

        self.fastTimerDisp = tk.Label(font=('', 20), bg=self.cfg.MAIN_BG, fg=self.cfg.TEXT_COLOR)
        self.fastTimerDisp.grid(row=5, column=4)

        self.fastTimerValue = self.cfg.FASTTICK_RATE

    def timer_update(self):
        if self.fastTimerValue == 0:
            self.update_fast_ticker_data()
            self.fastTimerValue = self.cfg.FASTTICK_RATE
            if self.fastNotifyIsActive and self.fast_ticker_data:
                playsound('media/notification_sound.mp3')
        values = divmod(self.fastTimerValue, 60)
        minutes = values[0]
        seconds = values[1]
        self.fastTimerDisp.config(text='{}:{:0>2}'.format(minutes, seconds))
        self.fastTimerValue -= 1
        self.app.after(1000, self.timer_update)
        
    def update_fast_ticker_data(self):
         self.fast_ticker_data = fasttick.heartbeat(self.cfg)
         if self.fast_ticker_data:
            for b_name in self.fastButtons:
                if self.fastButtons[b_name][0] == 'desc':
                    self.fast_ticker_data.sort(key=lambda x: x[self.fastButtons[b_name][1]],
                                          reverse=True)
                if self.fastButtons[b_name][0] == 'asc':
                    self.fast_ticker_data.sort(key=lambda x: x[self.fastButtons[b_name][1]])
         self.output_ticker()
        
    def output_ticker(self):
        self.fastListName.delete(0, tk.END)
        self.fastListRate.delete(0, tk.END)
        self.fastListVol.delete(0, tk.END)
        for i in self.fast_ticker_data:
            self.fastListName.insert(tk.END, i[0])
            self.fastListRate.insert(tk.END, '{}{}{}'.format('+', i[1], '%'))
            self.fastListVol.insert(tk.END, i[2])
        self.app.update()
