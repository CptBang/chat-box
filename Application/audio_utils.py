import pyaudio
import speech_recognition as sr


def get_input_devices():
    p = pyaudio.PyAudio()
    usable_mics = {}

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info.get('name')
        host_api_info = p.get_host_api_info_by_index(device_info.get('hostApi'))

        # Check if this device has any input channels, is not the "Microsoft Sound Mapper - Input",
        # and is from the DirectSound API
        if device_info.get('maxInputChannels') > 0 \
                and "Microsoft Sound Mapper - Input" not in device_name \
                and "mapper" not in device_name.lower() \
                and host_api_info.get('type') == pyaudio.paWASAPI:
            usable_mics[device_name] = i

    p.terminate()

    return usable_mics


def get_current_input_index(app):
    mic_index = app.microphones[app.microphone_option_combobox.currentText()]
    return mic_index
