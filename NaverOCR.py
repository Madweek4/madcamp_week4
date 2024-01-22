import json
import base64
import requests

class NaverOCR:
    def __init__(self, image_path, url="https://d23dowdibb.apigw.ntruss.com/custom/v1/27812/a3cb7b5967b41db49458e91b82573331dba5737dbe79ae192b38963330512d57/general", secret_key="ZGtMVWxtaldRZGpEUnVXS01yRWdQbUhLT0RXb0h6cmE="):
        with open(image_path, "rb") as f:
            self.img = base64.b64encode(f.read())
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "X-OCR-SECRET": secret_key
        }
        self.data = {
            "version": "V1",
            "requestId": "sample_id",  # 요청을 구분하기 위한 ID, 사용자가 정의
            "timestamp": 0,  # 현재 시간값
            "images": [
                {
                    "name": "sample_image",
                    "format": "png",
                    "data": self.img.decode('utf-8')
                }
            ]
        }

    def infer_text(self):
        data = json.dumps(self.data)
        response = requests.post(self.url, data=data, headers=self.headers)
        res = json.loads(response.text)

        # "inferText" 값만 추출
        infer_texts = [field["inferText"] for field in res["images"][0]["fields"]]

        # 추출된 값 반환
        return ' '.join(infer_texts)
