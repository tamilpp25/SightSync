import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)    # Speed of speech (words per minute)
engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

# Convert text to speech and output it
text = "Hello, how are you today?"
engine.say(text)
engine.runAndWait()
