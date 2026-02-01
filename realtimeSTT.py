from RealtimeSTT import AudioToTextRecorder
import time

# Callback for finalized transcription chunks
def on_transcribed_chunk(text: str):
    print("Processed chunk:", text)

# Initialize recorder
recorder = AudioToTextRecorder(
    input_device_index=1,
    on_realtime_transcription_update=on_transcribed_chunk,  # callback for each chunk
    enable_realtime_transcription=True,                     # must enable realtime for updates
    realtime_processing_pause=0.1,                           # process frequently
    use_main_model_for_realtime=False                        # optional: use separate lightweight model
)

# Start recording
print("Recording... speak now")
recorder.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping...")
    recorder.stop()
