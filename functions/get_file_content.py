import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # validate relative path
        full_path = os.path.abspath(os.path.join(working_directory,file_path))
        working_directory_abs = os.path.abspath(working_directory)
        
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path) as f:
            # always truncate at max_chars length
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) > MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"


    

