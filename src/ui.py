from PyQt5 import QtWidgets
import pyqtgraph as pg
import sys


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, first, second, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Sig2Dig")
        self.rawGraphWidget = pg.PlotWidget()
        self.cleanedGraphWidget = pg.PlotWidget()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.rawGraphWidget)
        layout.addWidget(self.cleanedGraphWidget)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.rawGraphWidget.plot(first[0], first[1])
        self.cleanedGraphWidget.plot(second[0], second[1])


def showTwoGraphs(first, second):
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(first=first, second=second)
    main.show()
    sys.exit(app.exec_())
