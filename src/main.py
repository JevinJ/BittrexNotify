from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QComboBox

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Coin Monitor')
        self.setGeometry(300, 300, 350, 200)
        self.setup_menu_bar()
        self.setup_tool_bar()
        self.show()

    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_action)

    def setup_tool_bar(self):
        tool_bar = self.addToolBar('ToolBar')

        website_select_box = QComboBox()
        website_select_box.addItems(['Bittrex', 'Binance'])
        website_select_label = QLabel("Website:")
        website_select_label.setBuddy(website_select_box)

        tool_bar.addWidget(website_select_label)
        tool_bar.addWidget(website_select_box)


if __name__ == '__main__':
    import sys
    self = QApplication(sys.argv)
    app = Application()
    sys.exit(self.exec_())
