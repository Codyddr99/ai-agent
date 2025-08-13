import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        
        full_path = os.path.normpath(full_path)
        
        if not full_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        result = subprocess.run(
            [sys.executable, file_path] + args,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30
        )

        output = []

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not output:
            return "No output produced."
        return "\n".join(output)
    
    except subprocess.TimeoutExpired:
        return f"Error: executing Python file: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"