import tkinter as tk
import config
from GUIfasttick import GUIfasttick
from GUIslowtick import GUIslowtick


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        # Images used by GUI
        self.downArrow = tk.PhotoImage(file='media/down_arrow.png')
        self.upArrow = tk.PhotoImage(file='media/up_arrow.png')
        self.noArrow = tk.PhotoImage(file='media/no_arrow.png')
        self.notifyBell = tk.PhotoImage(file='media/notification_bell.png')
        self.questionMark = tk.PhotoImage(file='media/question_mark.png')

        self.slowMarket = GUIslowtick(self)
        self.fastMarket = GUIfasttick(self)

        self.mainloop()

if __name__ == '__main__':
    app = Application()
    app.master.title('BittrexNotify')
