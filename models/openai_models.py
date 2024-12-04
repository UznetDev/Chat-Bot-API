from openai import OpenAI
from data.config import OPENAI_API_KEY


class Models:
    def __init__(self):
        pass
        # self.client = OpenAI(api_key=OPENAI_API_KEY)

    def get_answer(self, prompt, model: str, api_key):
        try:
            self.client = OpenAI(api_key=api_key)
            response = self.client.chat.completions.create(
                model=model,
                messages=prompt
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def create_promts(self, promt: str, prompt_history):
        try:
            promts = []
            for i in prompt_history:
                p = {"role": i["role"], "content": i["content"]}
                promts.append(p)

            promts.append({"role": "user", "content": promt})
            return promts
        except Exception as e:
            return f"Error: {str(e)}"


            prompt_history.append({"role": "user", "content": prompt})
            return prompt_history
        except Exception as e:
            return f"Error: {str(e)}"