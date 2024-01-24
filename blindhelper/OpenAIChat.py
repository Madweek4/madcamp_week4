import openai

class OpenAIChat:
    def __init__(self):
        openai.api_key = "이거 openai api 키 넣기..."
        self.model = "gpt-4"

    def get_completion(self, prompt, temperature=0):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message["content"]




  