from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QComboBox, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        menu_bar = self.menuBar()
        status_bar = self.statusBar()

        self.setWindowTitle('Coin Monitor')
        self.setGeometry(300, 300, 350, 200)

        exit_action = QAction(QIcon('exit24.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_action)

        website_select_box = QComboBox()
        website_select_box.addItems(['Bittrex', 'Binance'])
        website_select_label = QLabel("Website:")
        website_select_label.setBuddy(website_select_box)
        status_bar.addWidget(website_select_label)
        status_bar.addWidget(website_select_box, stretch=1)

        top_layout = QHBoxLayout()
        top_layout.addWidget(website_select_label)
        top_layout.addWidget(website_select_box)
        top_layout.addStretch(1)

        self.show()


if __name__ == '__main__':
    import sys
    self = QApplication(sys.argv)
    app = Application()
    sys.exit(self.exec_())
