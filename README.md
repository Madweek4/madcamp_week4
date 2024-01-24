# BlindHelper

MadCamp Week4 1분반 

- 시각 장애인들이 현재 사용하고 있는 프로그램은 이미지를 설명할 때 이미지의 대체 텍스트(alt)를 설명한다.
- 이 대체 텍스트는 제대로 되어 있지 않은 웹페이지가 많고, 웹이 아닌 곳에서는 이미지를 읽어올 수 없다는 단점이 있다.
- 이 단점을 보완하기 위해 구글 클라우드의 이미지 분석 api를 사용하여 이미지 자체를 분석하여 설명해주는 프로그램을 기획하였다.
- 시각 장애인의 90%는 색깔을 구분할 수 있기에 웹과 실행파일 gui를 만들 때 노란색을 주로 사용하였다.
- 이 프로그램은 시각 장애 중 시력 및 시야 장애를 가진 분들을 타겟으로 하였고, 인터넷을 사용할 때 특정 부분에 대한 설명을 해줄 수 있도록 구성하였다.

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
- 최대한 마우스를 사용하지 않도록 탭을 사용하여 입력할 수 있는 곳을 지정할 수 있게 하였고, 음성(구글 클라우드 TTS api)으로 설명을 해주도록 설계했다. 
- tkinter 파이썬 라이브러리로 gui를 구성하였다.
- uuid 라이브러리를 통해 사용자 컴퓨터의 mac 주소를 받아와 hashlib으로 암호화하여 이를 라이센스 코드로 사용하였다.
- pyinstaller로 실행파일을 만들었다.
-
  ```
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

## 2. BlindHelper Program

<img width="961" alt="chrome_cSLdJfE6SP" src="https://github.com/Madweek4/madcamp_week4/assets/155048947/eed9dbf0-919e-4d4a-8a6b-d238023b4251">

***Major features***

- BlindHelper 프로그램은 실행한 후에 따로 ui가 존재하지 않고 음성으로만 설명이 되도록 만들었다.
- 단축키들로 기능을 구현할 수 있다. "ctrl+alt"로 모든 단축키가 시작된다.
-
  ```
  ctrl+alt+q: 캡처 시작
  ctrl+alt+w: 음성 설명 취소
  ctrl+alt+e: 음성 설명 중지
  ctrl+alt+r: 음성 설명 다시재생(중지된 부분부터)
  ctrl+alt+d: 프로그램 종료
  ctrl+alt+f: 요약 시작
  ```
- 캡처가 시작되면 현재 화면에서 드래그하여 캡처 영역을 정할 수 있다. 드래그 영역은 노란색으로 표시하여 어느 부분을 캡처하는 지 인지할 수 있게 하였다.
- 구글 클라우드 api를 통해 글자를 인식할 때 그룹별로 인식하여 그리드 형태의 사이트에서도 문맥에 맞게 글자를 인식할 수 있게 하였다.
- 인식된 글자는 pykospacing 라이브러리를 통해 띄어쓰기를 적용하여 TTS가 읽을 때 자연스럽게 읽도록 구성했다.
- '''pip install git+https://github.com/haven-jeon/PyKoSpacing.git'''
- 요약 기능이 시작되면 우선 구글 클라우드 api를 통해 캡처 이미지에서 이미지 컨텐츠들의 키워드들을 추출한다.
- 이미지 키워드들을 추출할 때 confidence가 70% 이상인 키워드만 추출하여 정확도를 높였다.
- 해당 키워드와 텍스트를 이용하여 chatgpt api가 요약한 후 이를 TTS로 출력한다.
- 프롬프트를 구성할 때 텍스트만 있는 경우, 이미지만 있는 경우, 둘 다 있는 경우 세 가지로 나누어 프롬프트를 구성하여 자연스럽게 설명할 수 있도록 설계했다.
- 이 프로그램도 license 프로그램과 마찬가지로 상대 주소를 사용하고, pyinstaller로 exe 파일을 만들었다.


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

  

