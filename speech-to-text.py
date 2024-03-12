import tkinter as tk
import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
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

def start_recording():
    global is_recording
    is_recording = True
    text_var.set("Recording...")

def stop_recording():
    global is_recording
    is_recording = False
    text_var.set("Stopped recording")
    text = record_text()
    if text:
        result_var.set(text)
    else:
        result_var.set("No text recognized")

is_recording = False

# Create the main window
root = tk.Tk()
root.title("Speech Recognition")

# Create GUI elements
record_btn = tk.Button(root, text="Record", command=start_recording)
record_btn.pack(pady=10)

stop_record_btn = tk.Button(root, text="Stop Record", command=stop_recording)
stop_record_btn.pack(pady=10)

text_var = tk.StringVar()
text_var.set("Press 'Record' to start recording")
text_label = tk.Label(root, textvariable=text_var)
text_label.pack(pady=10)

result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var)
result_label.pack(pady=10)

root.mainloop()
