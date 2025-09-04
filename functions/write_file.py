import os
from google.genai import types
from helpers.validators import *
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # validate relative path
        full_path, err = validate_relative_path( working_directory, file_path, keyword = "write" )
        if err:
            return err

        # validate file_path exists, build path if not
        if not validate_path_exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # write content to file at path...this will overwrite as long as function is called even if content is not provided
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}" 


# define schema for export
schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Write or overwrite files with provided content. -Careful- this will overwrite as long as path is valid!, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The relative path of the file to write to within the working directory. If does not exist but is valid then folde structure is created.",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "Content to write to file."
            ),
        },
        required = ["file_path", "content"], # args is optional
    )
)
