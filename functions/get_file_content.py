import os
import sys
from config import MAX_FILE_READ_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
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
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists and is actually a regular file
        if not os.path.exists(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r") as file:
            content = file.read()

        if len(content) > MAX_FILE_READ_CHARS:
            content = content[:MAX_FILE_READ_CHARS]
            content += (
                f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARS} characters]'
            )

        return content

    except UnicodeDecodeError:
        return f'Error: Cannot read "{file_path}" - file appears to be binary or uses an unsupported encoding'
    except PermissionError:
        return f'Error: Permission denied reading "{file_path}"'
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
