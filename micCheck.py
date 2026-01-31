import pyaudio

def list_microphones():
    p = pyaudio.PyAudio()

    # Get the number of audio devices
    device_count = p.get_device_count()

    # Iterate through all devices and check for input (microphone) devices
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:  # Check if it's an input device (microphone)
            print(f"Device {i}: {device_info['name']} - {device_info['maxInputChannels']} channels")

    p.terminate()

if __name__ == "__main__":
    list_microphones()
