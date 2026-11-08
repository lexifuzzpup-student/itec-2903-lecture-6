from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

with open("./data/concoction327.png", "rb") as file:
    image_bytes = file.read()

response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = [
        types.Part.from_bytes(data = image_bytes, mime_type = "image/png"),
        "What is this a picture of?"
    ]
)

print(response.text)