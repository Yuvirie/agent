import os

def get_files_info(working_directory, directory=None):
    try:
        scope = os.path.abspath(working_directory)
        if directory is None:
            full_directory = scope
        else:
            full_directory = os.path.abspath(os.path.join(scope, directory))

        #check the scope of the directory
        if not full_directory.startswith(scope):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        #check if directory is in fact directory
        if not os.path.isdir(full_directory):
            return f'Error: "{directory}" is not a directory'

        entries = []

        file_paths = list(map(lambda x: (full_directory + "/" + x, x), os.listdir(full_directory)))
        
        for file_path, file in file_paths:
            entries.append(f"{file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")

        output = "\n".join(entries)
        return output
    except Exception as e:
        return f"Error: {e}"