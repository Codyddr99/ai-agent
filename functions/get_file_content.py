import os
import sys
from config import MAX_FILE_READ_CHARS

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        
        full_path = os.path.normpath(full_path)
        
        if not full_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path, 'r') as file:
            content = file.read()
        
        if len(content) > MAX_FILE_READ_CHARS:
            content = content[:MAX_FILE_READ_CHARS]
            content += f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARS} characters]'
        
        return content
        
    except UnicodeDecodeError:
        return f'Error: Cannot read "{file_path}" - file appears to be binary or uses an unsupported encoding'
    except PermissionError:
        return f'Error: Permission denied reading "{file_path}"'
    except Exception as e:
        return f"Error: {str(e)}"