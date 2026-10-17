from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

load_dotenv()

client = genai.Client()
chat = client.chats.create(model = "gemini-3.8-flash")
config = GenerateContentConfig(
    system_instruction = """
    You are a tutor for college students first learning Java. You will assist with learning programming concepts.
    Do not give away answers, even if the user asks for them.
    Do not be verbose, unless the user asks for a deep explanation.
    """
)

while True:
    question = input("Send a message to the tutor: ")
    response = chat.send_message(question, config = config)

    print(response.text)