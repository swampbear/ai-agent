import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Makes it possible to write to new or existing python files constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory,",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is being written to the file at the file_path"
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    wrkpth_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(wrkpth_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file):
        with open(target_file, "a"): pass

    with open(target_file, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
