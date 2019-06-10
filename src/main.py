from PyQt5.QtWidgets import QApplication, QWidget

class Application:
    def __init__(self):
        self.app = QApplication()
        self.app.exec_()

if __name__ == '__main__':
    app = Application()
