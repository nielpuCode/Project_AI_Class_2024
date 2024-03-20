import os
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
clear()

from deep_translator import GoogleTranslator

# translator = google_translator()

# text1 = "halo apa kabar"
text1 = "aku mau tidur ngantuk"

translated = GoogleTranslator(source='auto', target='en').translate(text1)
print(translated)