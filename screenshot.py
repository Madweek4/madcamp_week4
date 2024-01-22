import tkinter as tk
import pyautogui
from PIL import ImageTk
from TTS import TextToSpeech
import os
import sys

class Screenshot:
    def __init__(self):
        # 캡처 영역의 시작점과 끝점
        self.start_x, self.start_y, self.end_x, self.end_y = 0, 0, 0, 0
        self.rectangle = None
        self.root = None
        self.canvas = None
        self.capture_result = None

    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        self.end_x, self.end_y = event.x, event.y
        if self.rectangle:
            self.canvas.delete(self.rectangle)
        self.rectangle = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, fill='yellow', stipple='gray50')

    def on_release(self, event):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        wait = os.path.join(base_path, "wait.mp3")
        tts = TextToSpeech()
        tts.start_speech(wait)
        self.end_x, self.end_y = event.x, event.y
        if self.rectangle:
            self.canvas.delete(self.rectangle)  # 캡처 전에 노란색 사각형 삭제
        self.root.after(100, self.capture_screenshot)  # 1초 후에 스크린샷을 캡처

    def capture_screenshot(self):
        self.canvas.delete("all")  # 모든 요소를 캔버스에서 삭제 (전체 스크린샷 삭제)
        screen_width, screen_height = pyautogui.size()  # 화면의 크기를 가져옴
        left = max(0, min(self.start_x, self.end_x))  # 왼쪽 경계 확인
        top = max(0, min(self.start_y, self.end_y))  # 위쪽 경계 확인
        width = min(screen_width - left, abs(self.start_x - self.end_x))  # 오른쪽 경계 확인
        height = min(screen_height - top, abs(self.start_y - self.end_y))  # 아래쪽 경계 확인
        if width > 0 and height > 0:  # 너비와 높이가 0보다 크면 스크린샷을 찍음
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot.save('screenshot.png')
            print("return True at screenshot.py")
            self.capture_result = (left, top, width, height)
            self.root.destroy()
            return
        self.root.destroy()
        print("return False at screenshot.py")
        self.capture_result = None

    def start_capture(self):
        if self.root is None:
            self.root = tk.Tk()
            screen_width, screen_height = pyautogui.size()
            screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
            screenshot.save('fullscreenshot.png')
            self.background = ImageTk.PhotoImage(screenshot)
            self.root.attributes('-fullscreen', True)
            self.root.attributes('-topmost', True)
            self.root.attributes('-alpha', 1)
            self.root.bind('<Button-1>', self.on_click)
            self.root.bind('<B1-Motion>', self.on_drag)
            self.root.bind('<ButtonRelease-1>', self.on_release)
            self.canvas = tk.Canvas(self.root)
            self.canvas.create_image(0, 0, image=self.background, anchor='nw')
            self.canvas.pack(fill='both', expand=True)
            self.root.mainloop()
            self.root = None
            return self.capture_result
