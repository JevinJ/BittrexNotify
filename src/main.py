import tkinter as tk
import threading
import slowtick
import fasttick


SLOWTICK_RATE = 600
FASTTICK_RATE = 15

class Application(tk.Frame, threading.Thread):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        threading.Thread.__init__(self)
        self.start()
        self.grid()

        slowtick.delete_pickle()
        fasttick.delete_pickle()

        self.down_arrow = tk.PhotoImage(file='images/arrow1.png')
        self.up_arrow = tk.PhotoImage(file='images/arrow2.png')
        self.no_arrow = tk.PhotoImage(file='images/arrow3.png')
        self.m_ticker_data = []
        self.r_ticker_data = []
        self.slowTimerValue = SLOWTICK_RATE
        self.fastTimerValue = FASTTICK_RATE
        
        self.create_buttons()
        self.create_labels()
        self.create_lists()
        self.create_timers()

        self.slow_timer_update()
        self.fast_timer_update()

        self.mainloop()

    def create_buttons(self):
        # Button dict for sort button logic, key=string name, value[0] is the
        #  button itself, value[1] is the key value used in sorting ticker_data
        self.mSortByName = tk.Button(name='mSortByName', image=self.no_arrow,
            bg='#262626', activebackground='#3D3D3D', relief=tk.RAISED,
            command=lambda: self.on_m_click_sort('mSortByName', self.m_buttons))
        self.mSortByName.grid(row=1, column=0, sticky='NSWE')

        self.mSortByChange = tk.Button(name='mSortByChange', image=self.down_arrow,
            bg='#262626', activebackground='#3D3D3D', relief=tk.RAISED,
            command=lambda: self.on_m_click_sort('mSortByChange', self.m_buttons))
        self.mSortByChange.grid(row=1, column=1, sticky='NSWE')

        self.mSortByVol = tk.Button(name='mSortByVol', image=self.no_arrow,
            bg='#262626', activebackground='#3D3D3D', relief=tk.RAISED,
            command=lambda: self.on_m_click_sort('mSortByVol', self.m_buttons))
        self.mSortByVol.grid(row=1, column=2, sticky='NSWE')

        self.m_buttons = {'mSortByName': [self.mSortByName, 0],
                          'mSortByChange': [self.mSortByChange, 1],
                          'mSortByVol': [self.mSortByVol, 2]}

        self.rSortByName = tk.Button(name='rSortByName', image=self.no_arrow,
            bg='#262626', activebackground='#3D3D3D', relief=tk.RAISED,
            command=lambda: self.on_r_click_sort('rSortByName', self.r_buttons))
        self.rSortByName.grid(row=4, column=0, sticky='NSWE')

        self.rSortByRate = tk.Button(name='rSortByRate', image=self.down_arrow,
            bg='#262626', activebackground='#3D3D3D', relief=tk.RAISED,
            command=lambda: self.on_r_click_sort('rSortByRate', self.r_buttons))
        self.rSortByRate.grid(row=4, column=1, sticky='NSWE')

        self.rSortByVol = tk.Button(name='rSortByVol', image=self.no_arrow,
            bg='#262626', activebackground='#3D3D3D', relief=tk.RAISED,
            command=lambda: self.on_r_click_sort('rSortByVol', self.r_buttons))
        self.rSortByVol.grid(row=4, column=2, sticky='NSWE')

        self.r_buttons = {'rSortByName': [self.rSortByName, 0],
                          'rSortByRate': [self.rSortByRate, 1],
                          'rSortByVol': [self.rSortByVol, 2]}

    def on_m_click_sort(self, name, m_buttons):
        for n in m_buttons:
            if n == name:
                image_name = m_buttons[n][0].cget('image')
                if image_name == 'pyimage1':
                    m_buttons[n][0].config(image=self.up_arrow)
                    self.m_ticker_data = sorted(self.m_ticker_data, key=lambda x: x[m_buttons[n][1]])
                if image_name == 'pyimage2' or image_name == 'pyimage3':
                    m_buttons[n][0].config(image=self.down_arrow)
                    self.m_ticker_data = sorted(self.m_ticker_data, key=lambda x: x[m_buttons[n][1]], reverse=True)
                self.m_list_update()
            else:
                m_buttons[n][0].config(image=self.no_arrow)
        self.update()

    def on_r_click_sort(self, name, r_buttons):
        for n in r_buttons:
            if n == name:
                image_name = r_buttons[n][0].cget('image')
                if image_name == 'pyimage1':
                    r_buttons[n][0].config(image=self.up_arrow)
                    self.r_ticker_data = sorted(self.r_ticker_data, key=lambda x: x[r_buttons[n][1]])
                if image_name == 'pyimage2' or image_name == 'pyimage3':
                    r_buttons[n][0].config(image=self.down_arrow)
                    self.r_ticker_data = sorted(self.r_ticker_data, key=lambda x: x[r_buttons[n][1]], reverse=True)
                self.r_list_update()
            else:
                r_buttons[n][0].config(image=self.no_arrow)
        self.update()

    def create_labels(self):
        self.mLabelName = tk.Label(text='Market Name', bg='#262626', fg='#AFBDCC')
        self.mLabelName.grid(row=0, column=0, sticky='NSWE')

        self.mLabelChange = tk.Label(text='Change', bg='#262626', fg='#AFBDCC')
        self.mLabelChange.grid(row=0, column=1, sticky='NSWE')

        self.mLabelVol = tk.Label(text='Volume', bg='#262626', fg='#AFBDCC')
        self.mLabelVol.grid(row=0, column=2, sticky='NSWE')


        self.rLabelName = tk.Label(text='Market Name', bg='#262626', fg='#AFBDCC')
        self.rLabelName.grid(row=3, column=0, sticky='NSWE')

        self.rLabelChange = tk.Label(text='Rate', bg='#262626', fg='#AFBDCC')
        self.rLabelChange.grid(row=3, column=1, sticky='NSWE')

        self.rLabelVol = tk.Label(text='Volume', bg='#262626', fg='#AFBDCC')
        self.rLabelVol.grid(row=3, column=2, sticky='NSWE')

    def create_lists(self):
        self.mYBarBuf = tk.Frame(bg='#262626', width=18)
        self.mYBarBuf.grid(row=0, rowspan=2, column=4, sticky='NS')

        self.mYScroll = tk.Scrollbar(orient=tk.VERTICAL, command=self.on_vsb)
        self.mYScroll.grid(row=2, column=4, sticky='NS')

        self.mListName = tk.Listbox(activestyle='none',
            bg='#2B2B2B', fg='#AFBDCC', selectbackground='#2B2B2B',
            selectforeground='#AFBDCC', relief=tk.SUNKEN,
            highlightcolor='#2B2B2B', highlightbackground='#2B2B2B',
            width=40, height=8, yscrollcommand=self.mYScroll.set)
        self.mListName.bind('<MouseWheel>', self.on_mouse_wheel)
        self.mListName.grid(row=2, column=0, sticky='NSWE')

        self.mListChange = tk.Listbox(activestyle='none',
            bg='#2B2B2B', fg='#AFBDCC', selectbackground='#2B2B2B',
            selectforeground='#AFBDCC', relief=tk.SUNKEN,
            highlightcolor='#2B2B2B', highlightbackground='#2B2B2B',
            width=8, height=8, yscrollcommand=self.mYScroll.set)
        self.mListChange.bind('<MouseWheel>', self.on_mouse_wheel)
        self.mListChange.grid(row=2, column=1, sticky='NSWE')

        self.mListVol = tk.Listbox(activestyle='none',
            bg='#2B2B2B', fg='#AFBDCC', selectbackground='#2B2B2B',
            selectforeground='#AFBDCC', relief=tk.SUNKEN,
            highlightcolor='#2B2B2B', highlightbackground='#2B2B2B',
            width=8, height=8, yscrollcommand=self.mYScroll.set)
        self.mListVol.bind('<MouseWheel>', self.on_mouse_wheel)
        self.mListVol.grid(row=2, column=2, sticky='NSWE')


        self.rYBarBuf = tk.Frame(bg='#262626', width=18)
        self.rYBarBuf.grid(row=3, rowspan=3, column=4, sticky='NS')

        self.rYScroll = tk.Scrollbar(orient=tk.VERTICAL, command=self.on_vsb)
        self.rYScroll.grid(row=5, column=4, sticky='NS')

        self.rListName = tk.Listbox(activestyle='none',
            bg='#2B2B2B', fg='#AFBDCC', selectbackground='#2B2B2B',
            selectforeground='#AFBDCC', relief=tk.SUNKEN,
            highlightcolor='#2B2B2B', highlightbackground='#2B2B2B',
            width=40, height=8, yscrollcommand=self.rYScroll.set)
        self.rListName.bind('<MouseWheel>', self.on_mouse_wheel)
        self.rListName.grid(row=5, column=0, sticky='NSWE')

        self.rListRate = tk.Listbox(activestyle='none',
            bg='#2B2B2B', fg='#AFBDCC', selectbackground='#2B2B2B',
            selectforeground='#AFBDCC', relief=tk.SUNKEN,
            highlightcolor='#2B2B2B', highlightbackground='#2B2B2B',
            width=8, height=8, yscrollcommand=self.rYScroll.set)
        self.rListRate.bind('<MouseWheel>', self.on_mouse_wheel)
        self.rListRate.grid(row=5, column=1, sticky='NSWE')

        self.rListVol = tk.Listbox(activestyle='none',
            bg='#2B2B2B', fg='#AFBDCC', selectbackground='#2B2B2B',
            selectforeground='#AFBDCC', relief=tk.SUNKEN,
            highlightcolor='#2B2B2B', highlightbackground='#2B2B2B',
            width=8, height=8, yscrollcommand=self.rYScroll.set)
        self.rListVol.bind('<MouseWheel>', self.on_mouse_wheel)
        self.rListVol.grid(row=5, column=2, sticky='NSWE')

    def m_list_update(self):
        self.mListName.delete(0, tk.END)
        self.mListChange.delete(0, tk.END)
        self.mListVol.delete(0, tk.END)
        if self.m_ticker_data:
            for i in self.m_ticker_data:
                self.mListName.insert(tk.END, i[0])
                self.mListChange.insert(tk.END, '{}{}{}'.format('+', i[1], '%'))
                self.mListVol.insert(tk.END, i[2])

    def r_list_update(self):
        self.rListName.delete(0, tk.END)
        self.rListRate.delete(0, tk.END)
        self.rListVol.delete(0, tk.END)
        if self.r_ticker_data:
            for i in self.r_ticker_data:
                self.rListName.insert(tk.END, i[0])
                self.rListRate.insert(tk.END, '{}{}{}'.format('+', i[1], '%'))
                self.rListVol.insert(tk.END, i[2])

    def m_ticker_data_update(self):
        self.m_ticker_data.clear()
        self.m_ticker_data = slowtick.heartbeat()
        self.m_list_update()
        self.update()

    def r_ticker_data_update(self):
        self.r_ticker_data.clear()
        self.r_ticker_data = fasttick.heartbeat()
        self.r_list_update()
        self.update()

    def on_vsb(self, *args):
        self.mListName.yview(*args)
        self.mListChange.yview(*args)
        self.mListVol.yview(*args)

    def on_mouse_wheel(self, event):
        if event.delta < 0:
            self.mListName.yview('scroll', 1, 'units')
            self.mListChange.yview('scroll', 1, 'units')
            self.mListVol.yview('scroll', 1, 'units')
        if event.delta > 0:
            self.mListName.yview('scroll', -1, 'units')
            self.mListChange.yview('scroll', -1, 'units')
            self.mListVol.yview('scroll', -1, 'units')
        return 'break'

    def create_timers(self):
        self.timerFrame1Buf = tk.Frame(width=180, height=220, bg='#262626')
        self.timerFrame1Buf.grid(row=0, rowspan=3, column=5, columnspan=3)

        self.timerFrame1 = tk.LabelFrame(width=180, height=176, bg='#262626')
        self.timerFrame1.grid(row=2, column=5, columnspan=3)

        self.slowTimerDisp = tk.Label(font=('', 20), bg='#262626', fg='#AFBDCC')
        self.slowTimerDisp.grid(row=2, column=6, sticky='WE')

        self.timerFrame2Buf = tk.Frame(width=180, height=220, bg='#262626')
        self.timerFrame2Buf.grid(row=3, rowspan=3, column=5, columnspan=3)

        self.timerFrame2 = tk.LabelFrame(width=180, height=176, bg='#262626')
        self.timerFrame2.grid(row=5, column=5, columnspan=3)

        self.fastTimerDisp = tk.Label(font=('', 20), bg='#262626', fg='#AFBDCC')
        self.fastTimerDisp.grid(row=5, column=6, sticky='WE')

    def slow_timer_update(self):
        if self.slowTimerValue == 0:
            self.m_ticker_data_update()
            self.slowTimerValue = SLOWTICK_RATE
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
            self.r_ticker_data_update()
            self.fastTimerValue = FASTTICK_RATE
        seconds = self.fastTimerValue
        self.fastTimerDisp.config(text=str(seconds))
        self.fastTimerValue -= 1
        self.after(1000, self.fast_timer_update)

app = Application()
app.master.title('BittrexNotify')


