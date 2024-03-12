import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
    # Loop in case of errors
    while(1):
        try:
            # Use the microphone as source for input
            with sr.Microphone() as source2:
                # prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # Listen for the user's input
                print("Listening...")
                audio2 = r.listen(source2)

                # Using google to recognize audio
                print("Recognizing...")
                MyText = r.recognize_google(audio2)

                return MyText
        
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")

    return

# def output_text(text):
#     f = open("output.txt", "a")
#     f.write(text)
#     f.write("\n")
#     f.close()
#     return

def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text + "\n")

# while (1):
#     text = record_text()
#     output_text(text)

#     print(text + "\n")
        
# Record text once
text = record_text()
if text:
    output_text(text)
    print(text + "\n")
