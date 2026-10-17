from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown

load_dotenv()

client = genai.Client()
chat = client.chats.create(
    model = "gemini-3.8-flash",
    config = GenerateContentConfig(
        system_instruction = "Respond in a single sentence."
    )
)

while True:
    prompt = input("Send a message: ")
    response = chat.send_message(prompt)

    # token count increases with chat history, which increases price
    print(response.usage_metadata)
    rich.print(Markdown(response.text))