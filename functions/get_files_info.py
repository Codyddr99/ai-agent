import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        # Convert working_directory to absolute path and normalize it
        working_directory = os.path.abspath(working_directory)
        working_directory = os.path.normpath(working_directory)
        
        # Create the full path by joining working_directory with the relative directory
        full_path = os.path.join(working_directory, directory)
        
        # Normalize the full path to resolve any ".." or "." components
        full_path = os.path.normpath(full_path)

        # Check if the full path is within the working directory boundaries
        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the directory exists and is actually a directory
        if not os.path.exists(full_path):
            return f'Error: "{directory}" does not exist'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        # List the contents of the directory
        entries = os.listdir(full_path)
        entries.sort()  # Sort alphabetically for consistent output

        result_lines = []
        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            is_dir = os.path.isdir(entry_path)
            file_size = os.path.getsize(entry_path)
            result_lines.append(
                f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
