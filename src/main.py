from playsound import playsound
import tkinter as tk
import threading
import fasttick
import slowtick


SLOWTICK_RATE = 600
FASTTICK_RATE = 15

# Color constants for GUI
CLICKED_BG = '#3D3D3D'
MAIN_BG = '#262626'
LIGHT_BG = '#2B2B2B'
TEXT_COLOR = '#AFBDCC'


'''
Interface for both slow check and fast checking of price on bittrex.
Variables starting with m(% change) refer to upper section of gui.
    mList is calculated every (SLOWTICK_RATE, in seconds) over
    2 pickle data files in the past.
Variables starting with r(% avg rate) refer to lower section of gui.
    rList is calculated every (FASTTICK_RATE, in seconds) over
    10 pickle data files in the past
'''
class Application(tk.Frame, threading.Thread):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        #threading.Thread.__init__(self)
        #self.start()
        self.grid()

        slowtick.delete_ancient_pickles()
        fasttick.delete_ancient_pickles()

        self.load_media()
        self.m_ticker_data = []
        self.r_ticker_data = []
        self.slowTimerValue = SLOWTICK_RATE
        self.fastTimerValue = FASTTICK_RATE

        self.create_labels()
        self.create_buttons()
        self.mNotifyIsActive = False
        self.rNotifyIsActive = False
        self.create_lists()
        self.create_timers()

        self.slow_timer_update()
        self.fast_timer_update()

        self.mainloop()

    # Loading images and sound for GUI.
    def load_media(self):
        self.downArrow = tk.PhotoImage(file='media/down_arrow.png')
        self.upArrow = tk.PhotoImage(file='media/up_arrow.png')
        self.noArrow = tk.PhotoImage(file='media/no_arrow.png')
        self.notifyBell = tk.PhotoImage(file='media/notification_bell.png')
        self.questionMark = tk.PhotoImage(file='media/question_mark.png')

    def create_labels(self):
        self.mLabelName = tk.Label(text='Market Name', bg=MAIN_BG, fg=TEXT_COLOR)
        self.mLabelName.grid(row=0, column=0, sticky='NSWE')

        self.mLabelChange = tk.Label(text='Change', bg=MAIN_BG, fg=TEXT_COLOR)
        self.mLabelChange.grid(row=0, column=1, sticky='NSWE')

        self.mLabelVol = tk.Label(text='Volume', bg=MAIN_BG, fg=TEXT_COLOR)
        self.mLabelVol.grid(row=0, column=2, sticky='NSWE')

        self.mLabelBuf = tk.Frame(width=120, height=42, bg=MAIN_BG)
        self.mLabelBuf.grid(row=0, rowspan=2, column=4, columnspan=3)


        self.rLabelName = tk.Label(text='Market Name', bg=MAIN_BG, fg=TEXT_COLOR)
        self.rLabelName.grid(row=3, column=0, sticky='NSWE')

        self.rLabelChange = tk.Label(text='Rate', bg=MAIN_BG, fg=TEXT_COLOR)
        self.rLabelChange.grid(row=3, column=1, sticky='NSWE')

        self.rLabelVol = tk.Label(text='Volume', bg=MAIN_BG, fg=TEXT_COLOR)
        self.rLabelVol.grid(row=3, column=2, sticky='NSWE')

        self.rLabelBuf = tk.Frame(width=120, height=42, bg=MAIN_BG)
        self.rLabelBuf.grid(row=3, rowspan=2, column=4)

    '''
    Creates all the buttons in the GUI.
    m_buttons and r_buttons are used to store: 
        A reference to the button itself,
        The direction of the current sort for the button
        A key for the button clicked to sort the listbox data
    '''
    def create_buttons(self):
        self.mSortByName = tk.Button(name='mSortByName', image=self.noArrow,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='raised',
            command=lambda: on_click_sort('mSortByName', self.m_buttons, 'm'))
        self.mSortByName.grid(row=1, column=0, sticky='NSWE')

        self.mSortByChange = tk.Button(name='mSortByChange', image=self.downArrow,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='raised',
            command=lambda: on_click_sort('mSortByChange', self.m_buttons, 'm'))
        self.mSortByChange.grid(row=1, column=1, sticky='NSWE')

        self.mSortByVol = tk.Button(name='mSortByVol', image=self.noArrow,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='raised',
            command=lambda: on_click_sort('mSortByVol', self.m_buttons, 'm'))
        self.mSortByVol.grid(row=1, column=2, sticky='NSWE')

        self.m_buttons = {self.mSortByName: ['none', 0],
                          self.mSortByChange: ['desc', 1],
                          self.mSortByVol: ['none', 2]}

        self.mNotifyBell = tk.Button(name='mNotifyBell', image=self.notifyBell,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='raised',
            command=lambda: on_click_notif('m'))
        self.mNotifyBell.grid(row=1, column=3, sticky='NSWE')

        self.mHelp = tk.Button(name='mHelp', image=self.questionMark,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='flat',
            command=lambda: on_click_help('m'))
        self.mHelp.grid(row=0, column=4, sticky='E')


        self.rSortByName = tk.Button(name='rSortByName', image=self.noArrow,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='raised',
            command=lambda: on_click_sort('rSortByName', self.r_buttons, 'r'))
        self.rSortByName.grid(row=4, column=0, sticky='NSWE')

        self.rSortByRate = tk.Button(name='rSortByRate', image=self.downArrow,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='raised',
            command=lambda: on_click_sort('rSortByRate', self.r_buttons, 'r'))
        self.rSortByRate.grid(row=4, column=1, sticky='NSWE')

        self.rSortByVol = tk.Button(name='rSortByVol', image=self.noArrow,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='raised',
            command=lambda: on_click_sort('rSortByVol', self.r_buttons, 'r'))
        self.rSortByVol.grid(row=4, column=2, sticky='NSWE')

        self.r_buttons = {self.rSortByName: ['none', 0],
                          self.rSortByRate: ['desc', 1],
                          self.rSortByVol: ['none', 2]}

        self.rNotifyBell = tk.Button(name='rNotifyBell', image=self.notifyBell,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='raised',
            command=lambda: on_click_notif('r'))
        self.rNotifyBell.grid(row=4, column=3, sticky='NSWE')

        self.rHelp = tk.Button(name='rHelp', image=self.questionMark,
            bg=MAIN_BG, activebackground=CLICKED_BG, relief='flat',
            command=lambda: on_click_help('r'))
        self.rHelp.grid(row=3, column=4, sticky='E')

        # This takes the button dict and resets/changes button images
        #   and sorts the listbox data accordingly.
        def on_click_sort(pressed_name, buttons, caller):
            for b_name in buttons:
                if str(b_name) == ('.' + pressed_name):
                    sort_direction = buttons[b_name][0]
                    if sort_direction == 'desc':
                        buttons[b_name][0] = 'asc'
                        b_name.config(image=self.upArrow)
                        if caller == 'm':
                            self.m_ticker_data.sort(key=lambda x: x[buttons[b_name][1]])
                        if caller == 'r':
                            self.r_ticker_data.sort(key=lambda x: x[buttons[b_name][1]])
                    if sort_direction == 'asc' or sort_direction == 'none':
                        buttons[b_name][0] = 'desc'
                        b_name.config(image=self.downArrow)
                        if caller == 'm':
                            self.m_ticker_data.sort(key=lambda x: x[buttons[b_name][1]],
                                                    reverse=True)
                        if caller == 'r':
                            self.r_ticker_data.sort(key=lambda x: x[buttons[b_name][1]],
                                                    reverse=True)
                else:
                    buttons[b_name][0] = 'none'
                    b_name.config(image=self.noArrow)
            self.output_ticker(caller)
            self.update()

        # Switches notification button relief and turns on
        # notification sound.
        def on_click_notif(caller):
            if caller == 'm':
                if self.mNotifyBell.cget('relief') == 'raised':
                    self.mNotifyBell.config(relief='sunken')
                    self.mNotifyIsActive = True
                else:
                    self.mNotifyBell.config(relief='raised')
                    self.mNotifyIsActive = False
            if caller == 'r':
                if self.rNotifyBell.cget('relief') == 'raised':
                    self.rNotifyBell.config(relief='sunken')
                    self.mNotifyIsActive = True
                else:
                    self.rNotifyBell.config(relief='raised')
                    self.mNotifyIsActive = False

        def on_click_help(caller):
            helpWindow = tk.Toplevel()
            helpWindow.title('Help')

            frameBuf = tk.Frame(helpWindow,
                width=203, height=185, bg=MAIN_BG)
            frameBuf.grid(row=0, rowspan=4, column=0, columnspan=3)

            if caller == 'm':
                msg1 = tk.Message(helpWindow,
                    bg=MAIN_BG, fg=TEXT_COLOR, width=192,
                    text='This section shows % change over ' +
                    str(abs(slowtick.LOOKBACK)+1) +
                    ' measurements. Recorded once every ' +
                    str(SLOWTICK_RATE/60) +
                    ' minutes.')
                msg1.grid(row=0, columnspan=3)
            if caller == 'r':
                msg1 = tk.Message(helpWindow, aspect=300,
                    bg=MAIN_BG, fg=TEXT_COLOR, width=192,
                    text='This section shows % rate increase over ' +
                    str(abs(fasttick.LOOKBACK) + 1) +
                    ' measurements. Recorded once every ' +
                    str(FASTTICK_RATE) +
                    ' seconds.')
                msg1.grid(row=0, columnspan=3)

            msg2 = tk.Message(helpWindow,
                bg=MAIN_BG, fg=TEXT_COLOR, width=200,
                text='The arrow buttons can be used to ' +
                'sort data according to the ' +
                'label it is under.')
            msg2.grid(row=1, columnspan=3)

            msg3 = tk.Message(helpWindow,
                bg=MAIN_BG, fg=TEXT_COLOR, width=200,
                text='The bell button can be toggled ' +
                'on and off to play a notification ' +
                'when the ticker has been updated.')
            msg3.grid(row=2, columnspan=3)

            dismissButton = tk.Button(helpWindow, text='Dismiss',
                command=helpWindow.destroy)
            dismissButton.grid(row=3, column=1, sticky='WE')

    def create_lists(self):
        self.mYBarBuf = tk.Frame(bg=MAIN_BG, width=24)
        self.mYBarBuf.grid(row=0, column=3, sticky='NS')

        self.mYScroll = tk.Scrollbar(orient=tk.VERTICAL, command=self.on_m_vsb)
        self.mYScroll.grid(row=2, column=3, sticky='NS')

        self.mListName = tk.Listbox(activestyle='none',
            bg=LIGHT_BG, fg=TEXT_COLOR, selectbackground=LIGHT_BG,
            selectforeground=TEXT_COLOR, relief='sunken',
            highlightcolor=LIGHT_BG, highlightbackground=LIGHT_BG,
            width=40, height=6, yscrollcommand=self.mYScroll.set)
        self.mListName.bind('<MouseWheel>', self.on_m_mouse_wheel)
        self.mListName.grid(row=2, column=0, sticky='NSWE')

        self.mListChange = tk.Listbox(activestyle='none',
            bg=LIGHT_BG, fg=TEXT_COLOR, selectbackground=LIGHT_BG,
            selectforeground=TEXT_COLOR, relief='sunken',
            highlightcolor=LIGHT_BG, highlightbackground=LIGHT_BG,
            width=8, height=6, yscrollcommand=self.mYScroll.set)
        self.mListChange.bind('<MouseWheel>', self.on_m_mouse_wheel)
        self.mListChange.grid(row=2, column=1, sticky='NSWE')

        self.mListVol = tk.Listbox(activestyle='none',
            bg=LIGHT_BG, fg=TEXT_COLOR, selectbackground=LIGHT_BG,
            selectforeground=TEXT_COLOR, relief='sunken',
            highlightcolor=LIGHT_BG, highlightbackground=LIGHT_BG,
            width=8, height=6, yscrollcommand=self.mYScroll.set)
        self.mListVol.bind('<MouseWheel>', self.on_m_mouse_wheel)
        self.mListVol.grid(row=2, column=2, sticky='NSWE')


        self.rYBarBuf = tk.Frame(bg=MAIN_BG, width=24)
        self.rYBarBuf.grid(row=3, column=3, sticky='NS')

        self.rYScroll = tk.Scrollbar(orient=tk.VERTICAL, command=self.on_r_vsb)
        self.rYScroll.grid(row=5, column=3, sticky='NS')

        self.rListName = tk.Listbox(activestyle='none',
            bg=LIGHT_BG, fg=TEXT_COLOR, selectbackground=LIGHT_BG,
            selectforeground=TEXT_COLOR, relief='sunken',
            highlightcolor=LIGHT_BG, highlightbackground=LIGHT_BG,
            width=40, height=6, yscrollcommand=self.rYScroll.set)
        self.rListName.bind('<MouseWheel>', self.on_r_mouse_wheel)
        self.rListName.grid(row=5, column=0, sticky='NSWE')

        self.rListRate = tk.Listbox(activestyle='none',
            bg=LIGHT_BG, fg=TEXT_COLOR, selectbackground=LIGHT_BG,
            selectforeground=TEXT_COLOR, relief='sunken',
            highlightcolor=LIGHT_BG, highlightbackground=LIGHT_BG,
            width=8, height=6, yscrollcommand=self.rYScroll.set)
        self.rListRate.bind('<MouseWheel>', self.on_r_mouse_wheel)
        self.rListRate.grid(row=5, column=1, sticky='NSWE')

        self.rListVol = tk.Listbox(activestyle='none',
            bg=LIGHT_BG, fg=TEXT_COLOR, selectbackground=LIGHT_BG,
            selectforeground=TEXT_COLOR, relief='sunken',
            highlightcolor=LIGHT_BG, highlightbackground=LIGHT_BG,
            width=8, height=6, yscrollcommand=self.rYScroll.set)
        self.rListVol.bind('<MouseWheel>', self.on_r_mouse_wheel)
        self.rListVol.grid(row=5, column=2, sticky='NSWE')

    def on_m_vsb(self, *args):
        self.mListName.yview(*args)
        self.mListChange.yview(*args)
        self.mListVol.yview(*args)

    def on_r_vsb(self, *args):
        self.rListName.yview(*args)
        self.rListRate.yview(*args)
        self.rListVol.yview(*args)

    def on_m_mouse_wheel(self, event):
        if event.delta < 0:
            self.mListName.yview('scroll', 1, 'units')
            self.mListChange.yview('scroll', 1, 'units')
            self.mListVol.yview('scroll', 1, 'units')
        if event.delta > 0:
            self.mListName.yview('scroll', -1, 'units')
            self.mListChange.yview('scroll', -1, 'units')
            self.mListVol.yview('scroll', -1, 'units')
        return 'break'

    def on_r_mouse_wheel(self, event):
        if event.delta < 0:
            self.rListName.yview('scroll', 1, 'units')
            self.rListRate.yview('scroll', 1, 'units')
            self.rListVol.yview('scroll', 1, 'units')
        if event.delta > 0:
            self.rListName.yview('scroll', -1, 'units')
            self.rListRate.yview('scroll', -1, 'units')
            self.rListVol.yview('scroll', -1, 'units')
        return 'break'

    def output_ticker(self, caller):
        if caller == 'm':
            self.mListName.delete(0, tk.END)
            self.mListChange.delete(0, tk.END)
            self.mListVol.delete(0, tk.END)
            for i in self.m_ticker_data:
                self.mListName.insert(tk.END, i[0])
                self.mListChange.insert(tk.END, '{}{}{}'.format('+', i[1], '%'))
                self.mListVol.insert(tk.END, i[2])
        if caller == 'r':
            self.rListName.delete(0, tk.END)
            self.rListRate.delete(0, tk.END)
            self.rListVol.delete(0, tk.END)
            for i in self.r_ticker_data:
                self.rListName.insert(tk.END, i[0])
                self.rListRate.insert(tk.END, '{}{}{}'.format('+', i[1], '%'))
                self.rListVol.insert(tk.END, i[2])
        self.update()

    def update_ticker_data(self, caller):
        if caller == 'm':
            self.m_ticker_data = slowtick.heartbeat()
            if self.m_ticker_data:
                for b_name in self.m_buttons:
                    if self.m_buttons[b_name][0] == 'desc':
                        self.m_ticker_data.sort(key=lambda x: x[self.m_buttons[name][1]],
                                                reverse=True)
                    if self.m_buttons[b_name][0] == 'asc':
                        self.m_ticker_data.sort(key=lambda x: x[self.m_buttons[name][1]])
            self.output_ticker('m')
        if caller == 'r':
            self.r_ticker_data = fasttick.heartbeat()
            if self.r_ticker_data:
                for b_name in self.r_buttons:
                    if self.r_buttons[b_name][0] == 'desc':
                        self.r_ticker_data.sort(key=lambda x: x[self.r_buttons[b_name][1]],
                                                reverse=True)
                    if self.r_buttons[b_name][0] == 'asc':
                        self.r_ticker_data.sort(key=lambda x: x[self.r_buttons[b_name][1]])
            self.output_ticker('r')

    def create_timers(self):
        self.slowTimerLabel = tk.Label(text='Time until update:',
            bg=MAIN_BG, fg=TEXT_COLOR)
        self.slowTimerLabel.grid(row=1, column=4, ipadx=8)

        self.timerFrame1 = tk.LabelFrame(width=120, height=120, bg=MAIN_BG)
        self.timerFrame1.grid(row=2, column=4, columnspan=3)

        self.slowTimerDisp = tk.Label(font=('', 20), bg=MAIN_BG, fg=TEXT_COLOR)
        self.slowTimerDisp.grid(row=2, column=4)


        self.fastTimerLabel = tk.Label(text='Time until update:',
            bg=MAIN_BG, fg=TEXT_COLOR)
        self.fastTimerLabel.grid(row=4, column=4, ipadx=8)

        self.timerFrame2 = tk.LabelFrame(width=120, height=120, bg=MAIN_BG)
        self.timerFrame2.grid(row=5, column=4, columnspan=3)

        self.fastTimerDisp = tk.Label(font=('', 20), bg=MAIN_BG, fg=TEXT_COLOR)
        self.fastTimerDisp.grid(row=5, column=4)

    def slow_timer_update(self):
        if self.slowTimerValue == 0:
            self.update_ticker_data('m')
            self.slowTimerValue = SLOWTICK_RATE
            if self.mNotifyIsActive and self.m_ticker_data:
                playsound('media/notification_sound.mp3')
        values = divmod(self.slowTimerValue, 60)
        minutes = values[0]
        seconds = values[1]
        if minutes < 10:
            minutes = '0' + str(minutes)
        if seconds < 10:
            seconds = '0' + str(seconds)
        self.slowTimerDisp.config(text=str(minutes) + ':' + str(seconds))
        self.slowTimerValue -= 1
        self.after(1000, self.slow_timer_update)

    def fast_timer_update(self):
        if self.fastTimerValue == 0:
            self.update_ticker_data('r')
            self.fastTimerValue = FASTTICK_RATE
            if self.rNotifyIsActive and self.r_ticker_data:
                playsound('media/notification_sound.mp3')
        seconds = self.fastTimerValue
        self.fastTimerDisp.config(text=str(seconds))
        self.fastTimerValue -= 1
        self.after(1000, self.fast_timer_update)

app = Application()
app.master.title('BittrexNotify')


