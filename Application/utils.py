import os
import sys
import openai
from cryptography.fernet import Fernet
from elevenlabs import set_api_key


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def get_keys():
    # Now you can use resource_path to access the contents of the resources folder.
    # For example, to get the path to encrypted_key.txt:
    encrypted_key_file_path = resource_path('resources/encrypted_key')
    encrypted_api_key = read_key(encrypted_key_file_path)  # Your encrypted API key

    decryption_key_file_path = resource_path('resources/decryption_key')
    decryption_key = read_key(decryption_key_file_path)  # Your decryption key

    # Set OpenAI API Key
    openai.api_key = decrypt_key(encrypted_api_key, decryption_key)


def read_llm_key(user_api_key):
    openai.api_key = user_api_key


def read_eleven_labs_key(user_api_key):
    set_api_key(user_api_key)


def set_eleven_labs_key():
    # Now you can use resource_path to access the contents of the resources folder.
    # For example, to get the path to encrypted_key.txt:
    encrypted_key_file_path = resource_path('resources/elevenlabs_key')
    encrypted_api_key = read_key(encrypted_key_file_path)  # Your encrypted API key

    decryption_key_file_path = resource_path('resources/decryption_key')
    decryption_key = read_key(decryption_key_file_path)  # Your decryption key

    key = decrypt_key(encrypted_api_key, decryption_key)
    set_api_key(key)


def read_key(file_path):
    with open(file_path, 'rb') as file:
        encrypted_key = file.read()
    return encrypted_key


def decrypt_key(encrypted_key, decryption_key):
    cipher_suite = Fernet(decryption_key)
    decrypted_key = cipher_suite.decrypt(encrypted_key)
    return decrypted_key.decode()
