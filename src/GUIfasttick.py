import tkinter as tk
from time import sleep
from playsound import playsound
import config
import fasttick
from helpmessage import fasttick_help_message
import misc
from tickerwindow import TickerWindow


class GUIfasttick(TickerWindow):
    def __init__(self, app):
        super().__init__(app)
        misc.delete_ancient_pickles('fasttick_history')

        self.draw_labels()
        self.draw_buttons()
        self.draw_lists()
        self.draw_timer()
        self.timer_update()

    def draw_labels(self):
        self.labelName.grid(row=3, column=0, sticky='NSWE')

        self.labelChange.config(text='Rate')
        self.labelChange.grid(row=3, column=1, sticky='NSWE')

        self.labelVol.grid(row=3, column=2, sticky='NSWE')
        self.labelBuf.grid(row=3, rowspan=2, column=3, columnspan=2, sticky='NSWE')

    def draw_buttons(self):
        self.sortByName.grid(row=4, column=0, sticky='NSWE')
        self.sortByChange.grid(row=4, column=1, sticky='NSWE')
        self.sortByVol.grid(row=4, column=2, sticky='NSWE')
        self.notifyBell.grid(row=4, column=3, sticky='NSWE')
        self.help.grid(row=3, column=4, sticky='E')

    def on_click_help(self):
        helpWindow = tk.Toplevel()
        helpWindow.title('Help')

        frameBuf = tk.Frame(helpWindow, width=192, bg=config.MAIN_BG)
        frameBuf.grid(row=0, rowspan=4, column=0, columnspan=3)

        message = tk.Message(frameBuf, bg=config.MAIN_BG, fg=config.TEXT_COLOR,
                             width=192, text=fasttick_help_message)
        message.grid(row=0, columnspan=3)

        dismissButton = tk.Button(frameBuf, text='Dismiss', command=helpWindow.destroy)
        dismissButton.grid(row=1, column=1)

    def draw_lists(self):
        self.yScroll.grid(row=5, column=3, sticky='NSWE')
        self.listName.grid(row=5, column=0, sticky='NSWE')
        self.listChange.grid(row=5, column=1, sticky='NSWE')
        self.listVol.grid(row=5, column=2, sticky='NSWE')

    def draw_timer(self):
        self.timerLabel.grid(row=5, column=4, ipadx=8)
        self.timerFrame.grid(row=5, column=4, columnspan=3)
        self.timerDisp.grid(row=5, column=4)
        self.timerValue = config.FASTTICK_RATE

    def timer_update(self):
        if self.timerValue == 3:
            self.async = self.pool.apply_async(fasttick.heartbeat)
        if self.timerValue == 0:
            while True:
                if self.async.ready():
                    break
                for i in range(1, 4):
                    if self.async.ready():
                        break
                    self.timerDisp.config(text=f'{"." * i}', font=('', 20))
                    self.app.update()
                    sleep(1)
            self.ticker_data = self.async.get()
            self.sort_ticker()
            if self.notifyIsActive and self.ticker_data:
                playsound('media/notification_sound.mp3')
            self.timerValue = config.FASTTICK_RATE
        values = divmod(self.timerValue, 60)
        minutes = values[0]
        seconds = values[1]
        self.timerDisp.config(text=f'{minutes}:{seconds:0>2}', font=('', 20))
        self.timerValue -= 1
        self.app.after(1000, self.timer_update)