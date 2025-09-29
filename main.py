import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schena_write_file
from functions.call_function import call_function

def main():
    is_verbose = False

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
    

    available_functions = types.Tool(
                function_declarations = [
                        schema_get_files_info,
                        schema_get_file_content,
                        schema_run_python_file,
                        schena_write_file,
                    ]
            )
    
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files
        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

    response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages, 
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt, tools = [available_functions]
                ), 
    )
    
    function_calls = response.function_calls

    if len(args)>2:
        if "--verbose" in args:
            is_verbose = True
            print(f"User prompt: {user_prompt}\n")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")

    if len(function_calls) > 0:
        print("==========Function=Calls=============")
        for function_call_part in function_calls:
            function_call_result = call_function(function_call_part, is_verbose)
            if is_verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                raise Exception("There was not returned any response")



if __name__ == "__main__":
    main()
