import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        
        full_path = os.path.normpath(full_path)
        
        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
                
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        entries = os.listdir(full_path)
        
        result_lines = []
        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            is_dir = os.path.isdir(entry_path)
            file_size = os.path.getsize(entry_path)
            result_lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: {str(e)}"