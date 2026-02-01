# this file enables speech to text
# using a Blue Snowball Ice connected to a Beagle-YAi

import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

with mic as source:
    print("speak!")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    print("audio captured...")

try:
    text = r.recognize_google(audio)
    print(text)
except sr.UnknownValueError:
    print("could not understand")
except sr.RequestError as e:
    print("amazon could not process")
