import socket
import pyttsx3
import speech_recognition as sr
import time
from main import listen_with_retry, recognize_command  # Import functions from main.py

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Create a client that connects to the server
def create_client():
    # Server's address and port
    host = '127.0.0.1'  # Loopback address (localhost)
    port = 12345  # Server port (you can change if needed)

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    return client_socket

def listen_for_commands(client_socket):
    recognizer = sr.Recognizer()

    while True:
        # Listening for commands
        print("Listening for commands...")
        audio = listen_with_retry()
        if audio:
            command = recognize_command(audio)
            if command:
                # Send the command to the server
                client_socket.sendall(command.encode('utf-8'))
                print(f"Sent command: {command}")
                
                # Receive the server's response
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Response from server: {response}")
                speak(response)
            time.sleep(2)

# Run the client
def run_client():
    client_socket = create_client()
    listen_for_commands(client_socket)

if __name__ == "__main__":
    run_client()
