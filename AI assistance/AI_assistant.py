from __future__ import print_function
import datetime
import pyttsx3
import speech_recognition as sr
import subprocess
from openai import OpenAI
client = OpenAI(api_key = '<key>')

def chat_with_ai(context):
    try:
        completion = client.chat.completions.create(
            model =  "gpt-3.5-turbo",  # Use "gpt-3.5-turbo" for cost efficiency if needed
            messages=context
        )
        return completion.choices[0].message 
    except Exception as e:
        return f"Error: {str(e)}"
    


prompt =  ''' You are a motivational coach John while enjoy teach Python and data structures. You love 
using simple words to explain complex concepts. You first introduce the concept then explain by using simple term.'''

context = [{'role': 'system', 'content' : prompt},
           {'role': 'user', 'content': 'my name is john'}]

print("AI Tutor: Hi John! How can I help you learn Python today?")

def ai_tutor():
 while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        print("AI Tutor: Goodbye! Keep coding and stay curious!")
        break
    context.append({'role': 'user', 'content': user_input})
    response = chat_with_ai(context)
    print(f"AI Tutor: {response}")
    context.append({'role': 'assistant', 'content': str(response)})






def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except KeyboardInterrupt:
            print("\nStopped listening.")
        except Exception as e:
            print("Exception: " + str(e))

    return said.lower()

def get_audio_note():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Press Ctrl+C to stop.")
        r.adjust_for_ambient_noise(source, duration=1)  # Calibrate to background noise
        said = ""

        try:
            while True:
                print("Listening for another phrase...")
                audio = r.listen(source, phrase_time_limit=10)  # Listen for up to 10 seconds
                chunk = r.recognize_google(audio)
                print(chunk)
                said += " " + chunk
        except KeyboardInterrupt:
            print("\nStopped listening.")
        except Exception as e:
            print("Exception: " + str(e))

    return said.lower()

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["open", "-a", "TextEdit", file_name])
    
WAKE = "hey simon"
print("Start")
while True:
    print("Listening")
    text = get_audio()

    if text.count(WAKE) > 0:
        speak("I am ready")
        text = get_audio()
    
        NOTE_STRS = ["make a note", "write this down", "remember this"]
        AI_STRS   = ["bring me john", 'johnny come']
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("What would you like me to write down?")
                note_text = get_audio_note()
                note(note_text)
                state = False
                speak("I've made a note of that.")
        for phrase in AI_STRS:
            if phrase in text:
                ai_tutor()





