import speech_recognition as sr
import whisper
import wave
import torch
import pyaudio
import pyautogui
import pygame

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = whisper.load_model('tiny').to(device)

last_transcription = ""
typing_mode = False

command_phrases = {
    "double click": ["double click", "double-click"],
    "right click": ["right click", "right-click"],
    "single click": ["select", "click"],
    "scroll up": ["scroll up", "scroll-up", "scrol up"],
    "scroll down": ["scroll down", "scroll-down", "scrol down"],
    "scroll mode on": ["scroll mode on", "scroll mod on"],
    "scroll mode off": ["scroll mode off", "scroll mod off"],
    "typing mode on": ["typing mode on", "typing mod on"],
    "typing mode off": ["typing mode off", "typing mod off", "typing mood of", "typing mode of"],
    "delete": ["delete"]
}

pygame.mixer.init()

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def record_audio(filename):
    r = sr.Recognizer()
    format = pyaudio.paInt16
    channels = 1
    rate = 44100  
    with sr.Microphone() as source:
        # play_sound('./sounds/Listening.mp3')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(pyaudio.get_sample_size(format))
        wav_file.setframerate(rate)
        wav_file.writeframes(audio.frame_data)

def deaf():
    while True:
        global typing_mode
        filename = "my_recording.wav"
        record_audio(filename)
        result = model.transcribe(filename, fp16=device == 'cuda')
        transcription = result["text"].lower().strip()
        print(f"Transcription: {transcription}")
        
        command_executed = False 

        for command, phrases in command_phrases.items():
            if any(phrase in transcription for phrase in phrases):
                if not typing_mode:
                    if command == "double click":
                        pyautogui.doubleClick()
                        play_sound('./sounds/double.mp3')
                    elif command == "right click":
                        pyautogui.rightClick()
                        play_sound('./sounds/right_click.mp3')
                    elif command == "single click":
                        pyautogui.click()
                        play_sound('./sounds/item_selected.mp3')
                    elif command == "scroll up":
                        pyautogui.scroll(200)
                        play_sound('./sounds/scrolled_up.mp3')
                    elif command == "scroll down":
                        pyautogui.scroll(-200)
                        play_sound('./sounds/scrolled_down.mp3')
                    elif command == "scroll mode on":
                        play_sound('./sounds/Scroll_on.mp3')
                    elif command == "scroll mode off":
                        play_sound('./sounds/Scroll_off.mp3')
                    elif command == "typing mode on":
                        typing_mode = True
                        play_sound('./sounds/typing_onn.mp3')
                        print("Typing mode ON")
                    command_executed = True
                    break
                else:
                    if command == "typing mode off":
                        typing_mode = False
                        play_sound('./sounds/typing_offf.mp3')
                    elif command == "delete":
                        if last_transcription:
                            pyautogui.write('\b' * len(last_transcription))
                            last_transcription = ""
                            print("Deleted last word")
                        else:
                            print("There is nothing to be deleted")
                    else:
                        pyautogui.write(transcription + " ")
                        last_transcription = transcription
                    command_executed = True
                    break

        if typing_mode and not command_executed:
            pyautogui.write(transcription + " ")
            last_transcription = transcription
            print(f"Typed: {transcription}")

  
