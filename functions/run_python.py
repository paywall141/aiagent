import os
import subprocess
from helpers.validators import *

def run_python_file(working_directory, file_path, args=[]):
    try:      
        # validate path, create string ref to abs if valid
        full_path, err = validate_relative_path( working_directory, file_path, keyword = "execute" )
        if err:
            return err

        # validate file_path exists error out if not
        if not validate_path_exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        if args is None:
            args = []
        # Build the args and pass extra args
        cmd = ["uv", "run", full_path] + args

        result = subprocess.run(cmd, capture_output=True, cwd=working_directory, timeout=30, text=True)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"

        # if no content error out, white space removed
        output = result.stdout.strip() + result.stderr.strip()
        if not output:
            return "No output produced."

        return f"""STDOUT:\n{result.stdout}\nSTDERR:{result.stderr}"""        

    except Exception as e:
        return f"Error: {e}" 
