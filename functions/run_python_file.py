import os
import subprocess
from config import RUN_PY_TIMEOUT
def run_python_file(working_directory, file_path, args=[]):
    wrkdir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(wrkdir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'

    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        all_args =  ["python3", target_file]
        if args:
            all_args.extend(args)
        process = subprocess.run(timeout=RUN_PY_TIMEOUT, args=all_args, capture_output=True, cwd=wrkdir_abs, text=True)
        process.check_returncode

        output = []

        if process.stdout:
            output.append(f"STDOUT: {process.stdout}")
        if process.stderr:
            output.append(f"STDERR: {process.stderr}")

        if process.returncode != 0:
            output.append(f"Process exitedd with code {process.returncode}")

        return "\n".join(output) if output else "No output produced."
    
    except Exception as e:
        return f"Error: executing Python file: {e}"

    


