import speech_recognition as sr
import pyttsx3
import webbrowser
import sys
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to commands
def listen_with_retry():
    recognizer = sr.Recognizer()
    
    # Attempt to recognize speech with retries in case of timeout or errors
    with sr.Microphone() as source:
        print("Initializing microphone...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Microphone initialized. Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("Audio captured.")
            return audio
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that. Please try again.")
            return None
        except sr.RequestError:
            print("Network error occurred, please check your connection.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

def recognize_command(audio):
    recognizer = sr.Recognizer()
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Recognized: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the speech.")
        return None
    except sr.RequestError:
        print("Error with the request.")
        return None

# Main function to run the assistant
def main():
    speak("Voice assistant initializing...")
    time.sleep(1)

    while True:
        audio = listen_with_retry()
        if audio:
            command = recognize_command(audio)
            if command:
                process_command(command)

# Process different commands
def process_command(command):
    if 'open chrome' in command:
        speak("Opening Chrome.")
        webbrowser.open("https://www.google.com")
    elif 'open youtube' in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif 'exit' in command or 'quit' in command:
        speak("Exiting.")
        sys.exit(0)
    else:
        speak("Sorry, I did not recognize the command.")

if __name__ == "__main__":
    main()
