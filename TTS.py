import os
import threading
import keyboard
from google.cloud import texttospeech
import pygame
import threading

class TextToSpeech:

    def __init__(self, language_code="ko-KR", gender=texttospeech.SsmlVoiceGender.FEMALE):
        current_path = os.path.dirname(os.path.realpath(__file__))
        credentials_path = os.path.join(current_path, 'service_secret_key.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.stop_audio = False
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=gender)
        self.audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        keyboard.add_hotkey('ctrl+alt+s', self.pause_speech)  # Set 'q' as the hotkey
        keyboard.add_hotkey('ctrl+alt+d', self.resume_speech)  

    def start_speech(self, file):
        self.stop_speech()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        play_thread = threading.Thread(target=self.play_audio)
        play_thread.start()

    def synthesize_speech(self, text, output_file):
        if text == "": return
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(input=synthesis_input, voice=self.voice, audio_config=self.audio_config)
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        play_thread = threading.Thread(target=self.play_audio)
        play_thread.start()

    def play_audio(self):
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        

    def pause_speech(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.pause()

    def resume_speech(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()
            
    def stop_speech(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()


#tts = TextToSpeech()
#tts.synthesize_speech("취소", "cancel.mp3") #여기다가 문자열
        
