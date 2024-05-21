from flask import Flask, render_template, request, send_from_directory, jsonify
import aiml
import random
import re
import os
import speech_recognition as sr

app = Flask(__name__)
app.secret_key = os.urandom(24)

bot_name = "E-bot"
user_info = {}

# Load AIML Kernel
k = aiml.Kernel()
k.learn("std-startup.xml")

# Default responses
DEFAULT_RESPONSES = [
    "I'm sorry, I didn't understand your query. Please try again.",
    "Hmm... I'm not sure I follow. Can you rephrase your question?",
    "I'm not programmed to answer that. Let's stick to questions about LDRP Institute of Technology and Research."
]
EMPTY_RESPONSES = [
    "Please ask me something!",
    "Feel free to ask me anything about LDRP Institute of Technology and Research!",
    "I'm here to help. Ask me a question!"
]

# Preprocess user input
def preprocess_input(input_text):
    if input_text:
        input_text = input_text.lower()
        input_text = re.sub(r'[^\w\s]', '', input_text)  # Remove punctuation
        return input_text.strip()
    return ""

# Handle user input and generate bot responses
def handle_input(user_input):
    global user_info
    
    user_input = preprocess_input(user_input)
    
    if "my attendance is" in user_input:
        attendance = re.search(r'\d+', user_input)
        if attendance:
            user_info['attendance'] = attendance.group()
            return f"Got it! Your attendance has been updated to {attendance.group()} percent."
    
    elif "my attendance" in user_input:
        if 'attendance' in user_info:
            return f"Your attendance is {user_info['attendance']} percent."
        else:
            return "I'm sorry, I don't have your attendance information."
    
    elif "my spi is" in user_input:
        spi = re.search(r'\d+(\.\d+)?', user_input)
        if spi:
            user_info['spi'] = spi.group()
            return f"Got it! Your SPI has been updated to {spi.group()}."
    
    elif "what is my spi" in user_input:
        if 'spi' in user_info:
            return f"Your Semester Performance Index (SPI) is {user_info['spi']}."
        else:
            return "I'm sorry, I don't have your SPI information."
    
    elif "ldrp image" in user_input:
        # If the user asks for the LDRP image, return the image HTML tag
        return f"<img src='https://www.collegebatch.com/static/clg-gallery/ldrp-institute-of-technology-research-gandhinagar-272344.jpg' width='300' height='200' />"
    
    else:
        response = k.respond(user_input)
        if not response:
            return random.choice(DEFAULT_RESPONSES)
        elif response.startswith("<img"):
            # If response contains image tag, return the image URL
            image_match = re.search(r'<img src="([^"]+)"', response)
            if image_match:
                return image_match.group(1)
            else:
                return "I'm sorry, I couldn't fetch the image."
        elif response == 'No match':
            return random.choice(DEFAULT_RESPONSES)
        return response

# Flask routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')
    bot_response = handle_input(user_input)
    return bot_response

@app.route('/voice', methods=['POST'])
def handle_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        voice_input = r.recognize_google(audio)
        bot_response = handle_input(voice_input)
        return jsonify({'response': bot_response})
    except sr.UnknownValueError:
        return jsonify({'error': "Sorry, I couldn't understand what you said."})
    except sr.RequestError as e:
        return jsonify({'error': f"Could not request results from Google Speech Recognition service; {e}"})


if __name__ == "__main__":
    app.run()
