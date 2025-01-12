from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import pyttsx3

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 180)

def google_search(command):
    reg_ex = re.search('search google for (.*)', command)
    
    if reg_ex:
        subgoogle = reg_ex.group(1)
        speak("Okay sir!")
        speak(f"Searching for {subgoogle}")
        
        service = Service('C://Users//Prathamesh Devkate//Downloads//JARVIS-master//driver//chromedriver.exe')
        driver = webdriver.Chrome(service=service)
        
        driver.get('https://www.google.com')
        
        search = driver.find_element(By.NAME, 'q')
        search.send_keys(subgoogle)
        search.send_keys(Keys.RETURN)
        
        # Keep the browser open
        input("Press Enter to close the browser...")
        driver.quit()  # Manually close after Enter
    else:
        speak("Sorry, I didn't catch what you wanted to search for on Google.")

