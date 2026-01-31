# this file enables speech to text
# using a Blue Snowball Ice connected to a Beagle-YAi

import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("speak!")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    print("audio captured...")

try:
    text = r.recognize_amazon(audio)
    print(text)
except sr.UnknownValueError:
    print("count not understand")
except sr.RequestError as e:
    print("amazon could not process")
