from PySide6.QtWidgets import QComboBox


class WidgetFactory:
    def __init__(self, parent):
        self.selected_microphone = None
        self.parent = parent
        self.microphone_combobox = None

    def create_microphone_combobox(self, settings):
        self.selected_microphone = settings.value("selected_microphone", "")
        mic_names = list(self.parent.microphones.keys())
        # Add a combobox for selecting a microphone
        self.microphone_combobox = QComboBox(self.parent)
        self.microphone_combobox.addItems(mic_names)

        if self.selected_microphone in mic_names:
            self.microphone_combobox.setCurrentIndex(mic_names.index(self.selected_microphone))

        return self.microphone_combobox

    # def create_profile_buttons(self):
    #     # The code for creating profile_buttons here
    #
    # def create_gpt_output_widget(self):
    #     # The code for creating gpt_output_widget here

    # ... and so on for each widget ...