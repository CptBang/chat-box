from PySide6.QtCore import QThread, Signal
from elevenlabs import generate, play, User


class AudioplayerThread(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, text, profile, parent=None):
        super().__init__(parent)
        self.text = text
        self.profile = profile

    def run(self):
        user = User.from_api()
        characters_left = user.subscription.character_limit - user.subscription.character_count
        if len(self.text) > characters_left:
            self.error.emit(f"Only {characters_left} characters left for elevenlabs!")
            self.finished.emit(self.text)  # emit the signal when the thread is finished
            return
        try:
            audio = generate(
                text=self.text,
                voice=self.profile["voice"],
                model=self.profile["model"]
            )
            play(audio)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit(self.text)  # emit the signal when the thread is finished
