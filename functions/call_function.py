from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
                function_declarations = [
                        schema_get_files_info,
                        schema_get_file_content,
                        schema_run_python_file,
                        schema_write_file,
                    ]
    )



def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args

    function_result = ""
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    try:
        if function_call_part.name == "get_file_content":
            function_result = get_file_content("./calculator", file_path=args["file_path"])
        elif function_call_part.name == "get_files_info":
            function_result = get_files_info("./calculator", directory=args["directory"])
        elif function_call_part.name == "write_file":
            function_result = write_file("./calculator", file_path=args["file_path"], content=args["content"])
        elif function_call_part.name == "run_python_file":
            function_result = run_python_file("./calculator", file_path=args["file_path"])
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result},
                    )
                ],
            )

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )

    except Exception:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    
