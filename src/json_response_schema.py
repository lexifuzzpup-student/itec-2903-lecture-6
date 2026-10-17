from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel

class Recipe(BaseModel):
    recipe_name: str
    ingredients: list[str]
    instructions: list[str]

load_dotenv()

client = genai.Client()
response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = """
    I have asparagus, garlic, butter, and a large array of spices.
    Make me a recipe that uses these ingredients.
    """,
    config = GenerateContentConfig(
        system_instruction = "Use metric measurements",
        response_mime_type = "application/json",
        response_schema = Recipe
    )
)

print(response.text)

parsed = response.parsed
print(parsed)

print(parsed.recipe_name)

for ingredient in parsed.ingredients:
    print(ingredient)
for instruction in parsed.instructions:
    print(instruction)