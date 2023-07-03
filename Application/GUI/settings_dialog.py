from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QSlider, QTabWidget, QStyle
from functools import partial

class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_api_keys_settings_widget()
        self.create_microphone_settings_widget()

        # Tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.volume_mic_settings_widget, "Volume/Mic")
        self.tab_widget.addTab(self.api_keys_widget, "API Keys")
        # self.tab_widget.setTabPosition(QTabWidget.West)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.save_button)

        # Load the settings
        self.load_settings()

    def create_api_keys_settings_widget(self):
        openai_api_key_label = QLabel("OpenAI API Key:")
        self.openai_api_key_line = QLineEdit(self)
        self.openai_api_key_line.setEchoMode(QLineEdit.Password)  # mask the text
        toggle_view_action = self.create_toggle_view_action(self.openai_api_key_line)
        self.openai_api_key_line.addAction(toggle_view_action, QLineEdit.TrailingPosition)

        elevenlabs_api_key_label = QLabel("ElevenLabs API Key:")
        self.elevenlabs_api_key_line = QLineEdit(self)
        self.elevenlabs_api_key_line.setEchoMode(QLineEdit.Password)  # mask the text
        toggle_view_action = self.create_toggle_view_action(self.elevenlabs_api_key_line)
        self.elevenlabs_api_key_line.addAction(toggle_view_action, QLineEdit.TrailingPosition)

        api_keys_layout = QVBoxLayout(self)
        api_keys_layout.addWidget(openai_api_key_label)
        api_keys_layout.addWidget(self.openai_api_key_line)
        api_keys_layout.addWidget(elevenlabs_api_key_label)
        api_keys_layout.addWidget(self.elevenlabs_api_key_line)

        self.api_keys_widget = QWidget()
        self.api_keys_widget.setLayout(api_keys_layout)

    def create_toggle_view_action(self, line_edit):
        action = QAction(self)
        action.triggered.connect(partial(self.toggle_view, line_edit, action))
        action.setIcon(self.style().standardIcon(QStyle.SP_DialogYesButton))  # 'eye' icon

        return action

    def toggle_view(self, line_edit, action):
        if line_edit.echoMode() == QLineEdit.Password:
            line_edit.setEchoMode(QLineEdit.Normal)
            action.setIcon(self.style().standardIcon(QStyle.SP_DialogNoButton))  # 'crossed eye' icon
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            action.setIcon(self.style().standardIcon(QStyle.SP_DialogYesButton))  # 'eye' icon

    def create_microphone_settings_widget(self):
        # Volume/mic settings tab
        self.mic_sensitivity_label = QLabel("Microphone Sensitivity:")
        self.mic_sensitivity_slider = QSlider(Qt.Horizontal)
        self.mic_sensitivity_slider.setMinimum(0)
        self.mic_sensitivity_slider.setMaximum(100)

        self.volume_label = QLabel("Volume:")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)

        self.mute_button = QPushButton("Mute")
        self.mute_button.setCheckable(True)
        self.mute_button.toggled.connect(self.toggle_mute)

        volume_mic_settings_layout = QVBoxLayout()
        volume_mic_settings_layout.addWidget(self.mic_sensitivity_label)
        volume_mic_settings_layout.addWidget(self.mic_sensitivity_slider)
        volume_mic_settings_layout.addWidget(self.volume_label)
        volume_mic_settings_layout.addWidget(self.volume_slider)
        volume_mic_settings_layout.addWidget(self.mute_button)

        self.volume_mic_settings_widget = QWidget()
        self.volume_mic_settings_widget.setLayout(volume_mic_settings_layout)

    def toggle_mute(self, checked):
        if checked:
            self.mute_button.setText("Unmute")
        else:
            self.mute_button.setText("Mute")
        self.parent.tts_muted = checked


    def save_settings(self):
        self.parent.settings.setValue('openai_api_key', self.openai_api_key_line.text())
        self.parent.settings.setValue('elevenlabs_api_key', self.elevenlabs_api_key_line.text())
        self.parent.settings.setValue('mic_sensitivity', self.mic_sensitivity_slider.value())
        self.parent.settings.setValue('volume', self.volume_slider.value())
        self.parent.settings.setValue('mute_tts', self.mute_button.isChecked())
        self.parent.settings.sync()
        self.close()

    def load_settings(self):
        self.openai_api_key_line.setText(self.parent.settings.value('openai_api_key', ''))
        self.elevenlabs_api_key_line.setText(self.parent.settings.value('elevenlabs_api_key', ''))
        mic_sensitivity = self.parent.settings.value('mic_sensitivity')
        self.mic_sensitivity_slider.setValue(int(mic_sensitivity) if mic_sensitivity else 0)
        volume = self.parent.settings.value('volume')
        self.volume_slider.setValue(int(volume) if volume else 0)
        mute_tts = self.parent.settings.value('mute_tts', type=bool)
        self.mute_button.setChecked(mute_tts)
        self.parent.tts_muted = mute_tts
