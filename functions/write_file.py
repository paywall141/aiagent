import os
def write_file(working_directory, file_path, content):
    try:
        fullpath = os.path.abspath(os.path.join(working_directory,file_path ))
        working_directory_abs = os.path.abspath(working_directory)

        # validate path
        if not fullpath.startswith(working_directory_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # validate file_path exists, build path if not
        if not os.path.exists(fullpath):
            os.makedirs(os.path.dirname(fullpath), exist_ok=True)

        # write content to file at path
        with open(fullpath, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}" 



