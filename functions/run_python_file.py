import os
import subprocess
import sys
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    try:
        # Convert working_directory to absolute path and normalize it
        working_directory = os.path.abspath(working_directory)
        working_directory = os.path.normpath(working_directory)
        
        # Create the full path by joining working_directory with the relative file_path
        full_path = os.path.join(working_directory, file_path)
        
        # Normalize the full path to resolve any ".." or "." components
        full_path = os.path.normpath(full_path)

        # Check if the full path is within the working directory boundaries
        if not full_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'

        # Check if the file is a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
            [sys.executable, file_path] + args,
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30,
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


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
