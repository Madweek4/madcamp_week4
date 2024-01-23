from screenshot import Screenshot
from TTS import TextToSpeech
from ImageLabeler import ImageLabeler
from OpenAIChat import OpenAIChat
from pykospacing import Spacing
import keyboard, time
import os
import sys
import uuid
import hashlib

def get_mac_address():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = ''.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return mac

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

screenshot = Screenshot()
tts = TextToSpeech()
cont = True
result = ""

def captureStart():
    global result
    tts.start_speech(resource_path('capturestart.mp3'))
    #여기서 추출된 배열 받아와야 함. 지금은 하드코딩.
    isCaptured = Screenshot().start_capture() #드래그 한 영역 좌표
    print("여기임?")
    textPosition = ImageLabeler('fullscreenshot.png')
    if isCaptured == None:
        tts.start_speech(resource_path('capturecancel.mp3'))
        return
    full_position = textPosition.detect_document_text() #전체 글자, 좌표
    result_lst = []
    for text, coordinate in full_position:
        x1 = coordinate[0][0]
        x2 = coordinate[1][0]
        y1 = coordinate[0][1]
        y2 = coordinate[2][1]

        if (isCaptured[0] <= x1 <= isCaptured[0]+isCaptured[2] or isCaptured[0] <= x2 <= isCaptured[0]+isCaptured[2]):
            if (isCaptured[1] <= y1 <= isCaptured[1]+isCaptured[3] or isCaptured[1] <= y2 <= isCaptured[1]+isCaptured[3]):
                result_lst.append(text)
    
    result = ''.join(result_lst)
    spacing = Spacing()
    result = spacing(result)

    print(result)


    if result != "":
        tts.synthesize_speech(result, resource_path('text.mp3'))
    else:
        tts.start_speech(resource_path('notext.mp3'))
        

def summary():
    global result
    tts.start_speech(resource_path('sumstart.mp3'))
    labeler = ImageLabeler("screenshot.png")
    result2 = labeler.label_image()
    lst = result2.split(',')
    print(lst)
    if len(lst) == 0:
        print("여기")
        prompt = "화면에서 분석한 텍스트 정보가 있습니다. 화면에서 추출한 텍스트 정보는 다음과 같습니다: [{}]. 화면 텍스트 정보를 요약해서 설명해줘. 문맥 상 이상한 단어들을 제외하고, 분석 결과를 말하지 말고 요약 결과만 말해줘.".format(result)
    elif result == "":
        print("여기2")
        prompt = "화면에서 분석한 이미지 정보가 있습니다. 이미지 분석 결과, 다음 키워드들이 도출되었습니다: [{}]. 사진에 대해서 간단하게 설명해줘. 분석 결과를 말하지 말고 요약 결과만 말해줘.".format(result2)
    else:
        print("저기")
        prompt = "화면에서 분석한 이미지와 텍스트 정보가 있습니다. 이미지 분석 결과, 다음 키워드들이 도출되었습니다: [{}]. 또한 화면에서 추출한 텍스트 정보는 다음과 같습니다: [{}]. 사진에 대해서 간단하게 설명해줘. 그 후에 텍스트 정보를 요약해서 설명해줘. 문맥 상 이상한 단어들을 제외하고, 분석 결과를 말하지 말고 요약 결과만 말해줘.".format(result2, result)
    
    chat = OpenAIChat()
    response = chat.get_completion(prompt)

    print("요약: " + response)
    tts.synthesize_speech(response, resource_path('summary.mp3'))

def cancel():
    tts.stop_speech
    tts.start_speech(resource_path('cancel.mp3'))


def main():
    print("main 실행")
    keyboard.add_hotkey('ctrl+alt+q', lambda : captureStart())
    keyboard.add_hotkey('ctrl+alt+w', lambda: cancel())
    keyboard.add_hotkey('ctrl+alt+e', tts.pause_speech)
    keyboard.add_hotkey('ctrl+alt+r', tts.resume_speech)
    keyboard.add_hotkey('ctrl+alt+d', lambda : (tts.start_speech(resource_path('programexit.mp3')), time.sleep(2), globals().update({'cont': False})))
    keyboard.add_hotkey('ctrl+alt+f', lambda : summary())

if __name__ == "__main__":
    hash_object = hashlib.sha256(get_mac_address().encode())
    hex_dig = hash_object.hexdigest()
    f = open(resource_path("hash.txt"), 'r')
    if (f.read() == str(hex_dig)):
        tts.start_speech(resource_path('programstart.mp3'))
        main()
        while cont:
            pass
    else:
        tts.start_speech(resource_path('hash.mp3'))