import tkinter as tk
import config
import GUIfastmarket
import GUIslowmarket


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        self.cfg = config.Config()
        self.slowMarket = GUIslowmarket.SlowMarket(self, self.cfg)
        self.fastMarket = GUIfastmarket.FastMarket(self, self.cfg)

        self.mainloop()


app = Application()
app.master.title('BittrexNotify')
