import os
from config import MAX_CHARS
from helpers.validators import *

def get_file_content(working_directory, file_path):
    try:       
        # validate relative path
        full_path, err = validate_relative_path( working_directory, file_path, keyword = "read" )
        if err:
            return err

        # validate is file
        err = validate_is_file(working_directory, file_path)
        if err:
            return err
        
        with open(full_path) as f:
            # always truncate at max_chars +1 to avoid reading whole file in
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                file_content_string[:MAX_CHARS] += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"


    

