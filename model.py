import speech_recognition as sr
from openai import OpenAI
import pyttsx3

# Initialize OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# Initialize the recognizer for speech recognition
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties for a more natural-sounding voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Selecting a female voice for example
engine.setProperty('rate', 180)  # Adjust the speech rate (words per minute)
engine.setProperty('volume', 0.9)  # Adjust the volume (0.0 to 1.0)
engine.setProperty('rate', 150)  # Adjust the rate for natural pauses

# Initial chat history for the assistant
history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

while True:
    try:
        # Prompt the user to speak or type a question
        print("Speak or type your question/command:")
        
        # Use microphone as the audio source
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise

            # Listen to the user's input
            audio = r.listen(source)

            # Recognize speech using Google's API
            text = r.recognize_google(audio)
            print("You said:", text)  # Print the recognized text

        # Add user's speech to chat history
        history.append({"role": "user", "content": text})

        # Get AI assistant's response using OpenAI's chat model
        completion = client.chat.completions.create(
            model="local-model",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response_text = chunk.choices[0].delta.content

                # Print the assistant's response
                print("Assistant:", response_text)

                # Speak the entire response with reduced pauses between words
                engine.say(response_text)
                engine.runAndWait()

                # Store the entire response in the new_message content
                new_message["content"] = response_text

        # Add assistant's response to chat history
        history.append(new_message)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Unknown error occurred")

    except Exception as e:
        print(f"An error occurred: {e}")
