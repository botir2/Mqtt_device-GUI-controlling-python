from itertools import cycle
from PyQt5 import QtCore, QtGui, QtWidgets

class TrafficLight(QtWidgets.QMainWindow):
    def __init__(self,parent = None):
        super(TrafficLight, self).__init__(parent)
        self.setWindowTitle("TrafficLight ")
        self.traffic_light_colors = cycle([
            QtGui.QColor('red'),
            QtGui.QColor('yellow'),
            QtGui.QColor('green')
        ])
        self._current_color = next(self.traffic_light_colors)
        timer = QtCore.QTimer(
            self,
            interval=2000,
            timeout=self.change_color
        )
        timer.start()
        self.resize(200, 400)

    @QtCore.pyqtSlot()
    def change_color(self):
        self._current_color = next(self.traffic_light_colors)
        self.update()

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setBrush(self._current_color)
        p.setPen(QtCore.Qt.black)
        p.drawEllipse(self.rect().center(), 50, 50)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = TrafficLight()
    w.show()
    sys.exit(app.exec_())