import os
from config import CHARACTER_LIMIT_GET_FILE_CONTENT
from google.genai import types

schema_get_file_content= types.FunctionDeclaration(
    name="get_file_content",
    description="Gives what file to read from, constrained to the working_directoryg",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
           "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    full_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(full_working_directory):
        return f'Error: cannot read "{file_path}" as it is outside the permitted working directroy'

    if not os.path.isfile(target_file):
        return f'Error: file not found or is not a regualr file: "{file_path}"'
    try:
        fd = os.open(target_file, os.O_RDONLY)
        with open(target_file) as f:
            content = f.read(CHARACTER_LIMIT_GET_FILE_CONTENT)
            if os.path.getsize(target_file) > CHARACTER_LIMIT_GET_FILE_CONTENT:
                content += (f'[...File "{file_path}" truncated at {CHARACTER_LIMIT_GET_FILE_CONTENT} characters]'
                            )
        return content
    except Exception as e:
        return f'Error: failed to read file "{e}"'
