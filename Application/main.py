import os
import sys

from PySide6.QtWidgets import QApplication
from Application.main_gui import Application
from Application.profile_file_handler import ProfileFileHandler


def main():
    # Start the GUI
    app = QApplication([])
    # Add the directory containing ffplay to the PATH
    os.environ['PATH'] = os.path.join(os.path.dirname(sys.executable), 'ffmpeg', 'bin') + os.pathsep + \
                         os.environ['PATH']

    # Create and show the main window
    window = Application()
    window.show()

    # Run the event loop
    app.exec()

    # After the GUI is closed, join all threads
    if window.record_thread is not None:
        window.record_thread.join()
    if window.process_thread is not None:
        window.process_thread.join()


if __name__ == '__main__':
    main()
