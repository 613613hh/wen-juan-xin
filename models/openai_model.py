
import config
from models.model_interface import ModelInterface
from openai import OpenAI

class OpenAIModel(ModelInterface):
    def get_response(self, messages):
        client = OpenAI(
            api_key=config.OPENAI_KEY,
            base_url=config.BASEURL
        )
        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        response = completion.choices[0].message.content
        return response

