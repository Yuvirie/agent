import os

def write_file(working_directory, file_path, content):
    try:
        scope = os.path.abspath(working_directory)
        full_file_path = os.path.abspath(os.path.join(scope, file_path))

        if not full_file_path.startswith(scope):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(os.path.dirname(full_file_path)):
            os.makedirs(os.path.dirname(full_file_path))
        
        with open(full_file_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}"