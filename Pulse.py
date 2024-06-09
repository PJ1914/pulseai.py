import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import cv2
import requests
from bs4 import BeautifulSoup
import random
import openai
from googleapiclient.discovery import build

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to speak the given audio
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to greet the user based on the time
def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Pulse, your personal AI assistant. How may I help you?")

# Function to take user's voice command and convert it to text
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 2
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Can you please repeat?")
        return "none"
    except sr.RequestError:
        print("Sorry, I'm unable to access the Google API at the moment.")
        return "none"
    return query.lower()

# Function to provide personalized responses
def get_personal_info(query):
    if 'my name' in query:
        speak("Your name is Pranay.")
    elif 'my birthday' in query:
        speak("Your birthday is on 19th May 2005.")
    elif 'my phone number' in query:
        speak("Your phone number is 9381301429.")
    elif 'my email' in query:
        speak("Your email is pranay.jumbarthi1905@gmail.com.")

# Function to calculate the aspect ratio of a face
def calculate_aspect_ratio(face):
    x, y, w, h = face
    return float(w) / h

# Function for face recognition
def face_recognition():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            aspect_ratio = calculate_aspect_ratio((x, y, w, h))
            cv2.putText(frame, f'Aspect Ratio: {aspect_ratio:.2f}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        # Check if the window is closed
        if cv2.getWindowProperty('Face Recognition', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to allow the assistant to learn new things
def learn_new_thing():
    speak("What would you like me to learn?")
    new_info = take_command()
    if new_info != 'none':
        speak("Thank you for teaching me!")

# Function to get weather forecast
def get_weather(location):
    api_key = "your_openweather_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        condition = data['weather'][0]['description']
        speak(f"The current temperature in {location} is {temp}°C and the weather condition is {condition}.")
    else:
        speak("I couldn't retrieve the weather information.")

# Function to get Gemini cryptocurrency data
def get_gemini_data():
    url = "https://api.gemini.com/v1/pubticker/btcusd"  # Example endpoint
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        speak(f"The current price of Bitcoin is {data['last']} USD.")
    else:
        speak("I couldn't fetch the data from Gemini.")

# Function to get Google search results
def google_search(query):
    api_key = "your_google_api_key"
    search_engine_id = "your_search_engine_id"
    service = build("customsearch", "v1", developerKey=api_key)
    result = service.cse().list(q=query, cx=search_engine_id).execute()
    items = result.get('items', [])
    if items:
        speak(f"Here are the top results for {query}:")
        for item in items[:3]:  # Show top 3 results
            speak(f"Title: {item['title']}, Link: {item['link']}")
    else:
        speak("No results found.")

# Function to get response from GPT-4
def get_gpt4_response(prompt):
    openai.api_key = "your_openai_api_key"
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )
    message = response.choices[0].text.strip()
    speak(message)

# Function to set reminders
def set_reminder(task, time):
    speak(f"Reminder set for {task} at {time}.")

# Function to play music
def play_music():
    speak("Playing music...")

# Function to tell jokes
def tell_joke():
    jokes = ["Why don't scientists trust atoms? Because they make up everything!",
             "I told my wife she was drawing her eyebrows too high. She looked surprised.",
             "Why did the scarecrow win an award? Because he was outstanding in his field!",
             "Parallel lines have so much in common. It's a shame they'll never meet."]
    joke = random.choice(jokes)
    speak(joke)

# Function to translate text
def translate_text(text, source_lang, target_lang):
    speak("Translation feature coming soon!")

# Function to perform calculations
def calculate(expression):
    try:
        result = eval(expression)
        speak(f"The result of {expression} is {result}.")
    except:
        speak("Sorry, I couldn't perform the calculation.")

# Function to get news updates
def get_news():
    speak("News updates coming soon!")

# Function to get traffic updates
def get_traffic(location):
    speak("Traffic updates coming soon!")

# Function to find restaurants
def find_restaurants(location, cuisine):
    speak("Restaurant search feature coming soon!")

# Function to get sports updates
def get_sports_updates():
    speak("Sports updates coming soon!")

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()

        # Logic for executing tasks
        if 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open my youtube channel' in query:
            webbrowser.open("https://www.youtube.com/@univarsalmusicbyj.p1719/videos")
        elif 'personal info' in query:
            get_personal_info(query)
        elif 'face recognition' in query:
            face_recognition()
        elif 'learn new thing' in query:
            learn_new_thing()
        elif any(word in query for word in ['goodbye', 'bye', 'shut up', 'shut down']):
            speak("Goodbye!")
            break
        elif 'weather in' in query:
            location = query.split('in')[-1].strip()
            get_weather(location)
        elif 'bitcoin price' in query:
            get_gemini_data()
        elif 'google search' in query:
            query = query.replace('google search', '')
            google_search(query)
        elif 'ask gpt' in query:
            query = query.replace('ask gpt', '')
            get_gpt4_response(query)
        elif 'set reminder' in query:
            set_reminder("Meeting", "3:00 PM")
        elif 'play music' in query:
            play_music()
        elif 'joke' in query:
            tell_joke()
        elif 'translate' in query:
            translate_text("Hello", "English", "Spanish")
        elif 'calculate' in query:
            calculate("2 + 2")
        elif 'news' in query:
            get_news()
        elif 'traffic' in query:
            get_traffic("New York")
        elif 'find restaurant' in query:
            find_restaurants("New York", "Italian")
        elif 'sports updates' in query:
            get_sports_updates()
