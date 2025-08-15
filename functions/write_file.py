import os
from google.genai import types


def write_file(working_directory, file_path, content):
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
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Create the directory structure if it doesn't exist
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(full_path, "w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except PermissionError:
        return f'Error: Permission denied writing to "{file_path}"'
    except Exception as e:
        return f"Error: {str(e)}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, creating it if it doesn't exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
