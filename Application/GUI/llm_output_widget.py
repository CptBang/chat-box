from PySide6.QtWidgets import QTextEdit


class LLMOutputWidget(QTextEdit):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setReadOnly(True)

    def update_llm_output_widget(self, loaded_messages):
        self.clear()
        character_name = self.parent.ProfileHandler.profiles[self.parent.current_profile_name]['character_name']
        for message in loaded_messages:
            role = message['role']
            content = message['content']

            if role == "system":
                continue
            elif role == "user":
                self.append(f"<font color='#707070'>You:</font>")
            else:
                self.append(f"<font color='#505050'>{character_name}:</font>")
            # Add the response text
            self.append(f"{content}\n")  # Added an extra newline for spacing

    def write_to_widget(self):
        return

    def clear_widget(self):
        return
