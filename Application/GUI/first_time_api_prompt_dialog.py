from PySide6.QtWidgets import QInputDialog, QDialog

from Application.utils import get_keys, read_llm_key, set_eleven_labs_key


class FirstTimeAPIPromptDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Add dialog to prompt for API key
        dialog = QInputDialog(self)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle("API Keys")
        dialog.setLabelText("OpenAI Key (if you don't have one, leave it blank):")
        # dialog.setLabelText("ElevenLabs (if you don't have one, leave it blank):")
        dialog.resize(400, 200)

        if dialog.exec():
            self.llm_api_key = dialog.textValue()
        else:
            self.llm_api_key = None

        if self.llm_api_key is None or self.llm_api_key == '':
            print("No API key entered. Using the encrypted API key.")
            get_keys()  # Use the decrypted API key
        else:
            read_llm_key(self.llm_api_key)  # Set the API key provided by the user

        set_eleven_labs_key()
