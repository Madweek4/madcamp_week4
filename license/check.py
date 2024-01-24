from tkinter import *
from TTS import TextToSpeech
import os
import sys
import hashlib
import uuid
import requests

tk = Tk()
tts = TextToSpeech()

def get_mac_address():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = ''.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return mac

hash_object = hashlib.sha256(get_mac_address().encode())
hex_dig = hash_object.hexdigest()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 아이디 라벨과 입력 필드
Label(tk, text="아이디", font = 50).pack()
id_entry = Entry(tk, font=70)
id_entry.pack()
id_entry.focus_set()

# 비밀번호 라벨과 입력 필드
Label(tk, text="비밀번호", font = 50).pack()
password_entry = Entry(tk, show="*", font=70)  # 입력하는 내용이 보이지 않도록 설정
password_entry.pack()

# 버튼3을 미리 정의합니다.
button3 = Button(tk,text='라이센스 발급받기',bg='#FFDB00',font=15,width=70,height=14)

def getLicense():
    url = 'http://192.249.31.17:5000/certify'
    data = {'id': id_entry.get(), 'password': password_entry.get(), 'mac': hex_dig}
    response = requests.post(url, data=data)
    rst = response.json()
    print(rst)
    
    if rst['success']:
        tts.start_speech(resource_path("getfinish.mp3"))
        button3.configure(text="발급완료")
    else: 
        tts.start_speech(resource_path("error.mp3"))

# command로 버튼 클릭 시 동작할 함수 지정, bg로 색상지정, width,height로 각각 넓이 높이 지정
button3.configure(command=getLicense)
button3.pack(padx=10, pady=10)

# 창 이름 설정
tk.title('BlindHelperLicense') 

if __name__ == "__main__":
    print(hex_dig)
    tts.start_speech(resource_path("get.mp3"))
    tk.mainloop()
