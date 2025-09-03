import os 

def get_files_info(working_directory, directory="."):
    try:    
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory_abs = os.path.abspath(working_directory)
        
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        is_dir = os.path.isdir(full_path)
        if not is_dir:
            return f'Error: "{directory}" is not a directory'
        
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


