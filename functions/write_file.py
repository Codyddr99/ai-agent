import os

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        
        if not full_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(full_path, 'w') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except PermissionError:
        return f'Error: Permission denied writing to "{file_path}"'
    except Exception as e:
        return f"Error: {str(e)}"