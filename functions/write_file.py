import os
from helpers.validators import *

def write_file(working_directory, file_path, content):
    try:
        # validate relative path
        full_path, err = validate_relative_path( working_directory, file_path, keyword = "write" )
        if err:
            return err

        # validate file_path exists, build path if not
        if not validate_path_exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # write content to file at path
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}" 



