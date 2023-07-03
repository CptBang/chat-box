from functools import partial

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout


class ProfilesSidebarWidget(QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.profiles = {}
        self.create_profile_buttons_sidebar()
        self.prev_button = None

    def create_profile_buttons_sidebar(self):
        for profile_name, _ in self.parent.ProfileHandler.profiles.items():
            profile_layout = self.create_profile_button_widget(profile_name)
            self.addLayout(profile_layout)
            self.profiles[profile_name] = profile_layout

        self.create_profile_button = QPushButton("Create New Profile")
        self.create_profile_button.clicked.connect(self.parent.EventHandler.handle_create_profile_button_click)
        self.addWidget(self.create_profile_button)

        # Add a spacer at the bottom of the layout
        self.addStretch()

    def create_profile_button_widget(self, profile_name):
        # Create a QHBoxLayout for each profile
        profile_layout = QHBoxLayout()
        button = QPushButton(profile_name)
        button.clicked.connect(partial(self.parent.EventHandler.handle_switch_profile, profile_name))
        profile_layout.addWidget(button, 3)

        # Create the delete profile button
        delete_button = QPushButton("🗑️")  # Using a unicode trash can symbol as the button text
        delete_button.clicked.connect(partial(self.remove_profile_button, profile_name))
        profile_layout.addWidget(delete_button, 1)

        return profile_layout

    def create_new_profile_button(self, dialog):
        profile_name = dialog.instance_name_input.text()
        character_name = dialog.character_name_input.text()
        voice = dialog.voice_option_combobox.currentText()
        appearance = dialog.appearance_input.toPlainText()
        personality = dialog.personality_input.toPlainText()
        scenario = dialog.scenario_input.toPlainText()

        profile_data = {
            "character_name": character_name,
            "voice": voice,
            "model": "eleven_monolingual_v1",
            "appearance": appearance,
            "personality": personality,
            "scenario": scenario,
            "message_file": f"{profile_name.lower()}_messages.json"
        }

        try:
            self.parent.ProfileHandler.create_new_profile_file(profile_data)
            self.parent.ProfileHandler.profiles[profile_name] = profile_data
            self.parent.ProfileHandler.write_to_profiles()
        except Exception as e:
            return

        new_button = self.create_profile_button_widget(profile_name)
        self.insertLayout(self.count() - 2, new_button)
        self.profiles[profile_name] = new_button

    def remove_profile_button(self, profile_name):
        if self.prev_butto and self.prev_button.text() == profile_name:
            self.prev_button = None
        self.parent.ProfileHandler.delete_profile(profile_name)
        layout_to_delete = self.profiles[profile_name]
        while layout_to_delete.count():
            child = layout_to_delete.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.update()

        return

    def switch_profiles(self, profile_name):
        first_item = self.profiles[profile_name].itemAt(0)
        if first_item is not None:  # Check if the item exists
            profile_button = first_item.widget()  # Get the actual widget
        profile_button.setEnabled(False)
        if self.prev_button is not None:
            self.prev_button.setEnabled(True)
        self.prev_button = profile_button
