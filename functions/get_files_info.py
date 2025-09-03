import os 
from helpers.validators import *

def get_files_info(working_directory, directory="."):
    try:    
        # validate relative path
        full_path, err = validate_relative_path( working_directory, directory, keyword = "list" )
        if err:
            return err

        # validate is dir
        is_dir, err = validate_is_dir(working_directory,directory)
        if err:
            return err

        contents = os.listdir(full_path)
        lines = []
        for content in contents:
            abs_path = os.path.join(full_path, content)
            file_size = os.path.getsize(abs_path)
            is_dir = os.path.isdir(abs_path)
            lines.append(f"- {content}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"


