import json
import os
import threading

from Application.llm_memory import inject_personality


class MessageCache:
    def __init__(self, mainGUI, cache_size=100):
        # Use __file__ attribute to get the path of the current script
        self.current_script_path = os.path.dirname(os.path.realpath(__file__))
        self.current_file_path = None
        self.write_interval = None
        self.stopped = None
        self.all_messages = []
        self.mainGUI = mainGUI
        self.cache_size = cache_size
        self.lock = threading.Lock()

    def load_messages(self, file_path, incoming_profile):
        print(f"loading file_path + {file_path}")
        if file_path == self.current_file_path:
            return
        elif self.current_file_path is not None:
            self.write_to_file()

        if os.path.isfile(file_path):
            with self.lock:
                with open(file_path, 'r') as f:
                    try:
                        loaded_messages = json.load(f)

                        if not loaded_messages:
                            loaded_messages = [inject_personality(incoming_profile)]
                        self.all_messages = loaded_messages
                    except json.JSONDecodeError:
                        print("Error: Invalid JSON data in 'messages.json'")
                        self.all_messages = [inject_personality(incoming_profile)]
                    self.current_file_path = file_path

            self.mainGUI.llm_output_widget.update_llm_output_widget(self.all_messages)

    def add_message(self, message):
        print(message)
        with self.lock:
            self.all_messages.append(message)
            self.write_to_file()

    def write_messages(self):
        while True:
            if self.stopped.wait(self.write_interval):
                break
            self.write_to_file()

    def stop(self):
        self.write_to_file()
        pass

    def write_to_file(self):
        if not self.current_file_path:
            return
        with open(self.current_file_path, 'w') as f:
            try:
                print(self.all_messages)
                json.dump(self.all_messages, f)
            except Exception as e:
                print(f"Error writing to file: {e}")
