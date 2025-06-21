import os
import subprocess

def run_python_file(working_directory, file_path):

    try:
        scope = os.path.abspath(working_directory)
        full_file_path = os.path.abspath(os.path.join(scope, file_path))

        if not full_file_path.startswith(scope):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_file_path):
            return f'Error: File "{file_path}" not found.'

        _, extension = os.path.splitext(full_file_path)

        if extension != ".py":
            return f'Error: "{file_path}" is not a Python file.'

    except Exception as e:
        return f"Error: {e}"

    try:

        #result of the command run in obj format
        result = subprocess.run(["python",full_file_path], capture_output=True, timeout=30, cwd=scope)
        output = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"


        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            output += f"\nNo output produced."

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
