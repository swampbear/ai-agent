import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    args = sys.argv
    if len(args) < 2:
        print("Failed to generate respones: no prompt were given")
        os._exit(1)
    user_prompt = sys.argv[1] 
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
                model='gemini-2.0-flash-001', contents=messages
                )
    if len(args)>2:
        if args[2] == "--verbose":
            print(f"User prompt: {user_prompt}")
            print("Prompt tokens:",response.usage_metadata.prompt_token_count)
            print("Response tokens:",response.usage_metadata.candidates_token_count)
    print(response.text)
    
if __name__ == "__main__":
    main()
