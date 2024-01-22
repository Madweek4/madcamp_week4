from ImageLabeler import ImageLabeler
from NaverOCR import NaverOCR
from OpenAIChat import OpenAIChat
from TTS import TextToSpeech

image_url = 'C:/Users/KIMSUWHAN/Desktop/test2.png'


labeler = ImageLabeler(image_url)
result1 = labeler.label_image()

naver_ocr = NaverOCR(image_url)
result2 = naver_ocr.infer_text()

chat = OpenAIChat()
prompt = "화면에서 분석한 이미지와 텍스트 정보가 있습니다. 이미지 분석 결과, 다음 키워드들이 도출되었습니다: [{}]. 또한 화면에서 추출한 텍스트 정보는 다음과 같습니다: [{}]. 만약에 이미지 키워드들이 Font면 사진에 대해서 설명하지 말고 화면 텍스트 정보를 요약해서 200자 이하로 설명해주고, 이미지 키워드들이 Font가 아니면 사진에 대해서 설명해 준 뒤 텍스트 정보를 200자 이하로 요약해서 설명해줘. 바로 본론부터 말해주고, 이미지 키워드를 설명할 때 영어말고 한국어로 말해줘".format(result1, result2)
response = chat.get_completion(prompt)

print("요약: " + response)
tts = TextToSpeech()
tts.synthesize_speech(response)

