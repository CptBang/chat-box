from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QPushButton


class RecordingButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.original_text = text
        self.animations = []
        colors = ["#590D22", "#800F2F", "#A4133C", "#C9184A", "#FF4D6D",
                  "#FF758F", "#FF8FA3", "#FFB3C1", "#FFCCD5", "#FFF0F3"]

        for start_color, end_color in zip(colors[:-1], colors[1:]):
            animation = QPropertyAnimation(self, b"stylesheet")
            animation.setDuration(100)
            animation.setStartValue(f"background-color: {start_color};")
            animation.setEndValue(f"background-color: {end_color};")
            self.animations.append(animation)

        # Chain the animations together so they play in sequence
        for i in range(len(self.animations) - 1):
            self.animations[i].finished.connect(self.animations[i + 1].start)

    def start_animation(self):
        self.setDisabled(True)
        self.setText("Recording")
        # self.animations[0].start()

    def stop_animation(self):
        # Stop all animations
        # for animation in self.animations:
        #     animation.stop()
        self.setDisabled(False)
        self.setText(self.original_text)

