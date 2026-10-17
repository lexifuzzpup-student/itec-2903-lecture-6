from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()
response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = """
    We're a starting business wanting to set up an
    application to share events with people local to
    Minneapolis. What information should we collect
    from our users?
    """
)

print(response.text)