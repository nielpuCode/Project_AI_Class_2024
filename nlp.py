from keras.models import load_model
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
import customtkinter
import tkinter as tk
from tkinter import scrolledtext
import threading

import os
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()

# Set appearance mode
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

# Create the root window
root = customtkinter.CTk()
root.geometry("500x500")
root.title("Speech to Text Chatbot")

# Create a scrolled text widget to display conversation
conversation = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
conversation.pack(pady=20, padx=10)

# Create status label
status_label = customtkinter.CTkLabel(root, text="")
status_label.pack()

# Define function to update status message
def update_status(message):
    status_label.configure(text=message)

model = load_model("chatbot_AI.h5")
with open('intents_exercise.json',encoding='utf-8') as file:
    data = json.load(file)

lemmatizer = WordNetLemmatizer()


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
                if i["tag"] == "terminate":
                    result = random.choice(i["responses"])
                    exit()  # Terminate the program
                else:
                    result = random.choice(i["responses"])
                break
        return result

import pyttsx3
import re
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup

r = sr.Recognizer()

def perform_math_operation(inpText):
    inpText = re.sub(r'[^0-9+\-*/]', '', inpText)
    try:
        resultCalc = eval(inpText)
        text_to_speech = f"the result of {inpText} is {resultCalc}"
        engine.say(text_to_speech)
        engine.runAndWait()
        return text_to_speech
    except Exception as e:
        return f"Error: {str(e)}"

def extract_city(text):
    city = ""
    words = text.split()
    try:
        index = words.index("in")
        if index + 1 < len(words):
            if index + 2 < len(words):
                if words[index + 2].istitle():
                    city = words[index + 1] + " " + words[index + 2]
                else:
                    city = words[index + 1]
            else:
                city = words[index + 1]
    except ValueError:
        pass
    return city

def get_weather(city):
    url = "https://www.google.com/search?q=weather+" + city + "&hl=en"
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = str.split('\n')
    time = data[0]
    sky = data[1]
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text
    pos = strd.find('Wind')
    other_data = strd[pos:]
    weather_info = f"\nTemperature is {temp}\nTime: {time}\nSky Description: {sky}\n{other_data}\n"
    return weather_info

# Initialize Speech Engine
engine = pyttsx3.init()

# Flag to indicate whether the program should terminate
terminate_program = False

def process_speech_input():
    global terminate_program  # Declare terminate as flag
    global engine  # Declare engine as global
    
    while not terminate_program:  # Continue listening until termination flag is set
        conversation.insert(customtkinter.END, "Chatbot: Listening...\n")
        conversation.see(customtkinter.END)  # Scroll to the end of the conversation
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            conversation.insert(customtkinter.END, "Chatbot: Recognizing...\n")
            conversation.see(customtkinter.END)  # Scroll to the end of the conversation
            text = r.recognize_google(audio, language="en-US")
            conversation.insert(customtkinter.END, "User: " + text + "\n")
            conversation.see(customtkinter.END)  # Scroll to the end of the conversation
            translated_text = GoogleTranslator(source='auto', target='en').translate(text)
            intents = pred_class(translated_text, words, classes, model)
            if "terminate" in translated_text.lower():
                conversation.insert(customtkinter.END, "Chatbot: Terminating the program...\n")
                conversation.see(customtkinter.END)  # Scroll to the end of the conversation
                terminate_program = True  # Set the flag to terminate
            elif "calculate " in translated_text.lower():
                math_operation = translated_text.lower().replace("calculate ", "")
                conversation.insert(customtkinter.END, f"Chatbot: Calculating {math_operation}...\n")
                conversation.see(customtkinter.END)  # Scroll to the end of the conversation
                result = perform_math_operation(math_operation)
                conversation.insert(customtkinter.END, result + "\n\n")
                conversation.see(customtkinter.END)  # Scroll to the end of the conversation
            elif "weather in" in text:
                city = extract_city(text)
                if city:
                    conversation.insert(customtkinter.END, f"Chatbot: Weather in {city}:\n")
                    conversation.see(customtkinter.END)  # Scroll to the end of the conversation
                    weather_info = get_weather(city)
                    conversation.insert(customtkinter.END, weather_info + "\n")
                    conversation.see(customtkinter.END)  # Scroll to the end of the conversation
                    engine.say(weather_info)
                    engine.runAndWait()
                else:
                    conversation.insert(customtkinter.END, "Chatbot: City not specified.\n")
                    conversation.see(customtkinter.END)  # Scroll to the end of the conversation
            else:
                response = get_response(intents, data)
                conversation.insert(customtkinter.END, "Chatbot: " + response + "\n\n")
                conversation.see(customtkinter.END)  # Scroll to the end of the conversation
                engine.say(response)
                engine.runAndWait()
        except sr.UnknownValueError:
            conversation.insert(customtkinter.END, "Chatbot: Sorry, I could not understand the audio.\n\n")
            conversation.see(customtkinter.END)  # Scroll to the end of the conversation
        except sr.RequestError as e:
            conversation.insert(customtkinter.END, "Chatbot: Could not request results from Google Speech Recognition service; {0}\n\n".format(e))
            conversation.see(customtkinter.END)  # Scroll to the end of the conversation

    # Check if the termination flag is set
    if terminate_program:
        root.destroy()  # Terminate the GUI application
        exit()  # Terminate the program


# Define function to activate the program
def activate_chatbot():
    global terminate_program  # Declare global flag
    
    conversation.insert(customtkinter.END, "Chatbot: Activated. Listening...\n")
    conversation.see(customtkinter.END)  # Scroll to the end of the conversation

    # Start speech recognition process in a separate thread
    threading.Thread(target=process_speech_input).start()
   
# Create a button to activate the program
activate_button = customtkinter.CTkButton(root, text="Activate Chatbot", command=activate_chatbot)
activate_button.pack()

# Start the GUI main loop
root.mainloop()