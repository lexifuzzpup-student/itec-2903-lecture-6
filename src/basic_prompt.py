from dotenv import load_dotenv
from google import genai
import rich
from rich.markdown import Markdown

load_dotenv()

client = genai.Client()
response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = "What causes a shellfish allergy?"
)

print(response.usage_metadata)
rich.print(Markdown(response.text))