import os
from google.genai import types
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

# define schema for export
schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Reads the contents of a file truncating at a char limit set in config, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The relative path of the file to the working directory.",
            )
        },
        required=["file_path"],  # mark file_path as mandatory
    ),
)
    

