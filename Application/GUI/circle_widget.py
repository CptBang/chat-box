from PySide6 import QtCore
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect


class CircleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.SineCurve)
        self.animation.setLoopCount(-1)  # loop indefinitely
        self.setFixedSize(50, 50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(Qt.red)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect())

    def start_animation(self):
        self.show()
        self.animation.start()

    def stop_animation(self):
        self.animation.stop()
        self.hide()

    @QtCore.Slot()
    def on_animation_value_changed(self, value):
        print("Animation value changed:", value)
