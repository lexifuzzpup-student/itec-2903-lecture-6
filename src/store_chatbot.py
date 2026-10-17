from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
import sys

load_dotenv()

client = genai.Client()
chat = client.chats.create(model = "gemini-3.8-flash")

try:
    with open("./prompts/store_chatbot.txt", "r") as f:
        system_instruction = f.read()
except:
    print("Missing system prompt")
    sys.exit()

config = GenerateContentConfig(
    system_instruction = system_instruction
)

while True:
    question = input("> ")
    response = chat.send_message(question, config = config)

    print(response.text)