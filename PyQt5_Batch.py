import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # Define Quit Button
        exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        # Define File Selection Panel
        FileSelection = QLabel('File Selection')
        grid.addWidget(FileSelection, 0, 0)
        LabelNames = ['Set Path to Raw Data Files', 'Set Path to Additional Files', 'Set Directory for Raw STORM',
        'Create New Directory for Bin Files ']
        LabelPositions = [(i, j) for i in range(1,5) for j in range(1)]
        for LPosition, LName in zip(LabelPositions, LabelNames):
            label = QLabel(LName)
            grid.addWidget(label, *LPosition)
    
        processes = QLabel('How Many .DAX Movies to Analyze at Once?', self)
        grid.addWidget(processes, 5, 0)
        promptChannels = QLabel('Which Color Channels Are You Analyzing?', self)
        grid.addWidget(promptChannels, 0, 2)

        # Define File Selection buttons
        Btn1 = QPushButton('Select File', self)
        Btn1.clicked.connect(self.showFileDialog)
        grid.addWidget(Btn1, 1, 1)
        Btn2 = QPushButton('Select File', self)
        Btn2.clicked.connect(self.showFileDialog)
        grid.addWidget(Btn2, 2, 1)
        Btn3 = QPushButton('Select File', self)
        Btn3.clicked.connect(self.showFileDialog)
        grid.addWidget(Btn3, 3, 1)
        Btn4 = QPushButton('Select File', self)
        Btn4.clicked.connect(self.showFileDialog)
        grid.addWidget(Btn4, 4, 1)

        # Define user entry
        self.le = QLineEdit(self)
        grid.addWidget(self.le, 5, 1)

        #Define channel selection
        channels = ["750", "647", "561", "488", "IRbead", "Visbead"]
        positions = [(i, j) for i in range(1, 7) for j in range(2, 3)]

        for position, name in zip(positions, channels):
            channelbox = QCheckBox(name)
            grid.addWidget(channelbox, *position)

        #self.statusBar()

        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('&File')
        #fileMenu.addAction(exitAct)

        #toolbar = self.addToolBar('Exit')
        #toolbar.addAction(exitAct)

        #self.setGeometry(200, 200, 350, 350)
        self.setWindowTitle('Batch Storm Analysis')
        self.show()

    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', ' /home')

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',  'Enter your name:')

        if ok:
            self.le.setText(str(text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())