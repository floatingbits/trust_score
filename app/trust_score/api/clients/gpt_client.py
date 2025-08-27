# clients/gpt_client.py
import openai
import re


class GptClient:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def run_prompt(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4.1",
            #model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def strip_json_wrapper(self, content: str) -> str:
        pattern = r'^```json\s*(.*?)\s*```$'
        cleaned_string = re.sub(pattern, r'\1', content, flags=re.DOTALL)
        return cleaned_string.strip()
