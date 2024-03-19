import os
import speech_recognition as sr
import re
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()



r = sr.Recognizer()
# from googletrans import Translator


def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=1)
                print("Listening...")
                audio2 = r.listen(source2)
                print("Recognizing...")
                return r.recognize_google(audio2)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

from py_translate.translator import Translator
translator = Translator()

while True:
    clear()
    print("press 0 if you want to talk with the chatbot, or press any other key to exit")
    choice = input()
    if choice == "0":
        print("chatbot activated")
        while True:
            inpText = record_text()
            translation = translator.translate(inpText, src='id', dest='en')
            translated_text = translation.text
            print("Translated Text:", translated_text)
    else:
        break

