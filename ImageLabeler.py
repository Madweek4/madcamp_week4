import io
import os
from google.cloud import vision

import os

class ImageLabeler:
    def __init__(self, image_path):
        current_path = os.path.dirname(os.path.realpath(__file__))
        credentials_path = os.path.join(current_path, 'service_secret_key.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
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
        
        

        result = []
        # 응답에서 텍스트 덩어리 정보 추출
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        if word.confidence < 0.9:
                            continue
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])

                        # 경계 상자 정보 추출
                        vertices = [(vertex.x, vertex.y)
                                    for vertex in word.bounding_box.vertices]
                        
                        result.append((word_text, vertices))
        
        return result
                        
