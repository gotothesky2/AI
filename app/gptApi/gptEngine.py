
from openai import OpenAI
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
#연결 성공
load_dotenv()

class GptBase(ABC):
    model="gpt-4o"
    client = OpenAI(
    api_key=os.getenv("GPT_API_KEY")
    )
    @abstractmethod
    def __new__(cls, *args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def system_prompt()->str:
        """
        시스템 프롬프트 정의필수
        """
        pass

    @staticmethod
    @abstractmethod
    def user_prompt(*args, **kwargs)->str:
        """
        유저 프롬프트 정의필수
        """
        pass

    @classmethod
    def get_response(cls, *args, **kwargs):
        return cls.client.chat.completions.create(
            model=cls.model,
            messages=[
                {"role": "system", "content": cls.system_prompt()},
                {"role": "user", "content": cls.user_prompt(*args, **kwargs)},
            ],
            max_tokens=50,
            temperature=0.8,
        )






