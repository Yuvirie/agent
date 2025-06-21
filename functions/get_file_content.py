import os

def get_file_content(working_directory, file_path):

    try:

        scope = os.path.abspath(working_directory)
        full_file_path = os.path.abspath(os.path.join(scope, file_path))

        if not full_file_path.startswith(scope):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory' 
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000

        with open(full_file_path, "r") as file:
            text = file.read().strip().split()
            len_chars = sum(len(word) for word in text)
            file_content_string = ""

            file.seek(0)
            
            if len_chars > MAX_CHARS:
                file_content_string = file.read(MAX_CHARS)
                file_content_string += f"[...File {file_path} truncated at 10000 characters]"
            else:
                file_content_string = file.read()

        return file_content_string

    except Exception as e:
        return f"Error: {e}"