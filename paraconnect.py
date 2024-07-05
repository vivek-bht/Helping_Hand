import subprocess
import google.generativeai as genai
import pyttsx3
import whisper
import torch
import wave
from datetime import date
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyaudio
import pyjokes
import ctypes
import pyautogui
import socket
from ecapture import ecapture as ec

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 50)
engine.setProperty('rate', 150)
flag = True
last_transcription = ""
typing_mode = False

command_phrases = { "double click": ["double click", "double-click"],
"right click": ["right click", "right-click"],
"single click": ["select", "single click", "left click"],
"scroll up": ["scroll up", "scroll-up", "scrol up"],
"scroll down": ["scroll down", "scroll-down", "scrol down"],
"scroll mode on": ["scroll mode on", "scroll mod on"],
"scroll mode off": ["scroll mode off", "scroll mod off"],
"typing mode on": ["typing mode on", "typing mod on"],
"typing mode off": ["typing mode off", "typing mod off", "typing mood of", "typing mode of"],
"delete": ["delete"],
"stop": ["stop listening"],
"start": ["start listening"]
}

recognizer = sr.Recognizer()
microphone = sr.Microphone()
def speak(audio):
		engine.say(audio)
		engine.runAndWait()
def append2log(text): 
		global today
		fname = 'chatlog-' + today + '.txt'
		with open(fname, "a") as f:
			f.write(text + "\n")

model = genai.GenerativeModel('gemini-pro')    
def takeCommand():
		with microphone as source:
			if flag:
				speak("Listening")
			recognizer.pause_threshold = 1
			audio = recognizer.listen(source)

		try:
			print("Recognize")
			query = recognizer.recognize_google(audio, language ='en-in')
			print(f"User said: {query}\n")

		except Exception as e:
			print(e) 
			print("Unable to Recognize your voice.") 
			return "None"
		return query

genai.configure(api_key=" AIzaSyCOKq-61EDI758wCeGT8RfHppW4sUFTEzs")

today = str(date.today())
def record_audio(filename):
	format = pyaudio.paInt16
	channels = 1
	rate = 44100
	with microphone as source:
		if flag:
			speak("listening")
		recognizer.adjust_for_ambient_noise(source)
		audio = recognizer.listen(source)

	with wave.open(filename, 'wb') as wav_file:
		wav_file.setnchannels(channels)
		wav_file.setsampwidth(pyaudio.get_sample_size(format))
		wav_file.setframerate(rate)
		wav_file.writeframes(audio.frame_data)

