from tkinter import *
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os
from bs4 import BeautifulSoup
import requests
import time
import winsound
from threading import *


BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica"
FONT_BOLD = "Helvetica 13 bold"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

class VoiceAssistant:
    
    def __init__(self, botName):
        self._botName = botName
        
        self.window = Tk()
        self._setup_main_window(botName)
        self.r = sr.Recognizer()

        self.alarmWin = False
        self.weatherWin
        self.hour = False
        self.minute = False
        self.second= False

        self._commandsArray = [
            "what is your name",
            "who are you",
            "what can you do",
            "search the web",
            "what time is it",
            "what is the weather",
            "open youtube",
            "open gmail",
            "find location",
            "set an alarm"
        ]
        
    def run(self):
        self.window.mainloop()

    def _setup_main_window(self, botName):
        self.window.title(f"{botName} - Voice Assistant")
        self.window.resizable(width=False, height=False)
        self.window.config(bg=BG_COLOR, padx=6, pady=10)
        self.window.geometry('370x320+500+80')

        # text widget
        self.text_widget = Text(self.window, width=20, height=0, bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT, 8), padx=5, pady=5)
        self.text_widget.place(relheight=0.820, relwidth=1)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scrollbar
        scrollbar = Scrollbar(self.text_widget, bg=BG_COLOR)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        # bottons container
        bottom_label = Label(self.window, bg="#000000", height=47)
        bottom_label.place(relwidth=1, rely=0.840)

        # buttons
        commandList_btn = Button(bottom_label, text="Commands", font=FONT_BOLD, width=20, bg="grey", command=self.commadList)
        commandList_btn.place(relwidth=0.30, relheight=0.06, rely=0.008, relx=0.011)
        
        speak_btn = Button(bottom_label, text="Speak", font=FONT_BOLD, width=20, bg="teal", fg="#000000",  command=self.yakan)
        
        speak_btn.place(relx=0.33, rely=0.008, relheight=0.06, relwidth=0.66)

        self.visual("Hello user, welcome!", self._botName)
        self.visual('Try saying, "What can you do?"', self._botName)

    def yakan(self):
        with sr.Microphone() as source:
            audio = self.r.listen(source)


        try:
            myText = self.r.recognize_google(audio)
            myText = myText.lower()
            
            self._insert_message(myText, "You")


            if myText == self._commandsArray[0] or myText == "what's your name":
                self.visual(f'My name is {self._botName}', self._botName)
                
            elif myText == self._commandsArray[1]:
                self.visual(f'I am {self._botName}, your voice assistant.', self._botName)

            elif myText == self._commandsArray[2]:
                self.visual("I can do anything within my ability", self._botName)

            elif myText == self._commandsArray[3]:
                self.searchWeb()

            elif myText == self._commandsArray[4]:
                self.visual(f'The time is {datetime.today().strftime("%I:%M %p")}', self._botName)

            elif myText == self._commandsArray[5]:
                self.weatherWin()

            elif myText == self._commandsArray[6]:
                self.openYoutube()

            elif myText == self._commandsArray[7]:
                self.openGmail()

            elif myText == self._commandsArray[8]:
                self.findLocation()

            elif myText == "set an alarm":
                self.invokeAlarm()
                
            else:
                self.visual("I’m sorry, I don’t get that. Can you say it differently?", self._botName)

        except sr.UnknownValueError:
            self.visual("Unable to recognize speech", self._botName)

    def createFolder(self):
        try: 
            os.mkdir('D:/') 
        except OSError as error: 
            print(error) 

    def findLocation(self):
        self.locationWin = Toplevel(self.window)
        self.locationWin.title("Find Location")
        self.locationWin.config(bg='#ffffff', padx=20, pady=20)
        self.locationWin.geometry('360x120+100+150')
        self.locationWin.config(bg=BG_COLOR, padx=10, pady=10)
        self.locationWin.resizable(False, False)

        label = Label(self.locationWin, text="Enter address", bg=BG_COLOR, fg="#ffffff", font=("Poppins", 10))
        label.grid()

        entryVar = Entry(self.locationWin, width=41, bg="grey", fg="#ffffff")
        entryVar.place(relwidth=1, rely=0.30)

                        
        btn = Button(self.locationWin, text="Find", font=FONT_BOLD, width=20, bg="teal", fg="#000000", padx=20, pady=2, command=lambda: self.getLocation(entryVar.get()))
        btn.place(relwidth=1, rely=0.62)

    def getLocation(self, address):
        address = ''.join(address.split())
        os.system(f"start \"\" http://maps.google.co.uk/maps?q={address}")

            
    def invokeAlarm(self):
        self.alarmWin = Toplevel(self.window)
        self.alarmWin.title("Alarm")
        self.alarmWin.config(bg='#ffffff', padx=20, pady=20)
        self.alarmWin.geometry('280x150+100+150')
        self.alarmWin.config(bg=BG_COLOR, padx=10, pady=10)
        self.alarmWin.resizable(False, False)

        Label(self.alarmWin,text="Set Alarm", bg=BG_COLOR, fg="#ffffff", font=("Poppins", 10)).pack(pady=10)

        frame = Frame(self.alarmWin,)
        frame.pack()

        self.hour = StringVar(self.alarmWin)
        hours = ('00', '01', '02', '03', '04', '05', '06', '07',
                 '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17', '18', '19', '20', '21', '22', '23', '24'
                )
        self.hour.set(hours[0])
         
        hrs = OptionMenu(frame, self.hour, *hours)
        hrs.pack(side=LEFT)
         
        self.minute = StringVar(self.alarmWin)
        minutes = ('00', '01', '02', '03', '04', '05', '06', '07',
                   '08', '09', '10', '11', '12', '13', '14', '15',
                   '16', '17', '18', '19', '20', '21', '22', '23',
                   '24', '25', '26', '27', '28', '29', '30', '31',
                   '32', '33', '34', '35', '36', '37', '38', '39',
                   '40', '41', '42', '43', '44', '45', '46', '47',
                   '48', '49', '50', '51', '52', '53', '54', '55',
                   '56', '57', '58', '59', '60')
        self.minute.set(minutes[0])
         
        mins = OptionMenu(frame, self.minute, *minutes)
        mins.pack(side=LEFT)
         
        self.second = StringVar(self.alarmWin)
        seconds = ('00', '01', '02', '03', '04', '05', '06', '07',
                   '08', '09', '10', '11', '12', '13', '14', '15',
                   '16', '17', '18', '19', '20', '21', '22', '23',
                   '24', '25', '26', '27', '28', '29', '30', '31',
                   '32', '33', '34', '35', '36', '37', '38', '39',
                   '40', '41', '42', '43', '44', '45', '46', '47',
                   '48', '49', '50', '51', '52', '53', '54', '55',
                   '56', '57', '58', '59', '60')
        self.second.set(seconds[0])
         
        secs = OptionMenu(frame, self.second, *seconds)

        secs.pack(side=LEFT)

        
         
        Button(self.alarmWin,text="Set Alarm", font=FONT_BOLD, width=20, bg="teal", fg="#000000", padx=20, pady=2, command=self.Threading).pack(pady=10)


    def Threading(self):
        t1=Thread(target=self.setAlarm)
        t1.start()

    def setAlarm(self):
        if f"{self.hour.get()}:{self.minute.get()}:{self.second.get()}" == "00:00:00":
            return

        self.alarmWin.destroy()
        self._insert_message(f"You set an alarm at: {self.hour.get()}:{self.minute.get()}:{self.second.get()}s", self._botName)

        while True:
            set_alarm_time = f"{self.hour.get()}:{self.minute.get()}:{self.second.get()}"
            time.sleep(1)
     
            current_time = datetime.now().strftime("%H:%M:%S")
     
            if current_time == set_alarm_time:
                self._insert_message("Alarm ringing... ", self._botName)
                winsound.PlaySound("sound.wav",winsound.SND_ASYNC)
        

    def weatherWin(self):
        self.weatherWin = Toplevel(self.window)
        self.weatherWin.title("Weather")
        self.weatherWin.config(bg='#ffffff', padx=20, pady=20)
        self.weatherWin.geometry('360x120+100+150')
        self.weatherWin.config(bg=BG_COLOR, padx=10, pady=10)
        self.weatherWin.resizable(False, False)

        label = Label(self.weatherWin, text="Enter City", bg=BG_COLOR, fg="#ffffff", font=("Poppins", 10))
        label.grid()

        entryVar = Entry(self.weatherWin, width=41, bg="grey", fg="#ffffff")
        entryVar.place(relwidth=1, rely=0.30)
                        
        btn = Button(self.weatherWin, text="Get weather", font=FONT_BOLD, width=20, bg="teal", fg="#000000", padx=20, pady=2, command=lambda: self.getWeather(entryVar.get()))
        btn.place(relwidth=1, rely=0.62)

        
    def getWeather(self, city):
        if city == "":
            return

        self.weatherWin.destroy()
        
        try:
            city = city + "weather"
            city = city.replace(" ", "+")
            res = requests.get(
                f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
            self.visual("Searching", self._botName)
            
            soup = BeautifulSoup(res.text, 'html.parser')
            location = soup.select('#wob_loc')[0].getText().strip()
            time = soup.select('#wob_dts')[0].getText().strip()
            info = soup.select('#wob_dc')[0].getText().strip()
            weather = soup.select('#wob_tm')[0].getText().strip()

            self.visual(f"""
 Weather at {location}
 {time}
 {info}
 {weather}°C       
            """, self._botName)

        except Exception as e:
            self.visual("City not found, please try again.", self._botName)
            

    def searchWeb(self):
        os.system("start \"\" https://google.com")
        self.visual("Google is open", self._botName)
        self.visual("what do you want to search?", self._botName)

    def visual(self, msg, sender):
        self._insert_message(msg, sender)
        self.speakText(msg)
        
        
    def speakText(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def openYoutube(self):
        os.system("start \"\" https://youtube.com")
        self.visual("Youtube opened.", self._botName)

    def openGmail(self):
        os.system("start \"\" https://gmail.com")
        self.visual("Gmail opened.", self._botName)
        

    def commadList(self):
        msg = f"""
Commands: 
 - {self._commandsArray[0]}?
 - {self._commandsArray[1]}?
 - {self._commandsArray[2]}?
 - {self._commandsArray[3]}
 - {self._commandsArray[4]}?
 - {self._commandsArray[5]}?
 - {self._commandsArray[6]}
 - {self._commandsArray[7]}
 - {self._commandsArray[8]}
  - {self._commandsArray[9]}


"""
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        msg1 = f"{sender}: {msg}\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
             
        
if __name__ == "__main__":
    app = VoiceAssistant("Vianus")
    app.run()
