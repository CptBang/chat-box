from functools import partial

from PySide6.QtCore import QSettings, Signal, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, \
    QHBoxLayout, QMenuBar

import utils
from Application.GUI.circle_widget import CircleWidget
from Application.GUI.first_time_api_prompt_dialog import FirstTimeAPIPromptDialog
from Application.GUI.llm_output_widget import LLMOutputWidget
from Application.GUI.profiles_sidebar_widget import ProfilesSidebarWidget
from Application.GUI.recording_button import RecordingButton
from Application.GUI.settings_dialog import SettingsDialog
from Application.GUI.widget_factory import WidgetFactory
from Application.audio_player_thread import AudioplayerThread
from Application.audio_utils import get_input_devices
from Application.event_handler import EventHandler
from Application.llm_thread import LLMThread
from Application.message_cache import MessageCache

import platform

from Application.profile_file_handler import ProfileFileHandler


class Application(QMainWindow):
    voice_to_text_signal = Signal(str)
    recording_complete_signal = Signal()

    def __init__(self):
        super().__init__()

        self.settings_dialog = None
        self.user_text_input = None
        self.llm_output_widget = None
        self.settings = None
        self.settings_action = None
        self.settings_menu_button = None
        self.menu_bar = None
        self.current_profile_name = None
        self.audio_thread = None
        self.tts_muted = False
        self.settings = QSettings("GitHub_CptBang_TTM", "Talk to Me")
        settings_version = self.settings.value("settings_version", "0.0")

        self.ProfileHandler = ProfileFileHandler()
        self.EventHandler = EventHandler(self)
        self.WidgetFactory = WidgetFactory(self)
        self.setWindowTitle("Help me Step-bro")
        self.resize(900, 600)
        self.MessageCache = MessageCache(self)
        self.check_first_run()

        self.llm_thread = None
        self.record_thread = None
        self.process_thread = None

        self.microphones = get_input_devices()

        # Connect signals to slots
        self.voice_to_text_signal.connect(self.EventHandler.handle_microphone_input_complete)

        self.create_menu_bar()
        self.create_widgets()

    def check_first_run(self):
        # Check if the application has been run before
        if self.settings.value("first_run", "true") == "true":
            self.settings.setValue("first_run", "false")

            # Set default settings here
            self.settings.setValue('openai_api_key', 'default_value')
            self.settings.setValue('elevenlabs_api_key', 'default_value')
            self.settings.setValue('mic_sensitivity', '50')
            self.settings.setValue('volume', '50')
            FirstTimeAPIPromptDialog()
        else:
            utils.read_llm_key(self.settings.value('openai_api_key', ''))
            utils.read_eleven_labs_key(self.settings.value('elevenlabs_api_key', ''))

    def create_menu_bar(self):
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.SettingsDialog = SettingsDialog(self)
        self.settings_menu_button = self.menu_bar.addMenu("Settings")
        self.settings_action = QAction("Open Settings", self)
        self.settings_action.triggered.connect(self.SettingsDialog.show)
        self.settings_menu_button.addAction(self.settings_action)

        self.report_bug_menu_button = QAction("Report a Bug", self)
        self.report_bug_menu_button.triggered.connect(self.EventHandler.handle_report_bug)
        self.menu_bar.addAction(self.report_bug_menu_button)

    def create_widgets(self):
        self.microphone_option_combobox = self.WidgetFactory.create_microphone_combobox(self.settings)

        # Create a QHBoxLayout for the profile buttons and the GPT3 output
        llm_output_and_profiles_layout = QHBoxLayout()

        # Create a QVBoxLayout for profile buttons
        self.profiles_sidebar_widget = ProfilesSidebarWidget(self)

        # Add profile_buttons_layout to the llm_output_layout
        llm_output_and_profiles_layout.addLayout(self.profiles_sidebar_widget, 1)

        # Add a widget for the GPT3 output
        self.llm_output_widget = LLMOutputWidget(self)

        # Add gpt_output_widget to the llm_output_layout
        llm_output_and_profiles_layout.addWidget(self.llm_output_widget, 3)

        self.user_text_input = QLineEdit(self)
        self.process_text_btn = QPushButton("Process Text", self)
        self.process_text_btn.clicked.connect(self.EventHandler.handle_process_text_button_click)

        # Create a QHBoxLayout
        hbox = QHBoxLayout()

        # Add the QLineEdit and the button to the layout
        hbox.addWidget(self.user_text_input, 3)  # The second argument is the stretch factor
        hbox.addWidget(self.process_text_btn, 1)

        # Set the layout of the widget to the QHBoxLayout
        self.setLayout(hbox)

        # Create a recording button
        self.start_recording_btn = RecordingButton("Start Recording", self)
        self.start_recording_btn.clicked.connect(self.EventHandler.handle_start_recording_button_click)

        # Create a red circle
        self.animation_circle = CircleWidget(self)
        self.animation_circle.hide()
        self.animation_circle.raise_()  # Ensure CircleWidget stays on top

        # Create a layout and add widgets to it
        layout = QVBoxLayout()
        layout.addLayout(self.profiles_sidebar_widget)
        layout.addWidget(self.WidgetFactory.microphone_combobox)
        layout.addLayout(llm_output_and_profiles_layout)
        layout.addLayout(hbox)
        layout.addWidget(self.start_recording_btn)

        # create a widget to hold the layout
        container = QWidget()
        container.setLayout(layout)

        # set the widget with the layout as the central widget of the main window
        self.setCentralWidget(container)

    def start_llm_processing(self, text):
        self.MessageCache.add_message({"role": "user", "content": text})
        # Add the label text with a tag
        self.llm_output_widget.append(f"<font color='#4169E1'>You:</font>")
        # Add the response text
        self.llm_output_widget.append(f"{text}\n")  # Added an extra newline for spacing
        self.animation_circle.start_animation()
        self.llm_thread = LLMThread(self.MessageCache.all_messages)
        self.llm_thread.result_signal.connect(self.handle_results_callback)
        self.llm_thread.error_signal.connect(self.process_text_error_callback)
        self.llm_thread.start()

    def handle_results_callback(self, text):
        self.animation_circle.stop_animation()
        profile = self.ProfileHandler.profiles[self.current_profile_name]
        if text is not None and not self.tts_muted:
            self.audio_thread = AudioplayerThread(text, profile)
            self.audio_thread.finished.connect(self.on_llm_response_complete)
            self.audio_thread.error.connect(self.process_text_error_callback)
            self.audio_thread.start()
        if text is not None and self.tts_muted:
            self.on_llm_response_complete(text)

    def on_llm_response_complete(self, text):
        self.MessageCache.add_message({"role": "assistant", "content": text})
        # Add the label text with a tag
        self.llm_output_widget.append(f"<font color='#FF6347'>{self.ProfileHandler.profiles[self.current_profile_name]['character_name']}:</font>")
        # Add the response text
        self.llm_output_widget.append(f"{text}\n")  # Added an extra newline for spacing
        self.set_user_input_buttons_enabled(True)



    def process_text_error_callback(self, error_message):
        self.animation_circle.stop_animation()
        self.play_system_sound()
        QMessageBox.critical(self, "Error", error_message)
        self.llm_output_widget.append(f"<font color='red'>\nError:\n{error_message}\n")

    def closeEvent(self, event):
        selected_microphone = self.WidgetFactory.microphone_combobox.currentText()
        self.settings.setValue("selected_microphone", selected_microphone)
        if self.audio_thread:
            self.audio_thread.terminate()
        self.MessageCache.stop()
        event.accept()
        super().closeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)  # Call the parent class showEvent method
        self.position_animation_circle()
        self.user_text_input.setFocus()

    def resizeEvent(self, event):
        super().resizeEvent(event)  # Call the parent class resizeEvent method
        self.position_animation_circle()

    def position_animation_circle(self):
        # Position the CircleWidget in the top right corner of the QTextEdit
        circle_x = self.llm_output_widget.width() - self.animation_circle.width()
        circle_y = self.animation_circle.width()
        self.animation_circle.move(circle_x, circle_y)
        self.animation_circle.raise_()  # Raise the CircleWidget to the top of the widget stack

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.EventHandler.handle_process_text_button_click()

    def play_system_sound(self):
        if platform.system() == 'Windows':
            import winsound
            winsound.MessageBeep(winsound.MB_ICONHAND)
        elif platform.system() == 'Darwin':
            import subprocess
            subprocess.call(['afplay', '/System/Library/Sounds/Basso.aiff'])
        elif platform.system() == 'Linux':
            import subprocess
            subprocess.call(['paplay', '/usr/share/sounds/gnome/default/alerts/bell.oga'])
        else:
            print('Unsupported platform:', platform.system())

    def set_user_input_buttons_enabled(self, enabled):
        self.process_text_btn.setEnabled(enabled)
        self.start_recording_btn.setEnabled(enabled)
