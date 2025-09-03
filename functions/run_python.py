import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        fullpath = os.path.abspath(os.path.join(working_directory,file_path ))
        working_directory_abs = os.path.abspath(working_directory)

        # validate path
        if not fullpath.startswith(working_directory_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # validate file_path exists
        if not os.path.exists(fullpath):
            return f'Error: File "{file_path}" not found.'
        
        if not fullpath.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        if args is None:
            args = []
        # Build the args and pass extra args
        cmd = ["uv", "run", fullpath] + args

        # meat of the function
        result = subprocess.run(cmd, capture_output=True, cwd=working_directory, timeout=30, text=True)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"

        output = result.stdout.strip() + result.stderr.strip()
        if not output:
            return "No output produced."

        final_str = f"""STDOUT:\n{result.stdout}\nSTDERR:{result.stderr}"""        
        return final_str

    except Exception as e:
        return f"Error: {e}" 
