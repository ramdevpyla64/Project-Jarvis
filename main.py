import speech_recognition as sr
import webbrowser
import pyttsx3
from googleapiclient.discovery import build
from openai import OpenAI
import re
import time
import os
from dotenv import load_dotenv
load_dotenv() 
api_key1 = os.getenv("API_KEY")
api_key2 = os.getenv("API_KEY1")
r=sr.Recognizer()
client = OpenAI(api_key=F"{api_key1}")
engine=pyttsx3.init()
engine.setProperty('rate',150)
count=0
chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
def ai(command):
    global count, chat_history
    if count!=10:
        try:
            chat_history.append({"role": "user", "content": command})
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=chat_history
            )
            reply = response.choices[0].message.content
            chat_history.append({"role": "assistant", "content": reply})
            count+=1
            return reply
        except Exception as e:
            return f"OpenAI API error: {str(e)}"
    elif count==10:
        count=0
        chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
        return "chat is overflowed ,lets start a new chat , i am resetting the previous chat"
def get_youtube_link(query):
    try:
        youtube = build("youtube", "v3", developerKey=f"{api_key2}")
        request = youtube.search().list(
            part="snippet",
            q=query,
            maxResults=1,
            type="video"
        )
        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"YouTube API Error: {e}")
        return None

def command(word):
    if "open google" in word:
        webbrowser.open("https://google.com")
        speak("opening google")
    elif "open youtube" in word:
        webbrowser.open("https://youtube.com")
        speak("opening youtube")
    elif "open github" in word:
        webbrowser.open("https://github.com")
        speak("opening github")
    elif "open stack overflow" in word:
        webbrowser.open("https://stackoverflow.com")
        speak("opening stack overflow")
    elif "what is your name" in word:
        speak("My name is Jarvis")
    elif "how are you" in word:
        speak("I am just a bunch of code, but I'm functioning properly")
    elif word.startswith("play"):
        yt_query = word.replace("play","")
        link = get_youtube_link(yt_query)
        if link:
            webbrowser.open(link)
            speak(f"Playing {yt_query}")
        else:
            speak("Sorry, I couldn't find that song.")
    else:
        content=ai(word)
        print("ai:",content)
        clean_content = re.sub(r'[^\x00-\x7F]+', ' ', content)
        speak(clean_content)
def speak(text):
    engine.say(text)
    engine.runAndWait()
if __name__=="__main__":
    speak("jarvis initialized")
    while True:
        try:
            with sr.Microphone() as source:
                audio=r.listen(source)
                word=r.recognize_google(audio)
            if word.lower()=="jarvis":
                speak("yes")
                while True:
                    print("listening")
                    with sr.Microphone() as source:
                        audio=r.listen(source)
                        word=r.recognize_google(audio)
                        print(word)
                    if word=="exit":
                        speak("signing off!jarvis")
                        time.sleep(0.5)
                        break
                    elif word=="":
                        pass
                    else:
                        command(word.lower())
                break        
            else:
                pass     
        except:
            pass