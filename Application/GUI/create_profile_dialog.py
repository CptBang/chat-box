from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QApplication, QComboBox, QTextEdit

import Application.constants


class CreateProfileDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.instance_name_label = QLabel("Instance Name:")
        self.instance_name_input = QLineEdit()
        self.instance_name_input.setPlaceholderText("Enter name of the instance here...")

        self.character_name_label = QLabel("Character Name:")
        self.character_name_input = QLineEdit()
        self.character_name_input.setPlaceholderText("Enter name here...")

        # Add a combobox for selecting a microphone
        self.voice_option_combobox = QComboBox(self)
        self.voice_option_combobox.addItems(Application.constants.ELEVEN_LABS_VOICES)

        self.appearance_label = QLabel("Appearance:")
        self.appearance_input = QTextEdit()
        self.appearance_input.setPlaceholderText("Enter appearance here...")

        self.personality_label = QLabel("Personality:")
        self.personality_input = QTextEdit()
        self.personality_input.setPlaceholderText("Enter personality here...")

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)  # QDialog will close and return 1 (Accept)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)  # QDialog will close and return 0 (Reject)

        self.layout.addWidget(self.instance_name_label)
        self.layout.addWidget(self.instance_name_input)
        self.layout.addWidget(self.character_name_label)
        self.layout.addWidget(self.character_name_input)
        self.layout.addWidget(self.voice_option_combobox)
        self.layout.addWidget(self.personality_label)
        self.layout.addWidget(self.personality_input)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)
