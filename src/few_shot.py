from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()
response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = """
    We're a starting business that has a platform where
    people can share events with other Minneapolis locals.
    What are some ways to advertise our service?
    We've put up posters in public places a few months ago
    and it seemed to work relatively well.
    We've also posted online, but it didn't get much traction.
    Frequently, we find people joining the platform after
    being invited by another.
    """
)

print(response.text)