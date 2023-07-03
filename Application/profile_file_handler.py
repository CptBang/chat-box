import json
import os

from PySide6.QtWidgets import QMessageBox

from Application.llm_memory import inject_personality


class ProfileFileHandler:

    def __init__(self):
        self.current_script_path = os.path.dirname(os.path.realpath(__file__))
        self.profiles_path = os.path.join(self.current_script_path, 'character_profiles', 'profiles.json')
        self.profiles = {}
        try:
            self.get_all_profiles()
        except FileNotFoundError as e:
            QMessageBox.critical("FileNotFound Error", e)
        except json.JSONDecodeError as e:
            QMessageBox.critical("JSONDecode Error", e)
        except Exception as e:
            QMessageBox.critical("Unknown Error", e)

    def get_all_profiles(self):
        with open(self.profiles_path, 'r') as f:
            self.profiles = json.load(f)

    def get_absolute_message_file_paths(self, file_name):
        # Construct the path to the profiles.json file
        json_file_path = os.path.join(self.current_script_path, 'character_profiles', file_name)

        return json_file_path

    def write_to_profiles(self):
        try:
            with open(self.profiles_path, 'w') as f:
                json.dump(self.profiles, f, indent=4)
        except IOError as e:
            QMessageBox.critical("IO Error", e)
        except Exception as e:
            QMessageBox.critical("Unexpected Error", e)

    def create_new_profile_file(self, new_profile):
        try:
            new_message_file = os.path.join(self.current_script_path, 'character_profiles', new_profile["message_file"])
            personality_injection = inject_personality(new_profile)
            with open(new_message_file, 'w') as f:
                json.dump([personality_injection], f)
        except IOError as e:
            QMessageBox.critical("IO Error", e)
        except Exception as e:
            QMessageBox.critical("Unexpected Error", e)

    def delete_profile(self, profile_name):
        try:
            file_to_delete = self.get_absolute_message_file_paths(self.profiles[profile_name]["message_file"])
            os.remove(file_to_delete)  # Use os.remove to delete files
            self.profiles.pop(profile_name)

            # Now, remove the profile from the profiles.json file
            with open(self.profiles_path, 'r') as f:
                profiles_data = json.load(f)
            profiles_data.pop(profile_name)
            with open(self.profiles_path, 'w') as f:
                json.dump(profiles_data, f, indent=4)

        except IOError as e:
            QMessageBox.critical("IO Error", e)
