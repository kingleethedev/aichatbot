import re
import string
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext

# Function to read the text file and create a dictionary of keyword-response pairs
def load_qa_file(filename):
    qa_dict = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if ':' in line:
                keywords, response = line.split(':', 1)
                for keyword in keywords.split():
                    qa_dict[keyword.strip().lower()] = response.strip()
    return qa_dict

# Function to normalize text (convert to lowercase and remove punctuation)
def normalize_text(text):
    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Function to get an answer based on the detected keyword in the user's question
def get_answer(question, qa_dict, variables):
    question = normalize_text(question)
    for keyword in qa_dict:
        if keyword in question:
            response = qa_dict[keyword]
            # Replace placeholders with actual variables
            for var, value in variables.items():
                response = response.replace(f'{{{var}}}', value)
            return response
    return "Sorry, I don't have an answer for that question."

# Function to speak text using TTS
def speak(text, voice_id=1):
    engine = pyttsx3.init()
    if voice_id:
        engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

# Function to listen and respond
def listen_and_respond():
    try:
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            voice = listener.listen(source)
            question = listener.recognize_google(voice)
            print(f'You asked: {question}')
            chat_area.insert(tk.END, f'You: {question}\n')
            answer = get_answer(question, qa_dict, variables)
            print(f'Answer: {answer}')
            chat_area.insert(tk.END, f'Bot: {answer}\n')
            speak(answer)
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        chat_area.insert(tk.END, "Bot: Sorry, I did not understand that.\n")
        speak("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        chat_area.insert(tk.END, "Bot: Sorry, the service is down; please try again later.\n")
        speak("Sorry, the service is down; please try again later.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        chat_area.insert(tk.END, "Bot: An error occurred.\n")
        speak("An error occurred.")

# Load the Q&A file
qa_file = 'data.txt'
qa_dict = load_qa_file(qa_file)
print('Debug: Loaded Q&A pairs', qa_dict)

# Define the variables to be used in responses
variables = {
    'user_name': 'Alice',
    'creator_name': 'John Doe'
}

# Initialize Tkinter window
root = tk.Tk()
root.title("KINGbot")
root.geometry("500x400")

# ScrolledText widget to display chat
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 10))
chat_area.pack(pady=10)
chat_area.insert(tk.END, "KINGBot: Hello, I am your KINGbot. Click 'Speak' to ask a question.\n")

# Button to start listening
button = tk.Button(root, text="Speak", command=listen_and_respond, font=("Arial", 12))
button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()



