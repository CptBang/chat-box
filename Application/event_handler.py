from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QPushButton, QDialog

from Application.GUI.create_profile_dialog import CreateProfileDialog
from Application.GUI.no_profile_selected_message_box import no_profile_selected
from Application.user_prompt_processing import start_recording


class EventHandler:
    def __init__(self, mainGUI):
        self.mainGUI = mainGUI

    def handle_switch_profile(self, profile_name):
        self.mainGUI.current_profile_name = profile_name
        self.mainGUI.profiles_sidebar_widget.switch_profiles(profile_name)
        message_file_path = self.mainGUI.ProfileHandler.profiles[profile_name]["message_file"]
        message_file = self.mainGUI.ProfileHandler.get_absolute_message_file_paths(message_file_path)
        self.mainGUI.MessageCache.load_messages(message_file,
                                                self.mainGUI.ProfileHandler.profiles[profile_name])

    def handle_create_profile_button_click(self):
        dialog = CreateProfileDialog()

        if dialog.exec() == QDialog.Accepted:
            self.mainGUI.profiles_sidebar_widget.create_new_profile_button(dialog)

    def handle_process_text_button_click(self):
        if self.mainGUI.current_profile_name is None:
            no_profile_selected(self.mainGUI)
            return
        text = self.mainGUI.user_text_input.text()
        if text:
            self.mainGUI.set_user_input_buttons_enabled(False)
            self.mainGUI.start_llm_processing(text)

        self.mainGUI.user_text_input.clear()

    def handle_start_recording_button_click(self):
        if self.mainGUI.current_profile_name is None:
            no_profile_selected(self.mainGUI)
            return
        self.mainGUI.start_recording_btn.start_animation()
        self.mainGUI.set_user_input_buttons_enabled(False)
        start_recording(self.mainGUI)

    def handle_microphone_input_complete(self, result):
        if result:
            self.mainGUI.start_llm_processing(result)

    def handle_report_bug(self):
        QDesktopServices.openUrl(QUrl("https://github.com/TieConscious/chat-box/issues/new"))