class voice_assistant():
	def __init__(self, shared_dict, lock):
		self.shared_dict = shared_dict
		self.lock = lock
		self.append2log = append2log()

	def wishMe():
		hour = int(datetime.datetime.now().hour)
		if hour>= 0 and hour<12:
			speak("Good Morning!")
		elif hour>= 12 and hour<18:
			speak("Good Afternoon!") 
		else:
			speak("Good Evening!") 

	wishMe()
	speak("Welcome to Para Connect")
	speak("How can I help you?")

	def internet(host = "8.8.8.8", port = 53, timeout = 3):
		try:
			socket.setdefaulttimeout(timeout)
			socket.socket(socket.AF_INET,
                 socket.SOCK_STREAM).connect((host,port))
			return True
		except socket.error as ex:
			return False

	def close_voice(self,shared_dict):
			query = takeCommand().lower()
			if "voice mode off" in query:
				
				self.shared_dict["voice_mode": False]
				exit()
			else :
				self.shared_dict ["voice_mode":True]

	def offline():
		device = 'cuda' if torch.cuda.is_available() else 'cpu'
		modelOffline = whisper.load_model('tiny').to(device) 
		global flag
		global typing_mode
		global last_transcription
		while True:
			filename = "my_recording.wav"
			record_audio(filename)
			result = modelOffline.transcribe(filename, fp16=device == 'cuda')
			transcription = result["text"].lower().strip()
			print(f"transcription by whisper: {transcription}")
			command_executed = False
			for command, phrases in command_phrases.items():
				if any(phrase in transcription for phrase in phrases):
					if not typing_mode:
						if command == "double click":
							pyautogui.doubleClick()
							speak('double click performed!')
						elif command == "right click":
							pyautogui.rightClick()
							speak("right click performed!")
						elif command == "start":
							flag = True
							speak("Initiating Listening Cue")
						elif command == "stop":
							flag = False
						elif (command == "single click") or (command == "left click"):
							pyautogui.click()
							speak("Item selected!")
						elif command == "scroll up":
							pyautogui.scroll(400)
							speak("scrolled up!")
						elif command == "scroll down":
							pyautogui.scroll(-400)
							speak("scrolled down!")
						elif command == "typing mode on":
							typing_mode = True    
							speak("Typing mode is now ON! Anything you speak will be typed wherever you place your cursor!")    
						command_executed = True                    

					else: 
						if command == "typing mode off":    
							command_executed = True      
							speak("Typing mode is now off! You are back to giving commands!")
							typing_mode = False
						elif command == "delete":
							command_executed = True
							if last_transcription:
								pyautogui.write('\b'*(len(last_transcription) + 1))
								last_transcription = ""
								print("Deleted the last transcription!")
							else:
								print("There is nothing to be deleted")
		
			if typing_mode and not command_executed:
				pyautogui.write(transcription + " ")
				last_transcription = transcription
				print(f"Typed: {transcription}")			
	def main():
		global talk, today, model 
		recognizer.dynamic_energy_threshold=False
		recognizer.energy_threshold = 400 
		sleeping = True

		while True: 
			with microphone as source1:
				recognizer.adjust_for_ambient_noise(source1, duration= 0.5)
				try:
					if flag:
						speak("listening")
					audio = recognizer.listen(source1, timeout = 10, phrase_time_limit = 15)
					text = recognizer.recognize_google(audio)
					if sleeping == True:
						if "gemini" in text.lower():
							request = text.lower().split("gemini")[1]
							sleeping = False
							append2log(f"_"*40)
							talk = []
							today = str(date.today()) 
       
							if len(request) < 5:
								speak("Hi, there, how can I help?")
								append2log(f"AI: Hi, there, how can I help? \n")
								continue
						else:
							continue
					else:
						request = text.lower()
						if "that's all" in request:
							append2log(f"You: {request}\n")
							speak("Bye Now")
							append2log(f"AI: Bye now. \n")
							print('Bye now')
							break
   
						if "gemini" in request:
							request = request.split("gemini")[1]
       
					append2log(f"You: {request}\n ")
					print(f"You: {request}\n")
					talk.append({'role':'user', 'parts':[request]})
					response = model.generate_content(talk,stream = True,
                                      generation_config = genai.types.GenerationConfig
                                      (max_output_tokens = 50))
    
					for chunk in response:
						print(chunk.text, end = '')
						speak(chunk.text.replace("*",""))
     
					print('\n')
					talk.append({'role':'model', 'parts': [response.text]})
    
					append2log(f"AI: {response.txt}\n")
				except Exception as e:
					continue
 
	if internet():
		global flag
		global typing_mode
		global last_transcription
		while True:
			command_executed = False
			query = takeCommand().lower()
			if not typing_mode:
				if 'wikipedia' in query:
					speak('Searching Wikipedia...')
					query = query.replace("wikipedia", "")
					try:
						results = wikipedia.summary(query, sentences = 3)
						speak("According to Wikipedia")
						print(results)
						speak(results)
					except Exception as e:
						print("An error occured:",e)
						speak("Sorry, I couldn't find any information on wikipedia for your query")

				elif 'open youtube' in query:
					speak("Opening Youtube for you")
					webbrowser.open("youtube.com")

				elif 'open google' in query:
					speak("Opening Google for you")
					webbrowser.open("google.com")

				elif 'open stackoverflow' in query:
					speak("Opening Stack Overflow for you. Happy coding!")
					webbrowser.open("stackoverflow.com") 

				elif 'voice mode off' in query:
					speak("Turning voice mode off! Happy to help anytime!")
					exit()
				
				elif 'joke' in query:
					speak(pyjokes.get_joke())

				elif 'search' in query or 'play' in query:
					query = query.replace("search", "") 
					query = query.replace("play", "")		 
					webbrowser.open(query) 

				elif 'power point' in query:
					speak("opening Power Point presentation")
					power = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
					os.startfile(power)

				elif 'change the background' in query:
					ctypes.windll.user32.SystemParametersInfoW(20, 
														0, 
														"Location of wallpaper",
														0)
					speak("Background changed successfully")

				elif 'sleep' in query:
						speak("locking the device")
						ctypes.windll.user32.LockWorkStation()

				elif 'system shutdown' in query:
						speak("Your system is on its way to shut down")
						subprocess.call('shutdown / p /f')
				elif 'stop listening' in query:
						flag = False
				elif 'start listening' in query:
						flag = True
						speak("Initiating Listening Cue")

				elif "camera" in query or "take a photo" in query:
					ec.capture(0, " Camera ", "img.jpg")
					speak("Picture Captured. You look gorgeous!")

				elif "restart" in query:
					speak("Restarting your system for you!")
					subprocess.call(["shutdown", "/r"])

				elif "wikipedia" in query:
					webbrowser.open("wikipedia.com")
					speak("Opening wikipedia.com")
		
				elif "double click" in query:
					pyautogui.doubleClick()
					speak("double click performed!")
			
				elif "right click" in query:
					pyautogui.rightClick()
					speak("right click performed!")
	
				elif "click" in query:
					pyautogui.click()
					speak("Item selected!")
	
				elif "scroll up" in query:
					pyautogui.scroll(400)
					speak("scrolled up!")
	
				elif "scroll down" in query:
					pyautogui.scroll(-400)
					speak("scrolled down!")

				elif "open ai assistant"in query:
					speak("Opening Gemini AI")
					main()
				elif "typing mode on" in query:
					speak("typing mode is now ON! Anything you speak will be typed wherever you place your cursor")
					typing_mode = True
				command_executed = True
			else: 
				if "typing mode off" in query or "typing mod off" in query or "typing mode of" in query or "typing mod of" in query:          
					typing_mode = False
					speak("Typing mode is now off! You are back to giving commands!")
					command_executed = True
				elif "delete" in query:
					command_executed = True
					if last_transcription:
						pyautogui.write('\b'*(len(last_transcription) + 1))
						last_transcription = ""
						speak("Deleted the last transcription!")
					else:
						speak("There is nothing to be deleted")
				
			if typing_mode and not command_executed:
				pyautogui.write(query + " ", 0.15)
				last_transcription = query
				print(f"Typed: {query}")	
	else:
		offline()
	