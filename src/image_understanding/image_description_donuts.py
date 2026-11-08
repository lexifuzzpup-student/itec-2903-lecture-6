from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

class Donut(BaseModel):
    flavor: str     # model should guess what the flavor is
    frosting_color: str
    sprinkles_colors: list[str]

client = genai.Client()

with open("./data/donuts_final.png", "rb") as file:
    image_bytes = file.read()

response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = [
        types.Part.from_bytes(data = image_bytes, mime_type = "image/png"),
        "What donuts are in this picture?"
    ],
    config = types.GenerateContentConfig(
        system_instruction = """
            Identify all of the donuts in the picture.
            Assume the flavor based on popular donut types.
            Use english names for colors.
        """,
        response_mime_type = "application/json",
        response_schema = list[Donut]   # some syntax that means a list of the donut class
    )
)

print(response.parsed)