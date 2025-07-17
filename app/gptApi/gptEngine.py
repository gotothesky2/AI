from openai import OpenAI
import os
from dotenv import load_dotenv
#연결 성공
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GPT_API_KEY")
)
response=client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "너는 간단한 안내 메시지를 출력하는 챗봇이야."},
        {"role": "user", "content": "연결 테스트용으로 한 줄만 응답해줘."}
    ],
    max_tokens=50,
    temperature=0.5,
)
print(response)




