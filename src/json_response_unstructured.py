from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

load_dotenv()

client = genai.Client()
response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = """
    I have asparagus, garlic, butter, and a large array of spices.
    Make me a recipe that uses these ingredients.
    """,
    config = GenerateContentConfig(
        response_mime_type = "application/json"
    )
)

print(response.text)