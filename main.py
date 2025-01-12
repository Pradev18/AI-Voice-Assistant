import subprocess
from Jarvis import JarvisAssistant
import re
import os
import random
import pprint
import datetime
import requests
import sys
import urllib.parse  
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
import yfinance as yf
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis.features.gui import Ui_MainWindow
from Jarvis.config import config


obj = JarvisAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

EMAIL_DIC = {
    'recipient': 'pradev2002@gmail.com'
    
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"] ###
# =======================================================================================================================================================


def speak(text):
    obj.tts(text)


app_id = config.wolframalpha_id


def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
        return None
    

    
def startup():
    # speak("Initializing Jarvis")
    # speak("Starting all systems applications")
    # speak("Installing and checking all drivers")
    # speak("Caliberating and examining all the core processors")
    # speak("Checking the internet connection")
    # speak("Wait a moment sir")
    # speak("All drivers are up and running")
    # speak("All systems have been activated")
    # speak("Now I am online")
    # hour = int(datetime.datetime.now().hour)
    # if hour>=0 and hour<=12:
    #     speak("Good Morning")
    # elif hour>12 and hour<18:
    #     speak("Good afternoon")
    # else:
    #     speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Jarvis. Online and ready sir. Please tell me how may I help you")
    

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        startup()
        

        while True:
            command = obj.mic_input()

            if re.search('date', command):
                date = obj.tell_me_date()
                print(date)
                speak(date)

            elif "time" in command:
                time_c = obj.tell_time()
                print(time_c)
                speak(f"Sir the time is {time_c}")

            elif re.search('launch', command):
                dict_app = {
                    'chrome': 'C://Program Files//Google//Chrome//Application',
                    'notepad': 'C://Windows//System32//notepad.exe',
                    'calculator': 'C://Windows//System32//calc.exe',
                    'paint': 'C://Windows//System32//mspaint.exe',
                    'explorer': 'C://Windows//explorer.exe',
                    'word': 'C://Program Files//Microsoft Office//root//Office16//WINWORD.EXE',
                    'excel': 'C://Program Files//Microsoft Office//root//Office16//EXCEL.EXE',
                    'powerpoint': 'C://Program Files//Microsoft Office//root//Office16//POWERPNT.EXE',
                    'vlc': 'C://Program Files//VideoLAN//VLC//vlc.exe',
                    'spotify': 'C://Users//Prathamesh Devkate//AppData//Local//Microsoft//WindowsApps//Spotify.exe',
                    'pycharm': 'C://Program Files//JetBrains//PyCharm Community Edition 2021.1//bin//pycharm64.exe',
                    'edge': 'C://Program Files (x86)//Microsoft//Edge//Application//msedge.exe'
                    # Add more default applications and their paths here
                }

                app_name = command.split(' ', 1)[1].lower()  # Get app name from command
                path = dict_app.get(app_name)

                if path is None:
                    speak(f"I don't have {app_name} in my database. Could you provide the application path?")
                    path = obj.mic_input()  # Get the path from user voice input

                if os.path.exists(path):
                    speak(f'Launching {app_name} for you, sir!')
                    subprocess.Popen(path)  # Launch the app using the path
                else:
                    speak(f'Sorry, I could not find an executable at {path}. Please try again.')

            elif command in GREETINGS: 
                speak(random.choice(GREETINGS_RES))

            elif re.search('open', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                speak(f'Alright sir !! Opening {domain}')
                print(open_result)
            


            elif re.search('weather', command): #
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                print(weather_res)
                speak(weather_res)

            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = obj.tell_me(topic)
                    print(wiki_res)
                    speak(wiki_res)
                else:
                    speak(
                        "Sorry sir. I couldn't load your query from my database. Please try again")

            elif "buzzing" in command or "news" in command or "headlines" in command:
                news_res = obj.news()
                speak('Source: The Times Of India')
                speak('Todays Headlines are..')
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res)-2:
                        break
                speak('These were the top headlines, Have a nice day Sir!!..')

            elif 'search google for' in command:
                obj.search_anything_google(command)
            
            elif "play music" in command or "hit some music" in command: ####
                music_dir = "C:\\Users\\Prathamesh Devkate\\Music"
                songs = os.listdir(music_dir)
                for song in songs:
                    os.startfile(os.path.join(music_dir, song))

            

            elif "stock" in command or "stock price" in command or "predict stock" in command:
                try:
                    speak("Which company's stock price would you like to know?")
                    company = obj.mic_input().lower()  # Convert the input to lowercase for easier matching
                    
                    # Map common company names to ticker symbols (expand this as needed)
                    company_tickers = {
                        "microsoft": "MSFT",
                        "apple": "AAPL",
                        "google": "GOOGL",
                        "amazon": "AMZN",
                        # Add more mappings here as needed
                    }
                    
                    if company in company_tickers:
                        ticker = company_tickers[company]
                    else:
                        speak("Sorry, I couldn't recognize that company. Please try again with a valid company name.")
                        return
                    
                    speak(f"Fetching the stock data for {ticker}. Please wait...")
                    
                    # Fetch stock data using yfinance
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period="1d") 
                    
                    if hist.empty:
                        speak(f"Sorry, I couldn't find stock data for {ticker}. Please try with a valid ticker symbol.")
                    else:
                        # Check if 'regularMarketPrice' exists in stock.info
                        if 'regularMarketPrice' in stock.info:
                            current_price = stock.info['regularMarketPrice']
                            speak(f"The current stock price of {ticker} is {current_price} dollars.")
                            print(f"{ticker}: Current price is {current_price}")
                        else:
                            speak(f"Sorry, I couldn't fetch the current stock price for {ticker}.")
                            print(f"{ticker}: Current price not available.")
                        
                        # Simple prediction based on average of last 7 days
                        average_price = hist['Close'].mean()
                        speak(f"The predicted stock price based on the last 7 days average is {average_price:.2f} dollars.")
                        print(f"{ticker}: Predicted price (7-day average) is {average_price:.2f}")
                
                except Exception as e:
                    print("Error in stock predictor:", e)
                    speak("Sorry, I encountered an error while fetching the stock data. Please try again later.")


            elif "youtube" in command:
                split_command = command.split(' ')
                
                if len(split_command) > 1:  # Check if the command has more than one word
                    video = split_command[1]
                    speak(f"Okay sir, playing {video} on YouTube")
                    pywhatkit.playonyt(video)
                else:
                    speak("Please specify the video to play on YouTube")

            elif "email" in command or "send email" in command: #
                sender_email = config.email
                sender_password = config.email_password

                try:
                    speak("Whom do you want to email sir ?")
                    recipient = obj.mic_input()
                    receiver_email = EMAIL_DIC.get(recipient)
                    if receiver_email:

                        speak("What is the subject sir ?")
                        subject = obj.mic_input()
                        speak("What should I say?")
                        message = obj.mic_input()
                        msg = 'Subject: {}\n\n{}'.format(subject, message)
                        obj.send_mail(sender_email, sender_password,
                                      receiver_email, msg)
                        speak("Email has been successfully sent")
                        time.sleep(2)

                    else:
                        speak(
                            "I coudn't find the requested person's email in my database. Please try again with a different name")

                except:
                    speak("Sorry sir. Couldn't send your mail. Please try again")

            elif "calculate" in command:#
                question = command
                answer = computational_intelligence(question)
                speak(answer)
            
            elif "what is" in command or "who is" in command: #
                question = command
                answer = computational_intelligence(question)
                speak(answer)

            elif "what do i have" in command or "do i have plans" or "am i busy" in command:
                obj.google_calendar_events(command)

            if "make a note" in command or "write this down" in command or "remember this" in command:  #############
                speak("What would you like me to write down?")
                note_text = obj.mic_input()
                obj.take_note(note_text)
                speak("I've made a note of that")

            elif "close the note" in command or "close notepad" in command:
                speak("Okay sir, closing notepad")
                os.system("taskkill /f /im notepad++.exe")

            if "joke" in command:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif "system" in command:
                sys_info = obj.system_info()
                print(sys_info)
                speak(sys_info)

            elif "where is" in command: ###########
                place = command.split('where is ', 1)[1]
                current_loc, target_loc, distance = obj.location(place)
                city = target_loc.get('city', '')
                state = target_loc.get('state', '')
                country = target_loc.get('country', '')
                time.sleep(1)
                try:

                    if city:
                        res = f"{place} is in {state} state and country {country}. It is {distance} km away from your current location"
                        print(res)
                        speak(res)

                    else:
                        res = f"{state} is a state in {country}. It is {distance} km away from your current location"
                        print(res)
                        speak(res)

                except:
                    res = "Sorry sir, I couldn't get the co-ordinates of the location you requested. Please try again"
                    speak(res)

            elif "ip address" in command:
                ip = requests.get('https://api.ipify.org').text
                print(ip)
                speak(f"Your ip address is {ip}")

            elif "switch the window" in command or "switch window" in command: ###ask ques which window
                speak("Okay sir, Switching the window")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "where i am" in command or "current location" in command or "where am i" in command:
                try:
                    city, state, country = obj.my_location()
                    print(city, state, country)
                    speak(
                        f"You are currently in {city} city which is in {state} state and country {country}")
                except Exception as e:
                    speak(
                        "Sorry sir, I coundn't fetch your current location. Please try again")

            elif "take screenshot" in command or "take a screenshot" in command or "capture the screen" in command:
                speak("By what name do you want to save the screenshot?")
                name = obj.mic_input()
                speak("Alright sir, taking the screenshot")
                img = pyautogui.screenshot()
                name = f"{name}.png"
                img.save(name)
                speak("The screenshot has been successfully captured")



                try:
                    img = Image.open(name)
                    img.show()  # This opens the screenshot in the default viewer
                    speak("Here it is, sir")
                    time.sleep(2)  # Allows time to view the image
                except IOError:
                    speak("Sorry sir, I am unable to display the screenshot")


            elif "show me the screenshot" in command:
                try:
                    img = Image.open(name)
                    img.show()  # Display the previously taken screenshot
                    speak("Here is the screenshot, sir.")
                except IOError:
                    speak("Sorry sir, I couldn't find the screenshot.")

            elif "volume up" in command:
                try:
                    pyautogui.press("volumeup")  # Simulates pressing the volume up key
                    speak("Volume has been increased.")
                except Exception as e:
                    print("Error in volume control:", e)
                    speak("Sorry, I encountered an error while adjusting the volume.")

            elif "volume down" in command:
                try:
                    pyautogui.press("volumedown")  # Simulates pressing the volume down key
                    speak("Volume has been decreased.")
                except Exception as e:
                    print("Error in volume control:", e)
                    speak("Sorry, I encountered an error while adjusting the volume.")

            elif "hide all files" in command or "hide this folder" in command:
                os.system("attrib +h /s /d")
                speak("Sir, all the files in this folder are now hidden")

            elif "visible" in command or "make files visible" in command:
                os.system("attrib -h /s /d")
                speak("Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")

            # if "calculate" in command or "what is" in command:
            #     query = command
            #     answer = computational_0intelligence(query)
            #     speak(answer)

            

            elif "goodbye" in command or "offline" in command or "bye" in command:
                speak("Alright sir, going offline. It was nice working with you")
                sys.exit()


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    # def run(self):
    #     self.TaskExection
    def startTask(self):
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())