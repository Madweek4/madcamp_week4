import io
import os, cv2
from google.cloud import vision
from TTS import TextToSpeech
from pykospacing import Spacing

class ImageLabeler:
    def __init__(self, image_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service_secret_key.json'
        self.client = vision.ImageAnnotatorClient()
        self.image_path = os.path.abspath(image_path)

    def label_image(self):
        with io.open(self.image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations

        result = ''
        check = 0
        for label in labels:
            if label.score >= 0.70 and label.description != "Font":
                check = 1
                result += f"{label.description}, "

        if check == 0:
            result += ""
        
        return result
    
    def detect_document_text(self):
        result = ""
        with io.open(self.image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = self.client.document_text_detection(image=image)
        

        # 응답에서 텍스트 덩어리 정보 추출
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        word_conf = word.confidence

                        # 경계 상자 정보 추출
                        vertices = [(vertex.x, vertex.y)
                                    for vertex in word.bounding_box.vertices]
                        
                        print(f"Word: {word_text}, {word_conf},Bounding Box: {vertices}")
                        

i = ImageLabeler(r'C:\Users\KIMSUWHAN\Desktop\test_object\test6.png')
result = i.detect_document_text()

"""
spacing = Spacing()
kospacing_sent = spacing(result)
print(kospacing_sent)

tts = TextToSpeech()
tts.synthesize_speech(kospacing_sent, "test.mp3")
"""


