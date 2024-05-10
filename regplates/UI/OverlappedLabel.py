from PyQt5 import QtWidgets


class OverlappedLabel(QtWidgets.QLabel):
    def setRelatedLabel(self, label: QtWidgets.QLabel):
        self.relatedLabel = label
        self.setGeometry(self.relatedLabel.geometry())

    def resizeEvent(self, event):
        rect = self.geometry()
        rect.setWidth(rect.width() + 50)
        self.relatedLabel.setGeometry(rect)
        QtWidgets.QLabel.resizeEvent(self, event)
