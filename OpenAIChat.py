import openai

class OpenAIChat:
    def __init__(self):
        openai.api_key = "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"
        self.model = "gpt-4"

    def get_completion(self, prompt, temperature=0):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message["content"]




  