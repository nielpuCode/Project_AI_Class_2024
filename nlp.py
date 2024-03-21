from tensorflow.keras.models import load_model
import matplotlib
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import string
import random
import nltk
from nltk.stem import WordNetLemmatizer
from variables import words, classes, data_X
import pyttsx3
import speech_recognition as sr
import re
from deep_translator import GoogleTranslator

import os
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()



lemmatizer = WordNetLemmatizer()

model = load_model("./chatbot_AI.h5")
with open('intents_exercise.json',encoding='utf-8') as file:
    data = json.load(file)


def clean_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def bag_of_words(text, vocab):
    tokens = clean_text(text)
    bow = [0] * len(vocab)
    for word in tokens:
        for idx, w in enumerate(vocab):
            if w == word:
                bow[idx] = 1
    return np.array(bow)

def pred_class(text, vocab, labels, model):
    bow = bag_of_words(text, vocab)
    result = model.predict(np.array([bow]))[0]
    thresh = 0.5
    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]
    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in y_pred:
        return_list.append(labels[r[0]])
    return return_list

def get_response(intents_list, intents_json):
    if not intents_list:
        return "Sorry! I don't understand."
    else:
        tag = intents_list[0]
        list_of_intents = intents_json["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i["responses"])
                break
        return result

#Original code: ------------------------------------------------------------------------------------------------
# r = sr.Recognizer()

# def record_text():
#     while True:
#         try:
#             with sr.Microphone() as source2:
#                 r.adjust_for_ambient_noise(source2, duration=1)
#                 print("Listening...")
#                 audio2 = r.listen(source2)
#                 print("Recognizing...")
#                 return r.recognize_google(audio2, language="id-ID")
#         except sr.RequestError as e:
#             print("Could not request results; {0}".format(e))
#         except sr.UnknownValueError:
#             print("Unknown error occurred")


# while True:
#     clear()
#     print("press 0 if you want to talk with the chatbot, or press any other key to exit")
#     choice = input()
#     if choice == "0":
#         print("chatbot activated")
#         while True:
#             inpText = record_text()
#             print(f"Input text: {inpText}")
#             translated_text = GoogleTranslator(source='auto', target='en').translate(inpText)
#             print(f"Translated text: {translated_text}")
#             if translated_text.lower() == "0":
#                 print("Chatbot deactivated. Press 0 to activate again.")
#                 break
#             intents = pred_class(translated_text, words, classes, model)
#             result = get_response(intents, data)
#             print("Response:", result)
#             # engine = pyttsx3.init()
#             # engine.say(result)
#             # engine.runAndWait()
#     else:
#         break
#---------------------------------------------------------------------------------------------------------------

import pyttsx3
import re
import speech_recognition as sr


def record_text():
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as main_mic:
                r.adjust_for_ambient_noise(main_mic, duration=1)
                print("Listening...")
                input_audio = r.listen(main_mic)
                print("Recognizing...")
                return r.recognize_google(input_audio)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

def perform_math_operation(inpText):
    inpText = re.sub(r'[^0-9+\-*/]', '', inpText)
    print("Text:", inpText)
    try:
        resultCalc = eval(inpText)
        text_to_speech = f"the result of {inpText} is {resultCalc}"
        engine.say(text_to_speech)
        engine.runAndWait()
        return text_to_speech
    except Exception as e:
        return f"Error: {str(e)}"

engine = pyttsx3.init()

while True:
    print("press 0 if you want to talk with the chatbot, or press any other key to exit")
    choice = input()
    if choice == "0":
        print("chatbot activated")
        while True:
            inpText = record_text()
            if "calculate " in inpText.lower():
                mathOperation = inpText.lower().replace("calculate ", "")
                print(perform_math_operation(mathOperation))
            elif inpText.lower() == "0":
                print("Chatbot deactivated. Press 0 to activate again.")
                break
            else:
                intents = pred_class(inpText, words, classes, model)
                result = get_response(intents, data)
                print(result)
                engine.say(result)
                engine.runAndWait()
    else:
        break

