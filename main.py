import os
from dotenv import load_dotenv
from google import genai
import sys


if len(sys.argv) < 2:
    print("Missing parameter. Scripts expexts prompt to work you knoow...")
    sys.exit(1)
elif len(sys.argv) > 2:
    print("Too many parameters you know. We expect one string as a prompt")
    sys.exit(1)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]

test_response = client.models.generate_content(model="gemini-2.0-flash-001", contents=user_prompt)

print(f"Prompt tokens: {test_response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {test_response.usage_metadata.candidates_token_count}")

print(test_response.text)