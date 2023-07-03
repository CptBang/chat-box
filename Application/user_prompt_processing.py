import queue
import threading
import time
from threading import Timer
import speech_recognition as sr

import Application.constants
from Application.audio_utils import get_current_input_index


def start_recording(app):
    app.recording = True
    app.record_thread = threading.Thread(target=record, args=(app,))
    app.record_thread.start()


def record(app):
    # Initialize the recognizer
    app.r = sr.Recognizer()
    app.audio_queue = queue.Queue()

    # # Get the index of the selected microphone
    mic_index = get_current_input_index(app)

    # Record the audio
    with sr.Microphone(device_index=mic_index) as source:
        # adjust for ambient noise
        app.r.adjust_for_ambient_noise(source, duration=0.5)

        while app.recording:
            try:
                audio_data = app.r.listen(source, timeout=Application.constants.MICROPHONE_TIMEOUT,
                                          phrase_time_limit=Application.constants.MICROPHONE_PHRASE_TIME_LIMIT)
                app.audio_queue.put(audio_data)  # Add the audio data to the queue
            except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError, AssertionError):
                app.recording = False
                app.recording_complete_signal.emit()
                process_and_handle_results(app)
                break  # If no speech is detected within the timeout, stop recording


def process_and_handle_results(app):
    # Create a Queue for the result
    result_queue = queue.Queue()

    # Start a new thread to process the audio data, passing the Queue as an argument
    app.process_thread = threading.Thread(target=process_audio,
                                          args=(app, result_queue, app.process_text_error_callback))
    app.process_thread.start()

    # Check the queue periodically for results, without blocking the main thread
    Timer(0.1, check_for_results,
          args=[app, result_queue, app.process_thread]).start()


def process_audio(app, result_queue, error_callback):
    full_text = ''
    while not app.audio_queue.empty():
        audio_data = app.audio_queue.get()

        try:
            # Use recognizer to convert audio to text
            text = app.r.recognize_google(audio_data)
            full_text += text + ' '  # Add the transcribed text to the full text
        except sr.UnknownValueError:
            continue
            # error_callback("Error: Sorry, I could not understand your speech")
        except sr.RequestError:
            error_callback("Error", app.constants.ERROR_REQUEST_GOOGLE)

        time.sleep(0.1)  # Avoid busy waiting

    result_queue.put(full_text)


def check_for_results(app, result_queue, process_thread):
    if not process_thread.is_alive() and result_queue.empty():
        # If the processing thread has finished and the queue is empty, do nothing
        return
    elif not process_thread.is_alive():
        # If the processing thread has finished, get the result from the Queue
        result = result_queue.get()
        # Emit the signal instead of directly calling the callback
        app.voice_to_text_signal.emit(result)
        process_thread.join()

        # Empty the queue
        while not result_queue.empty():
            try:
                result_queue.get_nowait()
            except queue.Empty:
                break

        # app.set_user_input_buttons_enabled(True)
    else:
        # If the processing thread is still running, check again in 100ms
        Timer(0.1, check_for_results, args=[app, result_queue, process_thread]).start()
