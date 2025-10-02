import os
from re import A
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function, available_functions
from prompts import system_prompt
from config import MAX_ITER


def main():
    verbose = "--verbose" in sys.argv

    args = sys.argv
    user_prompt = sys.argv[1] 
    if len(args) < 2:
        print("Failed to generate respones: no prompt were given")
        os._exit(1)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    iter = 0
    while True:
        iter += 1
        if iter > MAX_ITER:
            print(f"maximum iterations reached")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error: error occured while generating respones {e}")

def generate_content(client, messages, verbose):
            response= client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt, tools = [available_functions]            
                )
            )
            for candidate in response.candidates:
                    messages.append(candidate.content)
            if verbose:
                print("Prompt tokens: ")
            if not response.function_calls:
                return response.text
   
            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)

                if not function_call_result.parts or not function_call_result.parts[0].function_response:
                    raise Exception("empty function call result")
                
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])
            if not function_responses:
                raise Exception("no function responses generated") 





    
    
if __name__ == "__main__":
    main()
