import os

def validate_relative_path( working_directory, file_path, keyword = "read" ):
    working_directory_abs = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory_abs,file_path))
    if not full_path.startswith(working_directory_abs):
        return None, f'Error: Cannot {keyword} "{file_path}" as it is outside the permitted working directory'
    return full_path, None

def validate_is_file(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory_abs,file_path))
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    return None

def validate_is_dir(working_directory, directory):
    working_directory_abs = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory_abs, directory))
    is_dir = os.path.isdir(full_path)
    if not is_dir:
        return None, f'Error: "{directory}" is not a directory'
    return  is_dir , None