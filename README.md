# BlindHelper

MadCamp Week4 1분반 

- 시각 장애인들이 현재 사용하고 있는 프로그램은 이미지를 설명할 때 이미지의 대체 텍스트(alt)를 설명한다.
- 이 대체 텍스트는 제대로 되어 있지 않은 웹페이지가 많고, 웹이 아닌 곳에서는 이미지를 읽어올 수 없다는 단점이 있다.
- 이 단점을 보완하기 위해 구글 클라우드의 이미지 분석 api를 사용하여 이미지 자체를 분석하여 설명해주는 프로그램을 기획하였다.
- 시각 장애인의 90%는 색깔을 구분할 수 있기에 웹과 실행파일 gui를 만들 때 노란색을 주로 사용하였다.

### a. 개발 팀원

- 김수환 - KAIST 전산학부(수리과학과) 22학번
- 이형진 - KAIST 전산학부 22학번

### b. 개발환경

- Language: JavaScript, HTML, CSS, Python
- Server: Flask
- DataBase: MongoDB
- IDE: Visual Studio code 

### c. WEB

## Page 0 - HOME/LOGIN/SIGNUP


***Major features***

- 웹 설명...

### d. EXE PROGRAM

## 1. License Program

<img width="961" alt="chrome_cSLdJfE6SP" src="https://github.com/Madweek4/madcamp_week4/assets/155048947/eed9dbf0-919e-4d4a-8a6b-d238023b4251">

***Major features***

- BlindHelper 프로그램은 유료로 기획하였기에 무단 복제를 막고자 라이센스를 발급하는 실행파일을 만들었다.
- 회원가입 후 결제를 한 사용자에게는 본래 라이센스 프로그램을 다운로드할 수 있게 하였고, 결제를 하지 않으면 데모판을 다운로드 할 수 있게 웹을 구성하였다.
- 프로그램을 실행하면 아이디와 비밀번호를 입력할 수 있는 gui가 뜨고 노란색 버튼을 누르면 라이센스가 발급된다. 데모판의 경우에는 해당 라이센스는 3일 후 사용할 수 없다.
- 최대한 마우스를 사용하지 않도록 탭을 사용하여 입력할 수 있는 곳을 지정할 수 있게 하였고, 음성으로 설명을 해주도록 설계했다.
- tkinter 파이썬 라이브러리로 gui를 구성하였다.
- uuid 라이브러리를 통해 사용자 컴퓨터의 mac 주소를 받아와 hashlib으로 암호화하여 이를 라이센스 코드로 사용하였다.
- pyinstaller로 실행파일을 만들었다.
- ```
  #실행파일을 만드는 코드(cmd)
  pyinstaller --noconsole --onefile -n="BlindHelperLicense" --add-data "service_secret_key.json;." --add-data "error.mp3;." --add-data "get.mp3;." --add-data "getfinish.mp3;." check.py

  #exe가 제대로 실행되기 위한 상대 주소 사용 함수(py)
  def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
  ```

### e. DIRECTORY STRUCTURE
```
#라이센스 프로그램
📦test
 ┣ 📂__pycache__
 ┃ ┗ 📜TTS.cpython-310.pyc
 ┣ 📜check.py 
 ┣ 📜error.mp3
 ┣ 📜get.mp3
 ┣ 📜getfinish.mp3
 ┣ 📜service_secret_key.json
 ┗ 📜TTS.py
```
```
#BlindHelper 프로그램
📦newexe
 ┣ 📂__pycache__
 ┃ ┣ 📜ImageLabeler.cpython-310.pyc
 ┃ ┣ 📜ImageLabeler.cpython-38.pyc
 ┃ ┣ 📜NaverOCR.cpython-310.pyc
 ┃ ┣ 📜NaverOCR.cpython-38.pyc
 ┃ ┣ 📜OpenAIChat.cpython-310.pyc
 ┃ ┣ 📜OpenAIChat.cpython-38.pyc
 ┃ ┣ 📜screenshot.cpython-310.pyc
 ┃ ┣ 📜screenshot.cpython-38.pyc
 ┃ ┣ 📜TTS.cpython-310.pyc
 ┃ ┗ 📜TTS.cpython-38.pyc
 ┣ 📜BlindHelper.spec
 ┣ 📜cancel.mp3
 ┣ 📜capturecancel.mp3
 ┣ 📜capturestart.mp3
 ┣ 📜dragtest.py
 ┣ 📜exefolder.ico
 ┣ 📜fullscreenshot.png
 ┣ 📜hash.mp3
 ┣ 📜hash.txt
 ┣ 📜ImageLabeler.py
 ┣ 📜main.py
 ┣ 📜NaverOCR.py
 ┣ 📜notext.mp3
 ┣ 📜OpenAIChat.py
 ┣ 📜output.jpg
 ┣ 📜programexit.mp3
 ┣ 📜programstart.mp3
 ┣ 📜screenshot.png
 ┣ 📜screenshot.py
 ┣ 📜service_secret_key.json
 ┣ 📜summary.mp3
 ┣ 📜sumstart.mp3
 ┣ 📜test.mp3
 ┣ 📜test.py
 ┣ 📜text.mp3
 ┣ 📜TTS.py
 ┣ 📜ttt.py
 ┗ 📜wait.mp3
```

  

