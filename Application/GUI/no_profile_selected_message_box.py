from PySide6.QtWidgets import QMessageBox


def no_profile_selected(app):
    if app.current_profile_name is None:
        # Create a message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)  # Set the icon to the warning icon
        msg.setWindowTitle("Error")  # Set the window title
        msg.setText("No profile selected!")  # Set the main message
        msg.setInformativeText("Please select a profile before proceeding.")  # Set the secondary text
        msg.exec()  # Show the message box